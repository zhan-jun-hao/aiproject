from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel


'''
    接入大模型部分
'''
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
api_base = os.getenv("DEEPSEEK_API_BASE")

model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="deepseek",
    api_key=api_key,
    base_url=api_base,
    temperature=0.7
)

SYSTEM_PROMPT = """
            你是好课来教育平台的 AI 客服助手。
            
            你的职责: 帮助用户解决与好课来平台有关的问题
            
            规则:
            1.不得编造平台业务信息
            2.不知道的消息明确告诉用户无法确认
            3.只处理好课来平台相关问题
            4.使用中文简洁回答
        """

'''
    fastapi请求部分
'''
app = FastAPI()

class ChatResult(BaseModel):
    message: str
    code: int

class ChatRequest(BaseModel):
    message: str

@app.post("/", response_model=ChatResult)
def test(request: ChatRequest):
    messages.append(HumanMessage(content=request.message))
    response = model.invoke(messages)


    return ChatResult(
        message=str(response.content),
        code=200
    )
