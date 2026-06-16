# ramrecon/cli/commands/report.py

from __future__ import annotations
import os
import sys
import argparse
import webbrowser
from typing import List

from cmd2 import with_argparser, with_category
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

from ramrecon.utils.report_center import ReportGeneratorCenter, REPORTLAB_AVAILABLE
from ramrecon.config import settings

__mixin_name__ = "ReportMixin"

TEAL = "#2EC4B6"
console = Console()

class ReportMixin:
    _export_parser = argparse.ArgumentParser(description="Export session data")
    _export_parser.add_argument("format", nargs="?", choices=["json", "csv", "html", "pdf", "md", "all"], help="Export format")

    @with_argparser(_export_parser)
    @with_category("Reports")
    def do_export(self, args) -> None:
        self._run_export(args.format)

    def _run_export(self, format_name: str | None) -> None:
        if not self.session_results:
            console.print("[yellow][!] No modules have been run in this session. Run some modules first.[/yellow]")
            return

        if not self.target:
            self._prompt_target_if_needed()
            if not self.target:
                self.perror("No target specified.")
                return

        fmt = format_name
        if not fmt:
            console.print("""
╭──────────────────────────────╮
│   RAMRecon Export Center     │
╰──────────────────────────────╯

Select Export Format

[1] JSON Report
[2] CSV Report
[3] HTML Report
[4] PDF Report
[5] Markdown Report
[6] All Formats
[0] Back""")
            choice = Prompt.ask("Choice > ", choices=["0", "1", "2", "3", "4", "5", "6"], default="3").strip()
            if choice == "0":
                return
            mapping = {"1": "json", "2": "csv", "3": "html", "4": "pdf", "5": "md", "6": "all"}
            fmt = mapping[choice]

        # Generate report
        rep = ReportGeneratorCenter(self.target, self.session_results, self.session_history)
        rep.ensure_directories()
        
        fmt_label = fmt.upper() if fmt != "all" else "All"
        console.print(f"[green][+] Generating {fmt_label} Report...[/green]")
        console.print("[green][+] Saving evidence...[/green]")
        
        # Save individual raw modules
        rep.export_all_raw_modules()
        
        generated_paths = []
        
        if fmt in ("json", "all"):
            generated_paths.append(("JSON", rep.generate_json()))
        if fmt in ("csv", "all"):
            generated_paths.append(("CSV", rep.generate_csv()))
        if fmt in ("html", "all"):
            generated_paths.append(("HTML", rep.generate_html()))
        if fmt in ("pdf", "all"):
            if REPORTLAB_AVAILABLE:
                generated_paths.append(("PDF", rep.generate_pdf()))
            else:
                console.print("[red][!] ReportLab not available. PDF generation skipped.[/red]")
        if fmt in ("md", "all"):
            generated_paths.append(("Markdown", rep.generate_markdown()))

        console.print("[green][+] Report generated successfully.[/green]")
        console.print("\n[bold]Saved:[/bold]")
        for name, path in generated_paths:
            rel = os.path.relpath(path).replace("\\", "/")
            console.print(f"  [cyan]{rel}[/cyan]")
        console.print()

    @with_category("Reports")
    def do_report(self, _line) -> None:
        """Interactive reporting menu."""
        self._run_export(None)

    @with_category("Reports")
    def do_reports(self, _line) -> None:
        """List previous generated reports."""
        results_root = os.path.join(os.getcwd(), settings.RESULTS_DIR)
        if not os.path.exists(results_root):
            console.print("[yellow][!] No reports have been generated yet.[/yellow]")
            return

        table = Table(title="Generated Reports History", box=box.SIMPLE, expand=False)
        table.add_column("Target", style="cyan", no_wrap=True)
        table.add_column("Timestamp", style="green", no_wrap=True)
        table.add_column("Formats Available", style="magenta")

        found = False
        for target_dir in os.listdir(results_root):
            target_path = os.path.join(results_root, target_dir)
            if not os.path.isdir(target_path):
                continue
            for ts_dir in os.listdir(target_path):
                ts_path = os.path.join(target_path, ts_dir)
                if not os.path.isdir(ts_path):
                    continue
                
                # Check what report formats exist
                formats = []
                for ext in ["html", "pdf", "json", "csv", "md"]:
                    if os.path.exists(os.path.join(ts_path, f"report.{ext}")):
                        formats.append(ext.upper())
                        
                if formats:
                    table.add_row(target_dir, ts_dir.replace("_", " "), ", ".join(formats))
                    found = True

        if found:
            console.print(table)
        else:
            console.print("[yellow][!] No reports found in results directory.[/yellow]")

    @with_category("Reports")
    def do_openreport(self, _line) -> None:
        """Open latest HTML report in default browser."""
        results_root = os.path.join(os.getcwd(), settings.RESULTS_DIR)
        if not os.path.exists(results_root):
            console.print("[red][!] No reports have been generated yet.[/red]")
            return

        latest_path = None
        latest_time = 0
        
        for root, dirs, files in os.walk(results_root):
            for file in files:
                if file == "report.html":
                    html_path = os.path.join(root, file)
                    mtime = os.path.getmtime(html_path)
                    if mtime > latest_time:
                        latest_time = mtime
                        latest_path = html_path
                        
        if latest_path:
            console.print(f"[green][*] Opening latest report: {os.path.relpath(latest_path)}[/green]")
            webbrowser.open(f"file:///{os.path.abspath(latest_path)}")
        else:
            console.print("[red][!] HTML report not found.[/red]")

    @with_category("Reports")
    def do_history(self, _line) -> None:
        """View session history."""
        if not self.session_history:
            console.print("[yellow][!] No modules executed in this session yet.[/yellow]")
            return

        table = Table(title="Session History", box=box.SIMPLE, expand=False)
        table.add_column("Order", style="cyan", no_wrap=True)
        table.add_column("ID", style="yellow", no_wrap=True)
        table.add_column("Module Name", style="green")
        table.add_column("Execution Time", style="magenta")

        for idx, (mid, name, ts) in enumerate(self.session_history, 1):
            table.add_row(str(idx), mid, name, ts)
            
        console.print(table)
