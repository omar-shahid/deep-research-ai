import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

# 🌿 Load environment variables and disable tracing
load_dotenv()
set_tracing_disabled(disabled=True)

# 🔐 Setup clients
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)

# 🧠 Define the LLM model for our agents
llm_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
