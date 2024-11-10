from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import json

# Define message models
class DataUpdate(Model):
    type: str
    data: dict

# Define the data fetcher agent
kenya_data_fetcher = Agent(name="kenya_data_fetcher")
fund_agent_if_low(kenya_data_fetcher.wallet.address())

# Define the visualization agent
data_visualizer = Agent(name="data_visualizer")
fund_agent_if_low(data_visualizer.wallet.address())

# Shared data storage
shared_data = {}

@kenya_data_fetcher.on_interval(period=60.0)  # Fetch every minute
async def fetch_kenya_data(ctx: Context):
    try:
        # Example endpoint - you'll need to replace with actual FAO API endpoint
        api_url = "https://data.apps.fao.org/aquastat/api/v1/key-indicators"
        params = {
            "country": "KEN",
            "year_from": "2000",
            "year_to": "2023"
        }
        
        # Simulated data (replace with actual API call when you have the correct endpoint)
        sample_data = {
            "Total water withdrawal": [3.2, 3.5, 3.8, 4.1],
            "Years": [2000, 2005, 2010, 2015],
            "Agricultural water withdrawal": [2.2, 2.4, 2.6, 2.8]
        }
        
        shared_data["kenya_water_data"] = sample_data
        ctx.logger.info("Successfully fetched Kenya water data")
        
        # Create and send the message using the model
        update_message = DataUpdate(
            type="new_data_available",
            data=sample_data
        )
        await ctx.send(data_visualizer.address, update_message)
        
    except Exception as e:
        ctx.logger.error(f"Error fetching data: {str(e)}")

@data_visualizer.on_message(model=DataUpdate)
async def handle_data_update(ctx: Context, sender: str, msg: DataUpdate):
    try:
        if msg.type == "new_data_available":
            data = msg.data
            
            # Create visualization
            plt.figure(figsize=(10, 6))
            plt.plot(data["Years"], data["Total water withdrawal"], 
                    label="Total withdrawal", marker='o')
            plt.plot(data["Years"], data["Agricultural water withdrawal"], 
                    label="Agricultural withdrawal", marker='s')
            
            plt.title("Kenya Water Withdrawal Trends")
            plt.xlabel("Year")
            plt.ylabel("Water withdrawal (billion m³/year)")
            plt.legend()
            plt.grid(True)
            
            # Save the plot
            plt.savefig('kenya_water_trends.png')
            plt.close()
            
            ctx.logger.info("Successfully created visualization")
            
    except Exception as e:
        ctx.logger.error(f"Error creating visualization: {str(e)}")

# Set up the bureau and add agents
bureau = Bureau()
bureau.add(kenya_data_fetcher)
bureau.add(data_visualizer)

if __name__ == "__main__":
    bureau.run()