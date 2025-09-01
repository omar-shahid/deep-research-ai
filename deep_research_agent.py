import chainlit as cl
from agents import Runner
from src.main_agent import orchestrator_agent


@cl.on_message
async def main(message: cl.Message):
    result_complex = await Runner.run(orchestrator_agent, message.content)
    await cl.Message(content=result_complex.final_output).send()
