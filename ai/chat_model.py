from langchain.chat_models import init_chat_model
from tools import TOOLS

from config.settings import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_BASE
)

chat_model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_BASE,
    temperature=0.7
)

# 绑定tools
chat_model_with_tools = chat_model.bind_tools(
    TOOLS
)

