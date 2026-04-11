# RAMRecon: Cyber Reconnaissance & Intelligence Framework

**RAMRecon** is an all-in-one, Python-powered cyber reconnaissance and security intelligence framework designed to streamline information gathering, infrastructure analysis, web surface inspection, and exposure assessment from a single unified interface.

It combines a professional interactive CLI, modular architecture, analyst-focused workflows, and exportable reporting into one platform built for **cybersecurity researchers, students, SOC analysts, defenders, and authorized investigation environments**.

---

## ⚠️ Legal & Ethical Notice

RAMRecon is intended **strictly for authorized, educational, defensive, and ethical security assessment**.

The author is **not responsible** for misuse, unauthorized scanning, abuse, or any activity that violates applicable laws, regulations, or organizational policy.

By using this tool, you agree that:

- You will only assess systems you **own** or are **explicitly authorized** to test.
- You understand that some modules may generate network traffic or external lookups.
- You are solely responsible for ensuring your use complies with legal and ethical boundaries.

---

## 🚀 Key Features

- **Interactive CLI** with structured workflow commands
- **50 carefully selected modules** across recon, web, and security analysis
- **Professional terminal UI** with formatted tables, panels, and progress indicators
- **Batch execution** for running multiple modules efficiently
- **Profile-based workflows** for quick investigations
- **Favorites system** for commonly used modules
- **Multi-threaded execution** for improved speed
- **Threat intelligence integrations** (Shodan, VirusTotal, Censys, SSL Labs, CT logs)
- **Export support** for JSON, CSV, and TXT outputs
- **Configurable settings** for profiles, API keys, threading, and behavior
- **Designed for extensibility** with scalable module architecture

---

## 🧱 Project Scope

RAMRecon is designed as a **unified cyber recon platform**, bringing together functionality that is often spread across multiple tools.

Its capabilities are organized into six major categories:


### Commands Cheatsheet

| Command | Category | Description | Example |
|---------|----------|-------------|---------|
| `modules` | Discovery | List all modules | `modules` |
| `modules -d` | Discovery | List with details | `modules -d` |
| `search` | Discovery | Search by keyword | `search ssl` |
| `use` | Selection | Select module | `use 42` |
| `helpmod` | Help | Module help | `helpmod 42` |
| `set target` | Config | Set target | `set target example.com` |
| `set` | Config | Set options | `set threads 20` |
| `unset` | Config | Unset options | `unset target` |
| `opts` | Config | Show options | `opts` |
| `scope` | Config | Show config | `scope` |
| `profile` | Config | Apply profile | `profile speed` |
| `run` | Execute | Run selected | `run` |
| `runall` | Execute | Run category | `runall infra` |
| `runfav` | Execute | Run favorites | `runfav` |
| `last` | Execute | Re-run last | `last` |
| `fav` | Favorites | Manage favorites | `fav add 42` |
| `show modules` | Info | Browse modules | `show modules` |
| `show api_status` | Info | Check APIs | `show api_status` |
| `show options` | Info | Show options | `show options` |
| `show options_full` | Info | Detailed options | `show options_full` |
| `info` | Info | Project info | `info` |
| `recent` | Info | Recent modules | `recent` |
| `viewout` | Output | View cached output | `viewout` |
| `grepout` | Output | Search output | `grepout "192.168"` |
| `clear` | Utility | Clear screen | `clear` |
| `banner` | Utility | Show banner | `banner` |
| `reset` | Utility | Reset config | `reset` |
| `exit` | Utility | Exit RAMRecon | `exit` |
| `quit` | Utility | Exit RAMRecon | `quit` |
| `help` | Help | Show help | `help` |



RAMRecon currently includes **50 carefully selected reconnaissance and security analysis modules** designed to support practical cyber investigation, infrastructure profiling, web surface inspection, and exposure discovery workflows.

# 🌐 Network & Infrastructure Reconnaissance

These modules focus on **domain intelligence, DNS visibility, transport behavior, certificate analysis, and network-level discovery**.

They are intended to help analysts understand how a target is exposed at the infrastructure level before moving into deeper application and security analysis.

### Included Modules

- **Associated Hosts** — Identify related hosts and connected infrastructure
- **DNS Over HTTPS** — Validate DoH support and resolver behavior
- **DNS Records** — Retrieve A, AAAA, MX, NS, TXT, and CNAME records
- **DNSSEC Check** — Verify whether DNSSEC is configured and exposed
- **Domain Info** — Collect domain-level metadata and registration context
- **Domain Reputation Check** — Assess general trust and reputation signals
- **HTTP/2 & HTTP/3 Support** — Detect protocol support and transport capabilities
- **IP Info** — Gather IP ownership, ASN, and routing context
- **Open Ports Scan** — Identify exposed TCP service ports
- **Server Info** — Collect web server banner and response information
- **Server Location** — Resolve geolocation and hosting context
- **SSL Chain Analysis** — Inspect certificate chain validity and trust path
- **SSL Expiry Alert** — Detect certificate expiration risk
- **TLS Cipher Suites** — Enumerate supported TLS ciphers
- **Traceroute** — Map path visibility to the target
- **TXT Records** — Extract TXT-based metadata and service configuration
- **WHOIS Lookup** — Retrieve WHOIS registration information
- **ASN Lookup** — Identify ASN ownership and network association

---

## 🕸️ Web Application Surface Analysis

These modules focus on **content discovery, crawling, web behavior, client-side analysis, and application exposure mapping**.

They help analysts understand the visible attack surface of a target application and identify weak or interesting exposure points.

### Included Modules

- **Archive History** — Review historical snapshots and archived content
- **Broken Links Detection** — Identify dead or misconfigured links
- **CMS Detection** — Detect content management systems and platforms
- **Cookies Analyzer** — Inspect cookie attributes, scope, and security flags
- **Content Discovery** — Discover exposed files, paths, and web resources
- **Crawler** — Crawl linked pages and enumerate site structure
- **Robots.txt Analyzer** — Inspect robots directives and hidden paths
- **Directory Finder** — Identify accessible directories and paths
- **Redirect Chain** — Analyze redirect behavior and chain logic
- **Sitemap Parsing** — Parse sitemap.xml and enumerate indexed pages
- **Technology Stack Detection** — Identify frameworks, libraries, and platforms
- **JavaScript File Analyzer** — Analyze linked JavaScript resources
- **CORS Misconfiguration Scanner** — Detect insecure CORS behavior
- **Hidden Parameter Discovery** — Identify potentially hidden request parameters
- **Clickjacking Test** — Check framing protections and clickjacking exposure
- **Favicon Hashing** — Generate favicon hashes for fingerprinting and correlation
- **HTML Comments Extractor** — Extract comments from page source
- **JavaScript Obfuscation Detector** — Detect suspicious or heavily obfuscated JS
- **HTTP Method Enumerator** — Identify allowed HTTP methods
- **GraphQL Introspection Probe** — Check GraphQL introspection exposure

---

## 🛡️ Security & Threat Intelligence

These modules focus on **security posture review, exposure detection, reputation enrichment, and intelligence-based visibility**.

They are designed to help analysts identify weak configurations, exposed artifacts, and external intelligence signals associated with a target.

### Included Modules

- **Data Leak Detection** — Search for exposure indicators and leaked references
- **Exposed Environment Files** — Detect exposed `.env` and sensitive config files
- **Firewall Detection** — Identify possible WAF or filtering technologies
- **HTTP Headers** — Retrieve and inspect HTTP response headers
- **HTTP Security Features** — Evaluate common security headers and hardening signals
- **Malware & Phishing Check** — Assess known malicious or phishing-related indicators
- **Security.txt Check** — Verify presence and validity of `security.txt`
- **Shodan Reconnaissance** — Enrich host visibility using Shodan
- **SSL Labs Report** — Integrate SSL Labs style certificate posture review
- **Subdomain Enumeration** — Discover visible subdomains
- **VirusTotal Scan** — Enrich indicators with VirusTotal reputation context
- **CT Log Query** — Query certificate transparency logs for subdomain and cert visibility

---

## 🎯 Why This Module Set Matters

The RAMRecon module set is intentionally designed to be:

- **practical** for real-world recon workflows
- **maintainable** as a serious project
- **defensible** in interviews, demos, and project reviews
- **modular** for future growth
- **strong enough** to showcase analyst-oriented engineering skills

---


---

## 📦 Installation

### Option 1 — Run Directly from Source

```bash
git clone https://github.com/sairamdhonthula/ramrecon.git
cd ramrecon
pip install -r requirements.txt
python -m ramrecon

👨‍💻 Author

Dhonthula Sairam
Cybersecurity Student | Security Research Enthusiast | Investigation Workflow Builder
