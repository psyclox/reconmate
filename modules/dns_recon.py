import dns.resolver
import whois
from utils.logger import logger

class DNSRecon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}

    def get_dns_records(self):
        logger.info(f"Fetching DNS records for {self.domain}...")
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
        
        for record in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record)
                self.results[record] = [r.to_text() for r in answers]
                logger.info(f"Found {len(answers)} {record} records")
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                logger.error(f"Domain {self.domain} does not exist.")
                return None
            except Exception as e:
                logger.error(f"Error fetching {record}: {str(e)}")
        
        return self.results

    def get_whois_info(self):
        logger.info(f"Performing WHOIS lookup for {self.domain}...")
        try:
            w = whois.whois(self.domain)
            self.results['whois'] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "emails": w.emails
            }
            logger.success("WHOIS lookup completed")
        except Exception as e:
            logger.error(f"WHOIS lookup failed: {str(e)}")
            self.results['whois'] = None
        
        return self.results.get('whois')
