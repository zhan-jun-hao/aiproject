from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

from ai.chat_model import chat_model_with_tools
from ai.prompt import SYSTEM_PROMPT
from rag.vector_store import vector_store
from tools import TOOLS


# 临时使用内存保存会话
conversation_dict: dict[str, list] = {}

# 最近保留 10 条消息
MAX_HISTORY_SIZE = 10

# 一般来讲需要等外部io的需要用async和await ainvoke
async def chat(message: str, conversation_id: str) -> str:

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

    # 5.第1次调用大模型
    response = await chat_model_with_tools.ainvoke(messages)
    # 先把AIMessage放进去
    messages.append(response)
    # 6.判断 LLM 是否请求调用Tools
    if response.tool_calls:
        for tool_call in response.tool_calls:
            for tool in TOOLS:
                if tool.name == tool_call['name']:
                    # 6.1 真正执行Tool
                    tool_result = await tool.ainvoke(tool_call['args'])
                    messages.append(ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call['id'] # 这一次工具调用的唯一编号
                    ))
        # 6.2 生成最终答案
        final_response = await chat_model_with_tools.ainvoke(messages)

    else:
        final_response = response
    # 8.保存本轮对话
    answer = str(final_response.content)
    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=answer))
    conversation_dict[conversation_id] = history
    # 9.返回结果
    return answer