from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

from ai.chat_model import chat_model_with_tools
from ai.output_model import structured_output_model
from ai.prompt import SYSTEM_PROMPT, OUTPUT_PROMPT

from rag.retriever import retrieve
from tools import TOOLS

from schema.agent_output_schema import AgentAnswer


# 临时使用内存保存会话
conversation_dict: dict[str, list] = {}

# 最近保留 10 条消息
MAX_HISTORY_SIZE = 10

# Agent 最大行动轮数
MAX_AGENT_ROUNDS = 8


# Tool哈希关联
TOOL_MAP = {}

for tool in TOOLS:
    TOOL_MAP[tool.name] = tool


async def chat(
        message: str,
        conversation_id: str
) -> AgentAnswer:

    # 1. 获取历史会话
    history = conversation_dict.get(conversation_id, [])

    recent_content = history[-MAX_HISTORY_SIZE:]

    # 2. RAG 检索知识
    retrieved_docs = await retrieve(query=message)

    # 3. Document 转文本
    knowledge = ""

    for item in retrieved_docs:
        knowledge += item.document.page_content
        knowledge += "\n"

    # 4. 构造 Agent 上下文
    messages = [
        SystemMessage(
            content=f"""
            {SYSTEM_PROMPT}

            这是从好课来平台知识库中检索到的平台资料：

            【平台资料】
            {knowledge}

            请优先根据平台资料回答。
            如果资料中没有足够信息，不要编造。
            """
        ),

        *recent_content,

        HumanMessage(content=message)
    ]

    # 5. Agent Loop

    # Agent 最终得到的自然语言初步答案
    raw_answer = ""

    # 保存本轮所有 Tool 查询结果
    tool_results: list[str] = []

    # 保存本轮实际调用的 Tool
    used_tool_names: list[str] = []

    for round_index in range(MAX_AGENT_ROUNDS):

        # 5.1 调用 LLM
        response = await chat_model_with_tools.ainvoke(messages)

        # 保存 AI 当前这一轮的行动
        messages.append(response)

        # 5.2 没有 Tool Call
        # Agent 认为任务完成
        if not response.tool_calls:
            raw_answer = str(response.content or "")
            break

        # 5.3 执行所有 Tool Call
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            tool = TOOL_MAP.get(tool_name)

            # Tool 不存在
            if tool is None:
                tool_result = f"系统不存在工具：{tool_name}"

            else:
                try:
                    tool_result = await tool.ainvoke(tool_args)

                except Exception as e:
                    tool_result = f"工具 {tool_name} 执行失败：{str(e)}"

            # 记录本轮使用的 Tool
            if tool_name not in used_tool_names:
                used_tool_names.append(tool_name)

            # 5.4 ToolResult 给 Agent
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )

            # 5.5 同时保存 ToolResult
            # 给最后的结构化输出层
            tool_results.append(
                f"""
                【Tool】
                {tool_name}

                【查询结果】
                {tool_result}
                """
            )

    else:
        raw_answer = "任务处理步骤过多，暂时无法完成该请求。"

    # 6. Structured Output

    # LLM也需要换行 可读性更高
    tool_context = "\n".join(tool_results)

    used_tools_context = "\n".join(used_tool_names)

    output_messages = [
        SystemMessage(content=OUTPUT_PROMPT),

        HumanMessage(
            content=f"""
            【用户问题】
            {message}

            【本轮实际调用的 Tool】
            {used_tools_context}

            【业务系统查询结果】
            {tool_context}

            【Agent 初步回答】
            {raw_answer}

            【结构化输出规则】

            1. 只有本轮调用了 query_order，
               才允许填充 order。
               如果没有调用 query_order，
               order 必须为 null。

            2. 只有本轮调用了
               query_course
               或
               query_course_by_order_no，
               才允许填充 course。
               如果没有调用课程查询 Tool，
               course 必须为 null。

            3. Tool 查询结果属于系统确认的业务事实，
               不得修改、猜测或补充不存在的数据。

            4. 不得因为订单结果中偶然出现课程相关字段，
               就自动构造 CourseCard。

            5. 不得因为课程查询是通过订单号触发的，
               就自动构造 OrderCard。

            请根据以上已经确认的信息，
            生成最终结构化回答。
            """
        )
    ]

    agent_answer = await structured_output_model.ainvoke(output_messages)

    # 7. 保存会话历史
    history.append(
        HumanMessage(content=message)
    )

    history.append(
        AIMessage(content=agent_answer.message)
    )

    conversation_dict[conversation_id] = history

    # 8. 返回结构化结果
    return agent_answer