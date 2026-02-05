import os
from jinja2 import Environment, FileSystemLoader
from utils.logger import logger

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Simple inline template to avoid extra file dependency for now
        self.template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>AutoRecon Report - {{ domain }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e1e; color: #f0f0f0; margin: 0; padding: 20px; }
        h1, h2 { color: #00ff00; border-bottom: 1px solid #444; padding-bottom: 10px; }
        .section { background: #2d2d2d; padding: 15px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .badge { background: #007acc; padding: 2px 8px; border-radius: 4px; font-size: 0.9em; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #444; }
        th { background: #333; color: #00ff00; }
        a { color: #4db8ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        iframe { width: 100%; height: 600px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>AutoRecon Risk Report: {{ domain }}</h1>
    
    <div class="section">
        <h2>Summary</h2>
        <p><strong>Scan Date:</strong> {{ scan_date }}</p>
        <p><strong>Total Subdomains:</strong> {{ subdomains|length }}</p>
    </div>

    <div class="section">
        <h2>Network Vizualization</h2>
        {% if graph_path %}
        <iframe src="{{ graph_path }}"></iframe>
        {% else %}
        <p>No graph generated.</p>
        {% endif %}
    </div>

    <div class="section">
        <h2>DNS Records</h2>
        {% if dns_records %}
        <table>
            <tr><th>Type</th><th>Value</th></tr>
            {% for type, records in dns_records.items() %}
                {% if type != 'whois' %}
                    {% for r in records %}
                    <tr><td>{{ type }}</td><td>{{ r }}</td></tr>
                    {% endfor %}
                {% endif %}
            {% endfor %}
        </table>
        {% else %}
        <p>No DNS records found.</p>
        {% endif %}
    </div>

    <div class="section">
        <h2>Subdomains</h2>
        <ul>
        {% for sub in subdomains %}
            <li>{{ sub }}</li>
        {% endfor %}
        </ul>
    </div>

    <div class="section">
        <h2>Port Scan Results</h2>
        {% if port_data %}
            {% for host, protocols in port_data.items() %}
            <h3>Host: {{ host }}</h3>
            <table>
                <tr><th>Port</th><th>State</th><th>Service</th><th>Version</th></tr>
                {% for proto, ports in protocols.items() %}
                    {% for p in ports %}
                    <tr>
                        <td>{{ p.port }}/{{ proto }}</td>
                        <td><span class="{{ 'badge' if p.state == 'open' else '' }}">{{ p.state }}</span></td>
                        <td>{{ p.service }}</td>
                        <td>{{ p.version }}</td>
                    </tr>
                    {% endfor %}
                {% endfor %}
            </table>
            {% endfor %}
        {% else %}
        <p>No open ports found or scan skipped.</p>
        {% endif %}
    </div>
    
    <div class="section">
        <h2>Shodan Intelligence</h2>
        {% if shodan_data %}
        <p><strong>Organization:</strong> {{ shodan_data.org }}</p>
        <p><strong>OS:</strong> {{ shodan_data.os }}</p>
        <p><strong>Vulnerabilities:</strong> {{ shodan_data.vulns|join(', ') }}</p>
        {% else %}
        <p>No Shodan data available.</p>
        {% endif %}
    </div>

</body>
</html>
"""

    def generate_html(self, data):
        logger.info("Generating HTML report...")
        domain = data.get('domain')
        
        try:
            env = Environment()
            template = env.from_string(self.template_str)
            html_out = template.render(**data)
            
            output_file = os.path.join(self.output_dir, f"{domain}_report.html")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_out)
            
            logger.success(f"Report generated successfully: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return None
