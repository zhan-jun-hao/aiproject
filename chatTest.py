from fastapi import FastAPI
from pydantic import BaseModel

'''
    1.一个简单的fastapi + langchain 调用 model 
    2.项目启动:
        1.pip install uvicorn
        2.进入项目根目录
        3.uvicorn chatTest:app --reload
        4.swagger: /docs
        5.FastAPI 是 Web 框架, Uvicorn 才是真正跑服务的服务器
'''

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


'''
    fastapi请求部分
'''
app = FastAPI()

class ChatResult(BaseModel):
    message: str
    code: int

class ChatRequest(BaseModel):
    message: str

@app.post("/sayHello")
def say_hello(request: ChatRequest, response_model=ChatResult):
    response = model.invoke(request.message)
    return ChatResult(
        message=str(response.content),
        code=200
    )
