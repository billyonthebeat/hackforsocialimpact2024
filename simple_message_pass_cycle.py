from uagents import Agent, Bureau, Context, Model
import time

class Message(Model):
    value: int

# Create four agents
agent1 = Agent(name="agent1", seed="agent1 seed")
agent2 = Agent(name="agent2", seed="agent2 seed")
agent3 = Agent(name="agent3", seed="agent3 seed")
agent4 = Agent(name="agent4", seed="agent4 seed")

# Agent 1 function
@agent1.on_interval(period=1.0)
async def agent1_monitor(ctx: Context):
    ctx.logger.info(f"Agent 1 monitoring every second ! - starting the cycle")
    initial_value = 0
    await ctx.send(agent2.address, Message(value=initial_value))



# Agent 2 function
@agent2.on_message(model=Message)
async def agent2_function(ctx: Context, sender: str, msg: Message):
    new_value = msg.value + 1
    ctx.logger.info(f"Agent 2 received: {msg.value}, sending: {new_value}")
    await ctx.send(agent3.address, Message(value=new_value))

# Agent 3 function
@agent3.on_message(model=Message)
async def agent3_function(ctx: Context, sender: str, msg: Message):
    new_value = msg.value + 1
    ctx.logger.info(f"Agent 3 received: {msg.value}, sending: {new_value}")
    await ctx.send(agent4.address, Message(value=new_value))

# Agent 4 function
@agent4.on_message(model=Message)
async def agent4_function(ctx: Context, sender: str, msg: Message):
    new_value = msg.value + 1
    ctx.logger.info(f"Agent 4 received: {msg.value}, final value: {new_value}")
    await ctx.send(agent2.address, Message(value=new_value))

# Create a bureau and add all agents
bureau = Bureau()
bureau.add(agent1)
bureau.add(agent2)
bureau.add(agent3)
bureau.add(agent4)

# Run the bureau
if __name__ == "__main__":
    bureau.run()
