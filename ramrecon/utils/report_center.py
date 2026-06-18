# ramrecon/utils/report_center.py

import os
import sys
import json
import csv
import re
import datetime
from typing import Dict, List, Tuple, Any

from ramrecon.config import settings
from ramrecon.core.catalog_cache import tools, tools_mapping

# ReportLab imports for PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

TEAL_COLOR = "#2EC4B6"
DARK_COLOR = "#1D3557"
RED_COLOR = "#ef4444"
YELLOW_COLOR = "#FFB703"

def strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_module_output(raw_output: str) -> Dict[str, Any]:
    """Parse raw output of a module using heuristics to build structured key-values."""
    clean_text = strip_ansi(raw_output)
    parsed = {}
    
    for line in clean_text.splitlines():
        line_str = line.strip()
        if not line_str:
            continue
            
        # Try table separator first
        if "│" in line_str or "|" in line_str:
            sep = "│" if "│" in line_str else "|"
            parts = [p.strip() for p in line_str.split(sep)]
            if len(parts) >= 2:
                key = parts[0]
                if not key:
                    continue
                # Filter out table border/decorations
                if any(c in key for c in "─┌┐└┘┬┴┼╶╴╵╷├┤┼═"):
                    continue
                # Skip header columns
                if key.lower() in ("key", "type", "field", "module", "name", "value(s)", "value", "option", "setting"):
                    continue
                val = sep.join(parts[1:]).strip()
                if not val or val in ("-", "—", "None", "Not set"):
                    continue
                # Split if value has list elements
                if ";" in val:
                    val = [item.strip() for item in val.split(";") if item.strip()]
                elif "," in val and not val.replace(" ", "").isdigit():
                    val = [item.strip() for item in val.split(",") if item.strip()]
                parsed[key] = val
                continue
                
        # Try standard key-value colon splitter
        if ":" in line_str:
            # Avoid splitting URLs, banners, or protocol names
            if (line_str.startswith("http://") or 
                line_str.startswith("https://") or 
                line_str.startswith("==") or 
                line_str.startswith("http2") or 
                line_str.startswith("http3") or
                "elapsed" in line_str.lower() or 
                "total" in line_str.lower()):
                continue
            key, val = line_str.split(":", 1)
            key, val = key.strip(), val.strip()
            # Ensure key is a short string and not part of text paragraphs or logs
            if 0 < len(key) < 35 and not key.startswith("[") and not key.startswith("*") and not key.startswith("!") and not key.startswith("-"):
                if not val or val in ("-", "—", "None", "Not set"):
                    continue
                # If value is list-like
                if ";" in val:
                    val = [item.strip() for item in val.split(";") if item.strip()]
                parsed[key] = val
                
    return parsed

def get_module_metadata(script_key: str) -> Tuple[str, str]:
    """Return (module_name, section_name) for a given script key."""
    for t in tools:
        if os.path.splitext(t.get("script", ""))[0] == script_key:
            return t["name"], t["section"]
    return script_key.replace("_", " ").title(), "Security & Threat Intelligence"

def determine_severity(output_text: str) -> str:
    """Analyze output text to determine finding severity (Critical, High, Medium, Info)."""
    text = output_text.lower()
    if any(x in text for x in ["critical", "severe", "exploit", "compromise"]):
        return "Critical"
    if any(x in text for x in ["high", "alert", "vulnerable", "expired"]):
        return "High"
    if any(x in text for x in ["warn", "warning", "risk", "exposed"]):
        return "Medium"
    return "Informational"

class ReportGeneratorCenter:
    def __init__(self, target: str, session_results: Dict[str, str], session_history: List[Tuple[str, str, str]]):
        self.target = target
        self.session_results = session_results
        self.session_history = session_history
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.iso_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # Determine paths
        from ramrecon.utils.util import clean_domain_input
        results_root = os.path.join(os.getcwd(), settings.RESULTS_DIR)
        target_clean = clean_domain_input(self.target)
        self.results_dir = os.path.join(results_root, target_clean, self.timestamp)
        self.modules_dir = os.path.join(self.results_dir, "modules")
        
        # Parse all session results
        self.parsed_results = {}
        self.severity_stats = {"Critical": 0, "High": 0, "Medium": 0, "Informational": 0}
        self.grouped_results = {
            "Network & Infrastructure": [],
            "Web Application Analysis": [],
            "Security & Threat Intelligence": []
        }
        
        for k, v in self.session_results.items():
            name, section = get_module_metadata(k)
            parsed_data = parse_module_output(v)
            sev = determine_severity(v)
            self.severity_stats[sev] += 1
            
            entry = {
                "script": k,
                "name": name,
                "severity": sev,
                "raw_output": v,
                "clean_output": strip_ansi(v),
                "parsed_data": parsed_data
            }
            
            self.parsed_results[k] = entry
            if section in self.grouped_results:
                self.grouped_results[section].append(entry)
            else:
                if "Other" not in self.grouped_results:
                    self.grouped_results["Other"] = []
                self.grouped_results["Other"].append(entry)
                
        # Calculate Risk Score
        if self.severity_stats["Critical"] > 0:
            self.risk_score = "Critical"
        elif self.severity_stats["High"] > 0:
            self.risk_score = "High"
        elif self.severity_stats["Medium"] > 0:
            self.risk_score = "Medium"
        else:
            self.risk_score = "Low"

    def ensure_directories(self):
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.modules_dir, exist_ok=True)

    def export_all_raw_modules(self) -> List[str]:
        paths = []
        for k, entry in self.parsed_results.items():
            txt_path = os.path.join(self.modules_dir, f"{k}.txt")
            json_path = os.path.join(self.modules_dir, f"{k}.json")
            
            # Write TXT
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(entry["clean_output"])
            paths.append(txt_path)
            
            # Write JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(entry["parsed_data"], f, indent=2, ensure_ascii=False)
            paths.append(json_path)
            
        return paths

    def generate_json(self) -> str:
        report_data = {
            "target": self.target,
            "generated_at": self.iso_timestamp,
            "risk_score": self.risk_score,
            "summary": {
                "total_modules": len(self.session_results),
                "severity_distribution": self.severity_stats
            },
            "modules": {k: entry["parsed_data"] for k, entry in self.parsed_results.items()}
        }
        path = os.path.join(self.results_dir, "report.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        return path

    def generate_csv(self) -> str:
        path = os.path.join(self.results_dir, "report.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["module", "key", "value"])
            for k, entry in self.parsed_results.items():
                for key, val in entry["parsed_data"].items():
                    if isinstance(val, list):
                        val_str = "; ".join(map(str, val))
                    else:
                        val_str = str(val)
                    writer.writerow([k, key, val_str])
        return path

    def generate_markdown(self) -> str:
        path = os.path.join(self.results_dir, "report.md")
        lines = [
            f"# RAMRecon Investigation Report - {self.target}",
            "",
            f"**Target:** `{self.target}`",
            f"**Generated:** `{self.timestamp}`",
            f"**Overall Risk Score:** `{self.risk_score}`",
            "",
            "## Severity Findings Summary",
            f"- 🔴 **Critical:** {self.severity_stats['Critical']}",
            f"- 🟠 **High:** {self.severity_stats['High']}",
            f"- 🟡 **Medium:** {self.severity_stats['Medium']}",
            f"- 🟢 **Informational:** {self.severity_stats['Informational']}",
            "",
            "---",
            ""
        ]
        
        for section, entries in self.grouped_results.items():
            if not entries:
                continue
            lines.append(f"## {section}")
            lines.append("")
            for entry in entries:
                lines.append(f"### {entry['name']}")
                lines.append(f"- **Severity:** `{entry['severity']}`")
                lines.append("")
                if entry["parsed_data"]:
                    for key, val in entry["parsed_data"].items():
                        if isinstance(val, list):
                            val_str = ", ".join(map(str, val))
                        else:
                            val_str = str(val)
                        lines.append(f"- **{key}:** {val_str}")
                else:
                    lines.append("No structured key-value data extracted. Raw output snippet:")
                    lines.append("```")
                    snippet = "\n".join(entry["clean_output"].splitlines()[:15])
                    lines.append(snippet)
                    lines.append("```")
                lines.append("")
                
        lines.append("---")
        lines.append("*Generated by RAMRecon v2.0 - Cyber Reconnaissance & Intelligence Framework*")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return path

    def generate_html(self) -> str:
        path = os.path.join(self.results_dir, "report.html")
        
        # Build modules overview checklist HTML
        checklist_items = []
        for entries in self.grouped_results.values():
            for entry in entries:
                checklist_items.append(f"<li><span class='check-mark'>✓</span> {entry['name']}</li>")
        checklist_html = "\n".join(checklist_items)

        # Build details HTML
        details_html = []
        for section, entries in self.grouped_results.items():
            if not entries:
                continue
            details_html.append(f"<div class='section-title'>{section}</div>")
            for entry in entries:
                sev_class = entry['severity'].lower()
                details_html.append(f"<div class='card'>")
                details_html.append(f"  <div class='card-header'>")
                details_html.append(f"    <span class='module-title'>{entry['name']}</span>")
                details_html.append(f"    <span class='badge {sev_class}'>{entry['severity']}</span>")
                details_html.append(f"  </div>")
                details_html.append(f"  <div class='card-body'>")
                
                if entry["parsed_data"]:
                    details_html.append("    <table class='data-table'>")
                    details_html.append("      <thead><tr><th>Field</th><th>Value</th></tr></thead>")
                    details_html.append("      <tbody>")
                    for key, val in entry["parsed_data"].items():
                        if isinstance(val, list):
                            val_str = "<br>".join(map(str, val))
                        else:
                            val_str = str(val)
                        details_html.append(f"        <tr><td>{key}</td><td>{val_str}</td></tr>")
                    details_html.append("      </tbody>")
                    details_html.append("    </table>")
                else:
                    details_html.append("    <pre class='raw-output'>")
                    details_html.append(entry["clean_output"])
                    details_html.append("    </pre>")
                
                details_html.append(f"  </div>")
                details_html.append(f"</div>")
        
        full_details_html = "\n".join(details_html)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAMRecon Report - {self.target}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {TEAL_COLOR};
            --dark: {DARK_COLOR};
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #2d3748;
            --critical: {RED_COLOR};
            --high: {RED_COLOR};
            --medium: {YELLOW_COLOR};
            --info: #2EC4B6;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        header {{
            background: linear-gradient(135deg, var(--dark) 0%, #0d1b2a 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-bottom: 5px solid var(--primary);
        }}
        h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -1px;
        }}
        .subtitle {{
            color: var(--primary);
            font-weight: 600;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.9rem;
        }}
        .container {{
            max-width: 1000px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 40px;
        }}
        .summary-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .summary-title {{
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--bg);
            padding-bottom: 10px;
            color: var(--dark);
        }}
        .meta-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .meta-list li {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #edf2f7;
        }}
        .meta-list li:last-child {{
            border-bottom: none;
        }}
        .meta-label {{
            font-weight: 600;
            color: #718096;
        }}
        .meta-val {{
            font-weight: 700;
            color: var(--dark);
        }}
        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            color: white;
        }}
        .badge.critical {{ background-color: var(--critical); }}
        .badge.high {{ background-color: var(--high); }}
        .badge.medium {{ background-color: var(--medium); }}
        .badge.informational {{ background-color: var(--info); }}
        .badge.low {{ background-color: var(--info); }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }}
        .stat-box {{
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            color: white;
            font-weight: 700;
        }}
        .stat-box.critical {{ background-color: var(--critical); }}
        .stat-box.high {{ background-color: var(--high); }}
        .stat-box.medium {{ background-color: var(--medium); }}
        .stat-box.informational {{ background-color: var(--info); }}
        .stat-num {{
            font-size: 1.8rem;
            display: block;
        }}
        .stat-lbl {{
            font-size: 0.7rem;
            text-transform: uppercase;
            opacity: 0.9;
        }}
        
        .checklist {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        .checklist li {{
            font-weight: 600;
            color: var(--dark);
        }}
        .check-mark {{
            color: var(--primary);
            margin-right: 5px;
            font-weight: 700;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--dark);
            margin: 40px 0 20px 0;
            border-left: 5px solid var(--primary);
            padding-left: 15px;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #edf2f7;
            overflow: hidden;
        }}
        .card-header {{
            background-color: var(--dark);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .module-title {{
            font-weight: 700;
            font-size: 1.1rem;
        }}
        .card-body {{
            padding: 20px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-table th, .data-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #edf2f7;
        }}
        .data-table th {{
            background-color: #f7fafc;
            font-weight: 600;
            color: #4a5568;
        }}
        .data-table tr:hover {{
            background-color: #fafdff;
        }}
        .raw-output {{
            background-color: #1a202c;
            color: #a0aec0;
            padding: 15px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            white-space: pre-wrap;
            margin: 0;
        }}
        footer {{
            text-align: center;
            padding: 40px 20px;
            background-color: var(--dark);
            color: white;
            margin-top: 60px;
            border-top: 5px solid var(--primary);
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>RAMRecon Investigation Report</h1>
        <div class="subtitle">Cyber Reconnaissance & Intelligence Framework</div>
    </header>
    <div class="container">
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Executive Summary</div>
                <ul class="meta-list">
                    <li>
                        <span class="meta-label">Target Domain / IP</span>
                        <span class="meta-val">{self.target}</span>
                    </li>
                    <li>
                        <span class="meta-label">Report Generation Date</span>
                        <span class="meta-val">{self.timestamp} UTC</span>
                    </li>
                    <li>
                        <span class="meta-label">Risk Profile</span>
                        <span class="meta-val"><span class="badge {self.risk_score.lower()}">{self.risk_score}</span></span>
                    </li>
                    <li>
                        <span class="meta-label">Total Executed Modules</span>
                        <span class="meta-val">{len(self.session_results)}</span>
                    </li>
                </ul>
                <div class="stat-grid">
                    <div class="stat-box critical">
                        <span class="stat-num">{self.severity_stats['Critical']}</span>
                        <span class="stat-lbl">Critical</span>
                    </div>
                    <div class="stat-box high">
                        <span class="stat-num">{self.severity_stats['High']}</span>
                        <span class="stat-lbl">High</span>
                    </div>
                    <div class="stat-box medium">
                        <span class="stat-num">{self.severity_stats['Medium']}</span>
                        <span class="stat-lbl">Medium</span>
                    </div>
                    <div class="stat-box informational">
                        <span class="stat-num">{self.severity_stats['Informational']}</span>
                        <span class="stat-lbl">Info</span>
                    </div>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Executed Scope</div>
                <ul class="checklist">
                    {checklist_html}
                </ul>
            </div>
        </div>
        
        {full_details_html}
    </div>
    <footer>
        <p>Generated by RAMRecon v2.0 - Cybersecurity Investigation and Surface Mapping Platform</p>
    </footer>
</body>
</html>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return path

    def generate_pdf(self) -> str:
        if not REPORTLAB_AVAILABLE:
            return ""
            
        path = os.path.join(self.results_dir, "report.pdf")
        doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
        story = []
        
        styles = getSampleStyleSheet()
        
        # Modify existing styles to avoid adding duplicate names
        title_style = ParagraphStyle(
            'PDFTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor(DARK_COLOR),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'PDFSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor(TEAL_COLOR),
            spaceAfter=30
        )
        h1_style = ParagraphStyle(
            'PDFH1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=colors.HexColor(DARK_COLOR),
            spaceBefore=15,
            spaceAfter=10,
            keepWithNext=True
        )
        h2_style = ParagraphStyle(
            'PDFH2',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor(TEAL_COLOR),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        )
        body_style = ParagraphStyle(
            'PDFBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#333333"),
            spaceAfter=6
        )
        code_style = ParagraphStyle(
            'PDFCode',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#444444")
        )
        
        # Header / Title
        story.append(Paragraph("RAMRecon Investigation Report", title_style))
        story.append(Paragraph("Cyber Reconnaissance & Intelligence Framework", subtitle_style))
        
        # Executive Summary section
        story.append(Paragraph("Executive Summary", h1_style))
        summary_data = [
            [Paragraph("<b>Target</b>", body_style), Paragraph(self.target, body_style)],
            [Paragraph("<b>Generated</b>", body_style), Paragraph(f"{self.timestamp} UTC", body_style)],
            [Paragraph("<b>Overall Risk Score</b>", body_style), Paragraph(f"<b>{self.risk_score}</b>", body_style)],
            [Paragraph("<b>Modules Executed</b>", body_style), Paragraph(str(len(self.session_results)), body_style)],
            [Paragraph("<b>Critical Findings</b>", body_style), Paragraph(str(self.severity_stats["Critical"]), body_style)],
            [Paragraph("<b>High Findings</b>", body_style), Paragraph(str(self.severity_stats["High"]), body_style)],
            [Paragraph("<b>Medium Findings</b>", body_style), Paragraph(str(self.severity_stats["Medium"]), body_style)],
            [Paragraph("<b>Informational Findings</b>", body_style), Paragraph(str(self.severity_stats["Informational"]), body_style)],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5 * inch, 4.0 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8F9FA")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Details grouping
        for section, entries in self.grouped_results.items():
            if not entries:
                continue
            story.append(Paragraph(section, h1_style))
            for entry in entries:
                module_elements = []
                module_elements.append(Paragraph(entry["name"], h2_style))
                module_elements.append(Paragraph(f"<b>Severity:</b> {entry['severity']}", body_style))
                module_elements.append(Spacer(1, 4))
                
                if entry["parsed_data"]:
                    table_data = [[Paragraph("<b>Field</b>", body_style), Paragraph("<b>Value</b>", body_style)]]
                    for key, val in entry["parsed_data"].items():
                        if isinstance(val, list):
                            val_str = ", ".join(map(str, val))
                        else:
                            val_str = str(val)
                        table_data.append([Paragraph(key, body_style), Paragraph(val_str, body_style)])
                        
                    data_table = Table(table_data, colWidths=[2.2 * inch, 4.3 * inch])
                    data_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(DARK_COLOR)),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                        ('PADDING', (0, 0), (-1, -1), 6),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    # Quick fix for text color inside header row cells:
                    for i in range(2):
                        table_data[0][i].style.textColor = colors.white
                    
                    module_elements.append(data_table)
                else:
                    snippet = "\n".join(entry["clean_output"].splitlines()[:20])
                    code_para = Paragraph(snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)
                    code_table = Table([[code_para]], colWidths=[6.5 * inch])
                    code_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1A202C")),
                        ('PADDING', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#2D3748")),
                    ]))
                    module_elements.append(code_table)
                    
                module_elements.append(Spacer(1, 15))
                story.append(KeepTogether(module_elements))
                
        # Footer build callback
        def add_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor("#718096"))
            canvas.drawString(54, 36, "Generated by RAMRecon v2.0")
            canvas.drawRightString(doc.pagesize[0] - 54, 36, f"Page {doc.page}")
            canvas.restoreState()
            
        doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
        return path
