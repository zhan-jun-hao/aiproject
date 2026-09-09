from langchain_openai import OpenAIEmbeddings

from config.settings import (
    ALIYUN_BAI_LIAN,
    ALIYUN_API_BASE
)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-v4",
    api_key=ALIYUN_BAI_LIAN,
    base_url=ALIYUN_API_BASE,
    check_embedding_ctx_length=False,
    dimensions=1024,
)