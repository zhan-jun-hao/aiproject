from fastapi import FastAPI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from pydantic import BaseModel
import uuid

'''
    1.项目启动: uvicorn 05ragTest:app --reload
    2.完成代码后思考: 
       怎么检索RAG知识? 
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

# 1.思考RAG知识怎么高效检索
RAG_KNOWLEDGE = [
    "好课来平台课程购买后2天内可以申请退款。",
    "学习进度超过20%的课程不支持退款。",
    "特价课程不支持退款。",
    "优惠券领取后7天内有效。",
]

'''
    fastapi请求部分
'''
app = FastAPI()


class ChatResult(BaseModel):
    message: str
    code: int
    conversation_id: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None

conversation_dict : dict[str, list] = {}
MAX_HISTORY_SIZE = 10

@app.post("/", response_model=ChatResult)
def test(request: ChatRequest):
    conversation_id = request.conversation_id
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    history = conversation_dict.get(conversation_id, [])

    recent_content = history[-MAX_HISTORY_SIZE:]

    # 向LLM加入检索到的知识
    messages = [
        SystemMessage(f"""
            {SYSTEM_PROMPT},
            这是检索到的平台资料, 请先根据这个知识库进行回答, 资料中没有的信息不要编造
            【平台资料】: {RAG_KNOWLEDGE}
        """),
        *recent_content,
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
