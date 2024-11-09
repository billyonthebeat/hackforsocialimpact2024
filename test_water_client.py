from uagents import Agent, Context, Model
from datetime import datetime

class WaterData(Model):
    total_renewable: float
    total_withdrawal: float
    sources: list[dict]  # Fixed typing
    sectors: list[dict]  # Fixed typing
    timestamp: str

class WaterAlert(Model):
    level: str
    message: str
    timestamp: str

# Create test client with different port
test_client = Agent(
    name="test_client",
    port=8011,  # Different port
    endpoint=["http://localhost:8011/submit"],
    seed="test_client_seed"
)

@test_client.on_interval(period=30.0)
async def send_test_data(ctx: Context):
    try:
        # Update this with your water agent's address
        WATER_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
        
        test_data = WaterData(
            total_renewable=25.5,
            total_withdrawal=3.0,
            sources=[{"name": "Test Source", "value": 1.0}],
            sectors=[{"name": "Test Sector", "value": 1.0, "percentage": 50.0}],
            timestamp=datetime.now().isoformat()
        )
        
        await ctx.send(WATER_AGENT_ADDRESS, test_data)
        ctx.logger.info("Test data sent successfully")
        
    except Exception as e:
        ctx.logger.error(f"Error sending test data: {str(e)}")

@test_client.on_message(model=WaterAlert)
async def handle_response(ctx: Context, sender: str, msg: WaterAlert):
    ctx.logger.info(f"Received response: {msg.dict()}")

if __name__ == "__main__":
    print("\n=== Water Monitoring Test Client ===")
    print(f"Client Address: {test_client.address}")
    print(f"Endpoint: http://localhost:8011/submit")
    print("Sending test data every 30 seconds")
    print("Press Ctrl+C to exit\n")
    test_client.run()