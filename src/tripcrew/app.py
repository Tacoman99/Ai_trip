import chainlit as cl
from main import dacrew


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

    # Makes crew function async due to how long it takes to run
    da_message = await cl.make_async(dacrew)(message.content)

    await cl.Message(
        content=da_message.raw
    ).send()