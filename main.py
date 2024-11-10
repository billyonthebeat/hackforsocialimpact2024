from uagents import Bureau
from agents import data_retrieval_agent, analysis_agent, visualization_agent
from utils.config_loader import setup_environment, get_available_port, load_config
import os
import time
from datetime import datetime

def print_status_message():
    print("\n=== System Status ===")
    print("✓ Data Retrieval Agent is collecting data")
    print("✓ Analysis Agent is processing")
    print("✓ Visualization Agent is generating visuals")
    print("\nCheck 'visualizations/' directory for output files")
    print("Run 'python view_visualizations.py' in another terminal to auto-open visuals")
    print("\nPress Ctrl+C to stop the system")

def main():
    # Setup environment and load configuration
    setup_environment()
    config = load_config()
    
    # Get available port
    port = get_available_port(config['bureau']['base_port'])
    
    # Create and start the bureau
    bureau = Bureau(
        port=port,
        endpoint=[f"http://{config['bureau']['host']}:{port}/submit"]
    )
    
    # Add agents to the bureau
    bureau.add(data_retrieval_agent)
    bureau.add(analysis_agent)
    bureau.add(visualization_agent)
    
    # Store agent addresses in environment
    os.environ['ANALYSIS_AGENT_ADDRESS'] = analysis_agent.address
    os.environ['VISUALIZATION_AGENT_ADDRESS'] = visualization_agent.address
    
    # Print system information
    print("\n=== Geospatial Analysis System ===")
    print(f"\nBureau Status:")
    print(f"- Running on: http://{config['bureau']['host']}:{port}")
    print(f"- Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"- Data Collection Interval: {config['agents']['data_retrieval']['interval']} seconds")
    
    print("\nAgent Addresses:")
    print(f"- Data Retrieval: {data_retrieval_agent.address}")
    print(f"- Analysis: {analysis_agent.address}")
    print(f"- Visualization: {visualization_agent.address}")
    
    print_status_message()
    
    # Run the bureau
    try:
        bureau.run()
    except KeyboardInterrupt:
        print("\nShutting down the system...")

if __name__ == "__main__":
    main()