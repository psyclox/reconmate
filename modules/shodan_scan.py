import shodan
from config import Config
from utils.logger import logger

class ShodanScanner:
    def __init__(self, ip_address):
        self.ip = ip_address
        self.api_key = Config.SHODAN_API_KEY
        self.api = None
        self.results = {}

    def run_scan(self):
        if not self.api_key or "YOUR_SHODAN_API_KEY" in self.api_key:
            logger.warning("Shodan API key is not configured. Skipping Shodan scan.")
            return None

        try:
            self.api = shodan.Shodan(self.api_key)
            logger.info(f"Querying Shodan for IP: {self.ip}...")
            
            host = self.api.host(self.ip)
            
            self.results = {
                "org": host.get('org', 'n/a'),
                "os": host.get('os', 'n/a'),
                "ports": host.get('ports', []),
                "vulns": host.get('vulns', []),
                "hostnames": host.get('hostnames', [])
            }
            
            logger.success(f"Shodan scan completed. Found information for {self.results['org']}")
            return self.results

        except shodan.APIError as e:
            logger.error(f"Shodan API Error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Shodan scan failed: {str(e)}")
            return None
