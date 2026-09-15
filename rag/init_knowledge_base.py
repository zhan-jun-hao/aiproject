from langchain_qdrant import QdrantVectorStore
from ai.embedding_model import embedding_model
from rag.documents import documents


QDRANT_URL = "http://localhost:6400"
COLLECTION_NAME = "aiproject"


def init_knowledge_base():

    QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embedding_model,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )

    print("Qdrant 知识库初始化完成")


if __name__ == "__main__":
    init_knowledge_base()