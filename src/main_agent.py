from agents import  Agent, StopAtTools
from src.tools.index import comprehensive_research 
from src.config import llm_model

orchestrator_agent = Agent(
    name="MainAssistant",
    instructions=(
        "You are a helpful assistant.\n"
        "- If the user asks something simple, answer directly.\n"
        "- If the question requires in-depth research, Use the tools provided, do not write it yourself.\n"
    ),
    model=llm_model,
    tools=[comprehensive_research],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["comprehensive_research"])
)
