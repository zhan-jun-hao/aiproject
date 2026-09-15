from langchain_openai import OpenAIEmbeddings

from config.settings import (
    ALIYUN_BAI_LIAN,
    ALIYUN_API_BASE
)

embedding_model = OpenAIEmbeddings(
    model="qwen3.7-text-embedding-flash",
    api_key=ALIYUN_BAI_LIAN,
    base_url=ALIYUN_API_BASE,
    check_embedding_ctx_length=False,
    dimensions=1024,
)