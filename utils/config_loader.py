import yaml
import os
from dotenv import load_dotenv
import socket

def load_config():
    """Load configuration from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_available_port(start_port=8000):
    """Get an available port starting from the specified port."""
    port = start_port
    while port < start_port + 1000:  # Try up to 1000 ports
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise RuntimeError("No available ports found")

def setup_environment():
    """Setup environment variables and create necessary directories."""
    # Load environment variables
    load_dotenv()
    
    # Create necessary directories
    dirs = ['visualizations', 'data']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)