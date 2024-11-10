from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import asyncio
from typing import Optional, List, Dict

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

# Create a client agent
client_agent = Agent(name="client", seed="client_seed_key")

# Fund the client agent if needed
fund_agent_if_low(client_agent.wallet.address())

async def main():
    try:
        # Create the request
        request = AquastatRequest(
            country="Kenya",
            variables=["total_water_withdrawal", "total_population"]
        )
        
        # Replace with actual Aquastat agent address
        aquastat_address = "agent1q..."  
        
        # Send request and wait for response
        async with client_agent:
            await client_agent.start()
            await client_agent.send(aquastat_address, request)
            # Wait for some time to receive the response
            await asyncio.sleep(5)
            await client_agent.stop()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

@client_agent.on_message(model=AquastatResponse)
async def handle_response(ctx: Context, sender: str, msg: AquastatResponse):
    print(f"Received data for {msg.country}")
    print(f"Status: {msg.status}")
    print(f"Data: {msg.data}")

if __name__ == "__main__":
    asyncio.run(main())
    