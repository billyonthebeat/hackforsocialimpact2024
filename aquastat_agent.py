from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
import pandas as pd
from typing import Optional, List, Dict
import datetime

# Define message models
class AquastatRequest(Model):
    country: str
    variables: Optional[List[str]] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class AquastatResponse(Model):
    country: str
    data: Dict
    timestamp: str
    status: str

# Create the Aquastat Agent
aquastat_agent = Agent(
    name="aquastat_agent",
    seed="aquastat_agent_seed_key"
)

# Fund the agent if needed
fund_agent_if_low(aquastat_agent.wallet.address())

# Helper function to fetch data from AQUASTAT
async def fetch_aquastat_data(country: str, variables: List[str] = None) -> Dict:
    # Base URL for AQUASTAT API
    base_url = "https://data.apps.fao.org/aquastat/api/v1/data"
    
    # Build query parameters
    params = {
        "country": country,
        "format": "json"
    }
    
    if variables:
        params["variables"] = ",".join(variables)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

# Message handler for data requests
@aquastat_agent.on_message(model=AquastatRequest)
async def handle_request(ctx: Context, sender: str, msg: AquastatRequest):
    ctx.logger.info(f"Received request for {msg.country} data")
    
    try:
        # Fetch data from AQUASTAT
        data = await fetch_aquastat_data(
            country=msg.country,
            variables=msg.variables
        )
        
        # Prepare response
        response = AquastatResponse(
            country=msg.country,
            data=data,
            timestamp=datetime.datetime.now().isoformat(),
            status="success"
        )
        
    except Exception as e:
        response = AquastatResponse(
            country=msg.country,
            data={},
            timestamp=datetime.datetime.now().isoformat(),
            status=f"error: {str(e)}"
        )
    
    # Send response back
    await ctx.send(sender, response)

# Periodic task to check data updates
@aquastat_agent.on_interval(period=3600.0)  # Check every hour
async def check_updates(ctx: Context):
    ctx.logger.info("Checking for AQUASTAT data updates...")
    try:
        # Fetch latest data for Kenya
        data = await fetch_aquastat_data("Kenya")
        
        # Store or process the data as needed
        ctx.storage.set("latest_kenya_data", data)
        
        ctx.logger.info("Successfully updated Kenya data")
    except Exception as e:
        ctx.logger.error(f"Error updating data: {str(e)}")

# Main execution
if __name__ == "__main__":
    aquastat_agent.run()
