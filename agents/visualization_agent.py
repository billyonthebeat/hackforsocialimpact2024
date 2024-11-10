from uagents import Agent, Context, Model, Protocol
from typing import Dict, Any
import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
from utils.config_loader import load_config

class AnalyzedData(Model):
    temporal_analysis: Dict[str, Any]
    spatial_analysis: Dict[str, Any]
    vegetation_analysis: Dict[str, Any]
    raw_data: Dict[str, Any]

# Load configuration
config = load_config()
agent_config = config['agents']['visualization']

# Create protocol for handling messages
viz_protocol = Protocol()

# Create the agent
agent = Agent(
    name=agent_config['name'],
    seed="visualization_seed"  # Add a seed for deterministic address generation
)

# Initialize output directory
output_dir = agent_config['output_dir']
os.makedirs(output_dir, exist_ok=True)

@viz_protocol.on_message(model=AnalyzedData)
async def handle_analyzed_data(ctx: Context, sender: str, msg: AnalyzedData):
    try:
        # Create visualizations
        create_visualizations(msg)
        ctx.logger.info("Visualizations created successfully")
    except Exception as e:
        ctx.logger.error(f"Error in visualization: {str(e)}")

def create_visualizations(data: AnalyzedData):
    """Create all visualizations from analyzed data"""
    # Convert raw data back to DataFrames
    temporal_df = pd.DataFrame.from_dict(data.raw_data['temporal_data'])
    spatial_df = pd.DataFrame.from_dict(data.raw_data['spatial_data'])
    vegetation_df = pd.DataFrame.from_dict(data.raw_data['vegetation_data'])

    # Create individual visualizations
    create_map_visualization(vegetation_df, data.vegetation_analysis)
    create_trend_visualization(temporal_df, data.temporal_analysis)
    create_vegetation_visualization(data.vegetation_analysis)

def create_map_visualization(veg_df: pd.DataFrame, analysis: Dict):
    """Create map visualization with NDVI points"""
    map_settings = agent_config['map_settings']
    m = folium.Map(location=map_settings['center'], zoom_start=map_settings['zoom'])
    
    for idx, row in veg_df.iterrows():
        lat, lon = row['coordinates']
        ndvi = row['ndvi']
        color = get_ndvi_color(ndvi)
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            popup=f'NDVI: {ndvi:.2f}'
        ).add_to(m)
    
    m.save(os.path.join(output_dir, 'vegetation_map.html'))

def create_trend_visualization(temporal_df: pd.DataFrame, analysis: Dict):
    """Create temporal trend visualizations"""
    fig = make_subplots(rows=2, cols=1)
    
    # Temperature trend
    fig.add_trace(
        go.Scatter(
            x=temporal_df['date'],
            y=temporal_df['temperature'],
            name='Temperature'
        ),
        row=1, col=1
    )
    
    # Monthly averages
    months = list(analysis['seasonality']['monthly_avg'].keys())
    averages = list(analysis['seasonality']['monthly_avg'].values())
    
    fig.add_trace(
        go.Bar(x=months, y=averages, name='Monthly Average'),
        row=2, col=1
    )
    
    fig.update_layout(height=800, title_text="Temporal Analysis")
    fig.write_html(os.path.join(output_dir, 'temporal_analysis.html'))

def create_vegetation_visualization(analysis: Dict):
    """Create vegetation distribution visualization"""
    fig = px.pie(
        values=list(analysis['ndvi_zones'].values()),
        names=list(analysis['ndvi_zones'].keys()),
        title='NDVI Zone Distribution'
    )
    
    fig.write_html(os.path.join(output_dir, 'vegetation_distribution.html'))

def get_ndvi_color(ndvi: float) -> str:
    """Get color for NDVI value"""
    colors = agent_config['ndvi_colors']
    if ndvi < 0.2: return colors['low']
    elif ndvi < 0.4: return colors['medium_low']
    elif ndvi < 0.6: return colors['medium_high']
    else: return colors['high']

# Include the protocol in the agent
agent.include(viz_protocol)