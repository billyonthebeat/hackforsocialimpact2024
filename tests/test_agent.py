from agents.water_data_agent import water_agent
import asyncio

async def test_water_monitoring():
    print(f"Testing Water Monitoring Agent")
    print(f"Agent address: {water_agent.address}")
    
    # Wait for some monitoring cycles
    await asyncio.sleep(180)  # Wait 3 minutes

if __name__ == "__main__":
    asyncio.run(test_water_monitoring())