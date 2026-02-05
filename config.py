import os

class Config:
    # SHODAN API KEY
    # Default to environment variable for security, or placeholder
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "YOUR_SHODAN_API_KEY_HERE")

    # SCANNING CONFIG
    DNS_RESOLVERS = ["1.1.1.1", "8.8.8.8"]
    
    # OUTPUT
    OUTPUT_DIR = "reports"
    
    # THREADS
    MAX_THREADS = 10
