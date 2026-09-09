from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from ai.chat_model import chat_model
from ai.prompt import SYSTEM_PROMPT
from rag.vector_store import vector_store


# 临时使用内存保存会话
conversation_dict: dict[str, list] = {}

# 最近保留 10 条消息
MAX_HISTORY_SIZE = 10


def chat(message: str, conversation_id: str) -> str:

    # 1.获取历史会话
    history = conversation_dict.get(conversation_id, [])

    recent_content = history[-MAX_HISTORY_SIZE:]

    # 2.RAG检索知识
    docs = vector_store.similarity_search(
        message,
        k=2
    )

    # 3.Document 转成文本
    knowledge = ""

    for doc in docs:
        knowledge += doc.page_content
        knowledge += "\n"

    # 4.构造发送给大模型的上下文
    messages = [
        SystemMessage(
            content=f"""
            {SYSTEM_PROMPT}
            
            这是从好课来平台知识库中检索到的平台资料：
            
            【平台资料】
            {knowledge}
            
            请优先根据平台资料回答。
            如果资料中没有足够信息，不要编造。
            """),
        *recent_content,
        HumanMessage(content=message)
    ]

    # 5.调用大模型
    response = chat_model.invoke(messages)
    answer = str(response.content)
    # 6.保存本轮对话
    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=answer))
    conversation_dict[conversation_id] = history
    # 7.返回结果
    return answer