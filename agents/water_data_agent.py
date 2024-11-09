from uagents import Agent, Context, Model, Protocol
from datetime import datetime

class WaterData(Model):
    total_renewable: float
    total_withdrawal: float
    sources: list[dict]  # Changed from List[Dict]
    sectors: list[dict]
    timestamp: str

class WaterAlert(Model):
    level: str
    message: str
    timestamp: str

# Create agent with different port
water_agent = Agent(
    name="kenya_water_monitor",
    port=8000,  # Changed port to avoid conflicts
    endpoint=["http://localhost:8000/submit"],
    seed="kenya_water_monitoring_seed"
)

protocol = Protocol()

@protocol.on_interval(period=60.0)
async def monitor_water_levels(ctx: Context):
    try:
        water_data = WaterData(
            total_renewable=30.7,
            total_withdrawal=3.218,
            sources=[
                {"name": "Surface Water", "value": 2.165},
                {"name": "Groundwater", "value": 0.621},
                {"name": "Wastewater", "value": 0.032}
            ],
            sectors=[
                {"name": "Agriculture", "value": 2.165, "percentage": 67.3},
                {"name": "Industrial", "value": 0.257, "percentage": 8.0},
                {"name": "Municipal", "value": 0.795, "percentage": 24.7}
            ],
            timestamp=datetime.now().isoformat()
        )
        
        ctx.storage.set('latest_data', water_data.dict())
        ctx.logger.info(f"Updated water data: {water_data.dict()}")
        
    except Exception as e:
        ctx.logger.error(f"Monitoring error: {str(e)}")

@protocol.on_message(model=WaterData)
async def handle_water_update(ctx: Context, sender: str, msg: WaterData):
    try:
        ctx.logger.info(f"Received update from {sender}")
        await ctx.send(sender, WaterAlert(
            level="INFO",
            message="Data received",
            timestamp=datetime.now().isoformat()
        ))
    except Exception as e:
        ctx.logger.error(f"Error handling update: {str(e)}")

water_agent.include(protocol)

if __name__ == "__main__":
    print("\n=== Kenya Water Monitoring System ===")
    print(f"Agent Address: {water_agent.address}")
    print(f"Endpoint: http://localhost:8000/submit")
    print("Press Ctrl+C to exit\n")
    water_agent.run()