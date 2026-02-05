import socket
import validators
from urllib.parse import urlparse

def validate_target(target):
    """
    Validates if the target is a valid IP or Domain.
    Returns: 'ip', 'domain', or None
    """
    if validators.domain(target):
        return 'domain'
    
    try:
        socket.inet_aton(target)
        return 'ip'
    except socket.error:
        pass

    return None

def extract_domain(url):
    """
    Extracts domain from a URL if user provides http://...
    """
    if "://" in url:
        parsed = urlparse(url)
        return parsed.netloc
    return url
