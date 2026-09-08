from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from pydantic import BaseModel
import uuid

'''
    1.项目启动: uvicorn 04memoryTest:app --reload
    2.完成代码后思考: 
        这个对话id万一用户恶意传过来呢? 用user_id + conversation_id共同决定 并且对话记录需要持久化
        这个上下文无限增长? 
        并且每条消息的token不一样, 因为有些消息一句话只有5个token, 有些消息一条可能有3000个token?
    3.大模型根本不了解平台业务流程, 所以自然而然想到知识库RAG
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
    conversation_id: str  # 1.会话id

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None # 会话id 第一次不用传 后端生成传给前端

# 2.全局字典存储会话信息 conversation_id -> messages
conversation_dict : dict[str, list[BaseMessage]] = {}
MAX_HISTORY_SIZE = 10

@app.post("/", response_model=ChatResult)
def test(request: ChatRequest):
    # 1.先获取历史消息
    conversation_id = request.conversation_id
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    history = conversation_dict.get(conversation_id, [])
    # 2.压缩上下文 避免无限增加
    recent_content = history[-MAX_HISTORY_SIZE:]


    # 3.组装本次上下文
    messages = [
        SystemMessage(SYSTEM_PROMPT),
        *recent_content, # 解包写法 把这个列表中的每个元素拆分放入list, 而不是加整个list
        HumanMessage(request.message),
    ]
    res = model.invoke(messages)
    history.append(HumanMessage(content=request.message))
    history.append(AIMessage(content=res.content))
    conversation_dict[conversation_id] = history

    return ChatResult(
        message=str(res.content),
        code=200,
        conversation_id=conversation_id,
    )