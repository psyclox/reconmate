import requests
from utils.logger import logger

class SubdomainEnum:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()

    def fetch_from_crtsh(self):
        logger.info(f"Querying crt.sh for subdomains of {self.domain}...")
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name_value = entry['name_value']
                    # Handle multi-line entries
                    subdomains = name_value.split('\n')
                    for sub in subdomains:
                        if "*" not in sub:
                            self.subdomains.add(sub)
                
                logger.success(f"Found {len(self.subdomains)} unique subdomains from crt.sh")
            else:
                logger.error(f"crt.sh returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"Error querying crt.sh: {str(e)}")
            
        return list(self.subdomains)

    def run(self):
        # Placeholder for adding more sources later
        return self.fetch_from_crtsh()
