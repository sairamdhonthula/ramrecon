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
- **135 modular capabilities** across recon, web, and security analysis
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



### 📋 **All Modules** *(135 total)*

| Network & Infrastructure | Web Application Analysis | Security & Threat Intelligence |
|--------------------------|---------------------------|--------------------------------|
| 1. Associated Hosts | 53. Archive History | 103. Censys Reconnaissance |
| 2. DNS Over HTTPS | 54. Broken Links Detection | 104. Certificate Authority Recon |
| 3. DNS Records | 55. Carbon Footprint | 105. Data Leak Detection |
| 4. DNSSEC Check | 56. CMS Detection | 106. Exposed Environment Files |
| 5. Domain Info | 57. Cookies Analyzer | 107. Firewall Detection |
| 6. Domain Reputation Check | 58. Content Discovery | 108. Global Ranking |
| 7. HTTP/2 & HTTP/3 Support | 59. Crawler | 109. HTTP Headers |
| 8. IP Info | 60. Robots.txt Analyzer | 110. HTTP Security Features |
| 9. Open Ports Scan | 61. Directory Finder | 111. Malware & Phishing Check |
| 10. Server Info | 62. Email Harvesting | 112. Pastebin Monitoring |
| 11. Server Location | 63. Performance Monitoring | 113. Privacy & GDPR Compliance |
| 12. SSL Chain Analysis | 64. Quality Metrics | 114. Security.txt Check |
| 13. SSL Expiry Alert | 65. Redirect Chain | 115. Shodan Reconnaissance |
| 14. TLS Cipher Suites | 66. Sitemap Parsing | 116. SSL Labs Report |
| 15. TLS Handshake Simulation | 67. Social Media Presence | 117. SSL Pinning Check |
| 16. Traceroute | 68. Technology Stack Detection | 118. Subdomain Enumeration |
| 17. TXT Records | 69. Third-Party Integrations | 119. Subdomain Takeover |
| 18. WHOIS Lookup | 70. JavaScript File Analyzer | 120. VirusTotal Scan |
| 19. Zone Transfer | 71. CORS Misconfiguration Scanner | 121. CT Log Query |
| 20. ASN Lookup | 72. Login Page Brute Identifier | 122. Breached Credentials Lookup |
| 21. Reverse IP Lookup | 73. Hidden Parameter Discovery | 123. Cloud Bucket Exposure |
| 22. IP Range Scanner | 74. Clickjacking Test | 124. JWT Token Analyzer |
| 23. RDAP Lookup | 75. Form Grabber | 125. Exposed API Endpoints |
| 24. NTP Information Leak | 76. Favicon Hashing | 126. Git Repository Exposure Check |
| 25. IPv6 Reachability Test | 77. HTML Comments Extractor | 127. Typosquat Domain Checker |
| 26. BGP Route Analysis | 78. CAPTCHA Presence Checker | 128. SPF / DKIM / DMARC Validator |
| 27. CDN Detection | 79. JavaScript Obfuscation Detector | 129. Open Redirect Finder |
| 28. Reverse DNS Scan | 80. Virtual Host Fuzzer | 130. Rate-Limit & WAF Bypass Test |
| 29. Network Timezone Detection | 81. Session Cookie Lifetime Checker | 131. Security Changelog Diff |
| 30. Geo-DNS Footprint | 82. HTML5 Feature Abuse Detector | 132. Session Hijacking (Passive) |
| 31. SPF Network Extractor | 83. Autocomplete Vulnerability Checker | 133. Rogue Certificate Check |
| 32. NS Geo/ASN Diversity | 84. Embedded Object Hunter | 134. JS Malware Scanner |
| 33. DNS SLA Latency Monitor | 85. Multi-Language URL Tester | 135. Cloud Service Enumeration |
| 34. RPKI Route Validity | 86. Pixel Tracker Finder | |
| 35. Recursive Nameserver Leak | 87. SEO Abuse Detector | |
| 36. Dual-Stack Behavior Profiler | 88. Dependency JS/CDN Scanner | |
| 37. ICMP Reachability Matrix | 89. WebSocket Endpoint Sniffer | |
| 38. IP Allocation History Tracker | 90. API Schema Grabber | |
| 39. Autonomous Neighbor Peering Map | 91. Lazy-Load Resource Finder | |
| 40. TLS Session Resumption Map | 92. HTTP Method Enumerator | |
| 41. Network Certificate Inventory | 93. GraphQL Introspection Probe | |
| 42. SSH Banner & Key Fingerprinter | 94. File Upload Surface Finder | |
| 43. SNMP Public Community Checker | 95. DOM Sink Scanner | |
| 44. SNMP Bulk Walk | 96. Cache Behavior Analyzer | |
| 45. UDP Service Sampler | 97. Cookie Scope Diff Across Subdomains | |
| 46. NetBIOS Name Query | 98. CSP Deep Analyzer | |
| 47. TTL Analysis | 99. Third-Party Script Risk Profiler | |
| 48. IRR Routing Registry Analyzer | 100. Static Asset Fingerprinter | |
| 49. Dual Stack Diff | 101. Crawl Rules | |
| 50. DNS CAA Checker | 102. Email Config | |
| 51. Decoy DNS Beacon | | |
| 52. Geo IP Spoof Detection | | |

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
