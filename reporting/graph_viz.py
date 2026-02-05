from pyvis.network import Network
import os
from utils.logger import logger

class GraphVisualizer:
    def __init__(self, output_dir="reports"):
        self.net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_graph(self, domain, dns_data, subdomains, port_data, shodan_data):
        logger.info("Generating network graph...")
        
        # Add Main Domain Node
        self.net.add_node(domain, label=domain, color="red", title="Target Domain")

        # Add Subdomains
        for sub in subdomains:
            self.net.add_node(sub, label=sub, color="orange", size=15)
            self.net.add_edge(domain, sub)

        # Add DNS Records
        if dns_data:
            for r_type, records in dns_data.items():
                if r_type == 'whois': continue
                for record in records:
                    node_id = f"{r_type}:{record}"
                    self.net.add_node(node_id, label=record, color="blue", title=r_type, size=10)
                    self.net.add_edge(domain, node_id)

        # Add Ports (Attached to IP nodes usually, but attaching to domain/sub for simplicity in this view)
        # Assuming port_data structure is {host_ip: {protocol: [ports...]}}
        if port_data:
            for host, protocols in port_data.items():
                self.net.add_node(host, label=host, color="green", title="Host IP")
                self.net.add_edge(domain, host)
                
                for proto, ports in protocols.items():
                    for p in ports:
                        port_label = f"{p['port']}/{p['service']}"
                        self.net.add_node(port_label, label=port_label, color="purple", size=8)
                        self.net.add_edge(host, port_label)

        # Output
        output_path = os.path.join(self.output_dir, f"{domain}_graph.html")
        
        # Set physics for better layout
        self.net.barnes_hut()
        
        try:
            self.net.save_graph(output_path)
            logger.success(f"Graph generated at {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate graph: {str(e)}")
            return None
