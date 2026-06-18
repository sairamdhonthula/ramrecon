import os
import sys
import requests
from rich.console import Console
from rich.table import Table
from colorama import Fore, init


from ramrecon.config.settings import DEFAULT_TIMEOUT  
from ramrecon.utils.util import validate_ip, resolve_to_ip, clean_domain_input  


init(autoreset=True)
console = Console(record=True)

def banner():
    console.print(Fore.GREEN + """
    =============================================
           RAMRecon - Server Location Detection
    =============================================
    """)

def get_server_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=DEFAULT_TIMEOUT)
        data = response.json()
        if data['status'] == 'success':
            return data
        return None
    except requests.RequestException as e:
        console.print(Fore.RED + f"[!] Error retrieving server location: {e}")
        return None

def display_server_location(location_data):
    isp = location_data.get('isp', '')
    org = location_data.get('org', '')
    as_info = location_data.get('as', '')
    is_cdn = any(cdn in s.lower() for s in (isp, org, as_info) for cdn in ("cloudflare", "cloudfront", "fastly", "akamai", "sucuri", "incapsula"))
    if is_cdn:
        console.print(f"{Fore.YELLOW}[!] Note: Target IP is behind a CDN/Proxy ({isp or org}). The geolocation\n"
                      f"    information below represents the proxy edge server and not the actual origin host.\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan", justify="left")
    table.add_column("Details", style="green")

    for key, value in location_data.items():
        table.add_row(str(key), str(value))

    console.print(table)

def main(target):
    banner()

    target = clean_domain_input(target)
    ip = target
    if not validate_ip(ip):
        console.print(Fore.YELLOW + f"[!] '{target}' is not a valid IP address, attempting to resolve to an IP...")
        ip = resolve_to_ip(target)
        if not ip:
            console.print(Fore.RED + "[!] Invalid IP address or unable to resolve domain. Please check the input.")
            return
        console.print(Fore.GREEN + f"[+] Resolved domain '{target}' to IP: {ip}")

    console.print(Fore.WHITE + f"[*] Fetching server location for: {ip}")
    location_info = get_server_location(ip)
    if location_info:
        display_server_location(location_info)
    else:
        console.print(Fore.RED + "[!] No server location information found.")
    console.print(Fore.WHITE + "[*] Server location detection completed.")

if len(sys.argv) > 1:
    target = sys.argv[1]
    try:
        main(target)
    except KeyboardInterrupt:
        console.print(Fore.RED + "\n[!] Process interrupted by user.")
        sys.exit(1)
else:
    console.print(Fore.RED + "[!] No target provided. Please pass an IP address.")
    sys.exit(1)
