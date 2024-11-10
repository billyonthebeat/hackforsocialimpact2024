from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from utils.config_loader import load_config

# Define message models
class RawData(Model):
    temporal_data: Dict[str, Any]
    spatial_data: Dict[str, Any]
    vegetation_data: Dict[str, Any]

# Load configuration
config = load_config()
agent_config = config['agents']['data_retrieval']

# Create protocol for handling messages
data_protocol = Protocol()

# Create the agent
agent = Agent(
    name=agent_config['name'],
    seed="data_retrieval_seed"
)

@data_protocol.on_interval(period=30)  # Set to 30 seconds for testing
async def fetch_data(ctx: Context):
    try:
        print("\n=== Data Retrieval Started ===")
        
        # Get data from different sources
        print("Fetching NASA data...")
        nasa_data = await get_nasa_data()
        
        print("Fetching Earth Engine data...")
        earth_engine_data = await get_earth_engine_data()
        
        print("Fetching Sentinel data...")
        sentinel_data = await get_sentinel_data()
        
        # Prepare the message
        print("Preparing data message...")
        raw_data = RawData(
            temporal_data=nasa_data.to_dict(),
            spatial_data=earth_engine_data.to_dict(),
            vegetation_data=sentinel_data.to_dict()
        )
        
        # Send to analysis agent
        analysis_address = os.getenv('ANALYSIS_AGENT_ADDRESS')
        if analysis_address:
            print(f"Sending data to analysis agent at {analysis_address}")
            await ctx.send(analysis_address, raw_data)
            print("Data sent successfully")
        else:
            print("ERROR: Analysis agent address not found!")
        
    except Exception as e:
        print(f"ERROR in data retrieval: {str(e)}")
        raise

async def get_nasa_data():
    """Retrieve data from NASA Worldview (simulated)"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    df = pd.DataFrame({
        'date': pd.date_range(start_date, end_date),
        'temperature': np.random.normal(25, 5, 31),
        'vegetation_index': np.random.uniform(0.3, 0.8, 31)
    })
    print(f"Generated NASA data with {len(df)} records")
    return df

async def get_earth_engine_data():
    """Retrieve data from Earth Engine (simulated)"""
    df = pd.DataFrame({
        'location': [f'Region_{i}' for i in range(10)],
        'land_use': np.random.choice(['forest', 'urban', 'agriculture'], 10),
        'area': np.random.uniform(100, 1000, 10)
    })
    print(f"Generated Earth Engine data with {len(df)} records")
    return df

async def get_sentinel_data():
    """Retrieve data from Sentinel Hub (simulated)"""
    df = pd.DataFrame({
        'coordinates': [(lat, lon) for lat, lon in zip(
            np.random.uniform(30, 50, 20),
            np.random.uniform(-100, -80, 20)
        )],
        'ndvi': np.random.uniform(0.2, 0.9, 20)
    })
    print(f"Generated Sentinel data with {len(df)} records")
    return df

# Include the protocol in the agent
agent.include(data_protocol)

print("Data Retrieval Agent initialized successfully")