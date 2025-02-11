import chainlit as cl
from tripcrew.main import dacrew

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"""
        Welcome to the trip crew! I'm here to help you plan your next adventure. 
        How can I assist you today?
        """
    ).send()


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    da_message = message.content +' ' + 'I am a trip planner'

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {da_message}",
        ).send()



if __name__ == "__main__":
    main()
