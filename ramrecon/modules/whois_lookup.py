import sys
import os
import socket
from rich.console import Console
from rich.table import Table
from colorama import Fore, init, Style

from ramrecon.utils.util import clean_domain_input

init(autoreset=True)
console = Console(record=True)

def banner():
    console.print(f"""
{Fore.GREEN}=============================================
        RAMRecon - WHOIS Lookup Module
============================================= {Style.RESET_ALL}
""")

def raw_whois_query(domain, server):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((server, 43))
            s.sendall((domain + "\r\n").encode("utf-8"))
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            return response.decode("utf-8", errors="replace")
    except Exception as e:
        return f"Error: {e}"

def perform_whois_lookup(domain):
    """Perform WHOIS lookup for the given domain using standard TCP socket on port 43."""
    try:
        console.print(f"{Fore.CYAN}[*] Performing WHOIS lookup for domain: {domain}{Style.RESET_ALL}")
        
        # 1. Query IANA to get the correct WHOIS referral server
        iana_res = raw_whois_query(domain, "whois.iana.org")
        if iana_res.startswith("Error:"):
            console.print(f"{Fore.RED}[!] IANA WHOIS lookup failed: {iana_res}{Style.RESET_ALL}")
            return None
        
        refer_server = None
        for line in iana_res.splitlines():
            line_lower = line.lower()
            if line_lower.startswith("refer:") or line_lower.startswith("whois:"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    refer_server = parts[1].strip()
                    break
        
        # 2. Query the referral server if found
        if refer_server:
            if refer_server.startswith("whois://"):
                refer_server = refer_server[8:]
            console.print(f"{Fore.CYAN}[*] Querying referral WHOIS server: {refer_server}{Style.RESET_ALL}")
            refer_res = raw_whois_query(domain, refer_server)
            if not refer_res.startswith("Error:"):
                return refer_res.strip()
        
        # 3. Fallback based on TLD if referral not found/failed
        tld = domain.split(".")[-1].lower()
        fallback_server = f"whois.nic.{tld}"
        if tld in ("com", "net"):
            fallback_server = "whois.verisign-grs.com"
        elif tld == "org":
            fallback_server = "whois.nic.org"
            
        console.print(f"{Fore.CYAN}[*] Querying fallback WHOIS server: {fallback_server}{Style.RESET_ALL}")
        fallback_res = raw_whois_query(domain, fallback_server)
        if not fallback_res.startswith("Error:"):
            return fallback_res.strip()
            
        return iana_res.strip()
    except Exception as e:
        console.print(f"{Fore.RED}[!] WHOIS lookup failed: {e}{Style.RESET_ALL}")
        return None

def display_whois_info(whois_data):
    """Display the WHOIS information in a table format."""
    if not whois_data:
        console.print(f"{Fore.YELLOW}[!] No WHOIS information found.{Style.RESET_ALL}")
        return

    table = Table(show_header=True, header_style="bold white")
    table.add_column("Key", style="white", justify="left", min_width=20)
    table.add_column("Value", style="white", justify="left", min_width=50)

    for line in whois_data.splitlines():
        line = line.strip()
        if not line or line.startswith(("%", "#", ">>>")):
            continue
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key and value:
                table.add_row(key, value)

    console.print(table)
    console.print(f"\n{Fore.CYAN}[*] WHOIS lookup completed.{Style.RESET_ALL}")

def whois_lookup(target):
    """Perform the WHOIS lookup process for the given target."""
    banner()
    domain = clean_domain_input(target)
    whois_data = perform_whois_lookup(domain)
    display_whois_info(whois_data)

def main(target):
    whois_lookup(target)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        try:
            main(target)
            sys.exit(0)  # Explicitly exit with code 0
        except KeyboardInterrupt:
            console.print(f"\n{Fore.RED}[!] Script interrupted by user.{Style.RESET_ALL}")
            sys.exit(0)  # Exit with code 0 to prevent errors in ramrecon.py
        except Exception as e:
            console.print(f"{Fore.RED}[!] An unexpected error occurred: {e}{Style.RESET_ALL}")
            sys.exit(1)  # Exit with code 1 to indicate an error
    else:
        console.print(f"{Fore.RED}[!] No target provided. Please pass a domain or IP address.{Style.RESET_ALL}")
        sys.exit(1)
