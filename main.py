import argparse
import sys
import socket
from datetime import datetime
from colorama import Fore, Style

from config import Config
from utils.logger import logger
from utils.validators import validate_target, extract_domain
from modules.dns_recon import DNSRecon
from modules.subdomain_enum import SubdomainEnum
from modules.port_scan import PortScanner
from modules.shodan_scan import ShodanScanner
from reporting.graph_viz import GraphVisualizer
from reporting.report_generator import ReportGenerator

def banner():
    print(Fore.CYAN + r"""
    ____                      __  __       _       
   |  _ \ ___  ___ ___  _ __ |  \/  | __ _| |_ ___ 
   | |_) / _ \/ __/ _ \| '_ \| |\/| |/ _` | __/ _ \
   |  _ <  __/ (_| (_) | | | | |  | | (_| | ||  __/
   |_| \_\___|\___\___/|_| |_|_|  |_|\__,_|\__\___|
                                                   
    ReconMate - Automated OSINT & Recon Tool | v1.0
    """ + Style.RESET_ALL)

def resolve_ip(target):
    try:
        return socket.gethostbyname(target)
    except:
        return None

def main():
    banner()
    parser = argparse.ArgumentParser(description="ReconMate - Professional OSINT & Recon Tool")
    parser.add_argument("-t", "--target", required=True, help="Target Domain or IP")
    parser.add_argument("--ports", default="1-1000", help="Port range to scan (default: 1-1000)")
    parser.add_argument("--no-shodan", action="store_true", help="Skip Shodan scan")
    parser.add_argument("--no-subdomains", action="store_true", help="Skip subdomain enumeration")
    
    args = parser.parse_args()
    
    # Validation
    raw_target = args.target
    target_type = validate_target(raw_target)
    
    if not target_type:
        logger.error("Invalid target specified. Please provide a valid Domain or IP.")
        sys.exit(1)

    domain = extract_domain(raw_target) if target_type == 'domain' else raw_target
    target_ip = resolve_ip(domain)
    
    logger.info(f"Starting scan against: {domain} ({target_ip})")
    start_time = datetime.now()

    # Data Collection
    scan_data = {
        "domain": domain,
        "target_ip": target_ip,
        "scan_date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "dns_records": {},
        "subdomains": [],
        "port_data": {},
        "shodan_data": {},
        "graph_path": None
    }

    # 1. DNS Recon
    if target_type == 'domain':
        dns_module = DNSRecon(domain)
        scan_data['dns_records'] = dns_module.get_dns_records()
        scan_data['dns_records']['whois'] = dns_module.get_whois_info()

    # 2. Subdomain Enumeration
    if target_type == 'domain' and not args.no_subdomains:
        sub_module = SubdomainEnum(domain)
        scan_data['subdomains'] = sub_module.run()
        scan_data['subdomains'].append(domain) # Ensure main domain is in list
    else:
        scan_data['subdomains'] = [domain]

    # 3. Port Scanning
    # For efficiency, we scan the main target IP. 
    # In a full VAPT, we might iterate over all subdomains.
    if target_ip:
        scanner = PortScanner(target_ip)
        scan_data['port_data'] = scanner.run_scan(ports=args.ports)

    # 4. Shodan Scan
    if target_ip and not args.no_shodan:
        shodan_module = ShodanScanner(target_ip)
        scan_data['shodan_data'] = shodan_module.run_scan()

    # 5. Visualization
    viz = GraphVisualizer()
    scan_data['graph_path'] = viz.generate_graph(
        domain, 
        scan_data['dns_records'], 
        scan_data['subdomains'], 
        scan_data['port_data'], 
        scan_data['shodan_data']
    )

    # 6. Reporting
    reporter = ReportGenerator()
    report_path = reporter.generate_html(scan_data)

    end_time = datetime.now()
    duration = end_time - start_time
    
    print("-" * 50)
    logger.success(f"Scan completed in {duration}")
    if report_path:
        logger.info(f"Report available at: {report_path}")
    if scan_data['graph_path']:
        logger.info(f"Graph available at: {scan_data['graph_path']}")
    print("-" * 50)

if __name__ == "__main__":
    main()
