import nmap
from utils.logger import logger

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.nm = nmap.PortScanner()
        self.results = {}

    def run_scan(self, ports="1-1000"):
        logger.info(f"Starting port scan on {self.target} (Ports: {ports})...")
        try:
            # -sV for version detection, -T4 for faster execution
            # Note: SYN scan (-sS) requires root privileges
            self.nm.scan(self.target, ports, arguments='-sV -T4')
            
            for host in self.nm.all_hosts():
                logger.info(f"Host: {host} ({self.nm[host].hostname()})")
                logger.info(f"State: {self.nm[host].state()}")
                
                self.results[host] = {}
                
                for proto in self.nm[host].all_protocols():
                    logger.info(f"Protocol: {proto}")
                    ports_data = []
                    lport = self.nm[host][proto].keys()
                    for port in lport:
                        service = self.nm[host][proto][port]
                        state = service['state']
                        name = service['name']
                        version = service['version']
                        logger.info(f"Port: {port}\tState: {state}\tService: {name} {version}")
                        ports_data.append({
                            "port": port,
                            "state": state,
                            "service": name,
                            "version": version
                        })
                    self.results[host][proto] = ports_data
                    
            logger.success("Port scan completed.")
        except nmap.PortScannerError as e:
            logger.error(f"Nmap error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during scan: {str(e)}")
            
        return self.results
