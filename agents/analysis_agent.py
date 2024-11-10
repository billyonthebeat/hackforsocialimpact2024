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
    seed="data_retrieval_seed"  # Add a seed for deterministic address generation
)

@data_protocol.on_interval(period=agent_config['interval'])
async def fetch_data(ctx: Context):
    try:
        # Get data from different sources
        nasa_data = await get_nasa_data()
        earth_engine_data = await get_earth_engine_data()
        sentinel_data = await get_sentinel_data()
        
        # Prepare the message
        raw_data = RawData(
            temporal_data=nasa_data.to_dict(),
            spatial_data=earth_engine_data.to_dict(),
            vegetation_data=sentinel_data.to_dict()
        )
        
        # Send to analysis agent
        analysis_address = os.getenv('ANALYSIS_AGENT_ADDRESS')
        if analysis_address:
            ctx.logger.info(f"Sending data to analysis agent at {analysis_address}")
            await ctx.send(analysis_address, raw_data)
        else:
            ctx.logger.error("Analysis agent address not found")
        
    except Exception as e:
        ctx.logger.error(f"Error in data retrieval: {str(e)}")

async def get_nasa_data():
    """Retrieve data from NASA Worldview (simulated)"""
    config = agent_config['data_sources']['nasa_worldview']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=config['data_period_days'])
    
    return pd.DataFrame({
        'date': pd.date_range(start_date, end_date),
        'temperature': np.random.normal(25, 5, config['data_period_days'] + 1),
        'vegetation_index': np.random.uniform(0.3, 0.8, config['data_period_days'] + 1)
    })

async def get_earth_engine_data():
    """Retrieve data from Earth Engine (simulated)"""
    config = agent_config['data_sources']['earth_engine']
    return pd.DataFrame({
        'location': [f'Region_{i}' for i in range(config['region_count'])],
        'land_use': np.random.choice(['forest', 'urban', 'agriculture'], config['region_count']),
        'area': np.random.uniform(100, 1000, config['region_count'])
    })

async def get_sentinel_data():
    """Retrieve data from Sentinel Hub (simulated)"""
    config = agent_config['data_sources']['sentinel']
    return pd.DataFrame({
        'coordinates': [(lat, lon) for lat, lon in zip(
            np.random.uniform(30, 50, config['sample_points']),
            np.random.uniform(-100, -80, config['sample_points'])
        )],
        'ndvi': np.random.uniform(0.2, 0.9, config['sample_points'])
    })

# Include the protocol in the agent
agent.include(data_protocol)