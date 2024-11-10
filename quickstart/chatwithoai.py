from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from typing import Optional
import asyncio
from queue import Queue
import threading
from datetime import datetime

class Message(Model):
    message: str
    sender: Optional[str]

# Create a queue for sending messages
message_queue = Queue()

# Create the agent
my_agent = Agent(
    name="chat_client",
    port=8000,
    seed="your_seed_phrase",  # Replace with your secure seed phrase
    endpoint=["http://localhost:8000/submit"],
)

# Fund the agent if needed
fund_agent_if_low(my_agent.wallet.address())

OPENAI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

def print_formatted_message(role: str, message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] {role}: {message}")

# Handler for received messages
@my_agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    if sender == OPENAI_AGENT_ADDRESS:
        print_formatted_message("OpenAI Agent", msg.message)
    else:
        print_formatted_message("Unknown Sender", f"{sender}: {msg.message}")
    print("\nYour message (press Enter to send, 'quit' to exit): ", end='', flush=True)

# Message sender that checks the queue
@my_agent.on_interval(period=1.0)
async def send_message(ctx: Context):
    if not message_queue.empty():
        msg_text = message_queue.get()
        print_formatted_message("You", msg_text)
        
        await ctx.send(OPENAI_AGENT_ADDRESS, Message(
            message=msg_text,
            sender=ctx.address
        ))

def get_user_input():
    while True:
        msg = input("\nYour message (press Enter to send, 'quit' to exit): ")
        if msg.lower() == 'quit':
            print("\nExiting chat...")
            break
        if msg.strip():  # Only send non-empty messages
            message_queue.put(msg)

if __name__ == "__main__":
    print("\n=== OpenAI Agent Chat Started ===")
    print(f"Connected to OpenAI Agent: {OPENAI_AGENT_ADDRESS}")
    print("Type your messages and press Enter to send. Type 'quit' to exit.")
    print("Waiting for your message...\n")
    
    # Start the input thread
    input_thread = threading.Thread(target=get_user_input, daemon=True)
    input_thread.start()
    
    # Run the agent
    my_agent.run()