# ReconMate 🛡️

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**ReconMate** is a professional-grade, automated OSINT & Reconnaissance tool designed for cybersecurity analysts and penetration testers. It streamlines the initial phase of security assessments by automating DNS enumeration, subdomain discovery, port scanning, and threat intelligence gathering.

---

## 🚀 Features

-   **🔍 target Validation**: Smartly distinguishes between Domains and IPs.
-   **🌐 DNS Reconnaissance**:
    -   Retrieves `A`, `AAAA`, `MX`, `NS`, `TXT` records.
    -   Performs automatic WHOIS lookups.
-   **🔎 Subdomain Enumeration**:
    -   Integrates with **crt.sh** for passive certificate transparency log analysis.
-   **📡 Advanced Port Scanning**:
    -   Powered by **Nmap** for reliable service and version detection.
    -   Multi-threaded scanning for efficiency.
-   **🌍 Shodan Intelligence**:
    -   Queries **Shodan API** for organization details, OS fingerprinting, and known vulnerabilities (CVEs).
-   **🕸️ Network Visualization**:
    -   Generates interactive interactive graphs to map attack surfaces.
-   **📊 Professional Reporting**:
    -   Produces comprehensive HTML reports with risk summaries and data tables.

---

## 🛠️ Installation

### Prerequisites

-   **Python 3.8+**
-   **Nmap** (Must be installed and in your system PATH)

### Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/ReconMate.git
    cd ReconMate
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys**
    Open `config.py` and add your Shodan API Key:
    ```python
    class Config:
        SHODAN_API_KEY = "YOUR_SHODAN_API_KEY_HERE"
    ```

---

## 💻 Usage

Run ReconMate simply by pointing it to your target.

### Basic Scan
```bash
python main.py -t example.com
```

### Scan with Custom Port Range
```bash
python main.py -t 192.168.1.5 --ports "20-80,443,8080"
```

### Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `-t`, `--target` | Target Domain or IP address (Required) | N/A |
| `--ports` | Specific ports to scan | `1-1000` |
| `--no-shodan` | Skip Shodan intelligence lookup | `False` |
| `--no-subdomains` | Skip subdomain enumeration | `False` |

---

## 📊 Sample Output

```text
    ____                      __  __       _       
   |  _ \ ___  ___ ___  _ __ |  \/  | __ _| |_ ___ 
   | |_) / _ \/ __/ _ \| '_ \| |\/| |/ _` | __/ _ \
   |  _ <  __/ (_| (_) | | | | |  | | (_| | ||  __/
   |_| \_\___|\___\___/|_| |_|_|  |_|\__,_|\__\___|
                                                   
    ReconMate - Automated OSINT & Recon Tool | v1.0

[+] Starting scan against: example.com (93.184.216.34)
[+] DNS Records found: A, MX, TXT...
[+] Found 15 unique subdomains from crt.sh
[+] Port scan completed. Open ports: 80, 443
[+] Shodan scan completed. Org: EDGECAST
[-] Report generated successfully: reports/example.com_report.html
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Disclaimer: ReconMate is intended for educational and authorized testing purposes only. The developers assume no liability for misuse.*
