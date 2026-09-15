from schema.agent_output_schema import AgentAnswer

# 结构化输出模型
from langchain.chat_models import init_chat_model
from config.settings import (
    ALIYUN_BAI_LIAN,
    ALIYUN_API_BASE
)

output_model = init_chat_model(
    model="qwen3.8-flash",
    model_provider="openai",
    api_key=ALIYUN_BAI_LIAN,
    base_url=ALIYUN_API_BASE,
    temperature=0,
    extra_body={
            "enable_thinking": False
        }
)


structured_output_model = output_model.with_structured_output(
    AgentAnswer,  # 开启强类型输出
    method="json_schema",
    strict=True
)