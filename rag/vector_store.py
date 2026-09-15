from langchain_qdrant import QdrantVectorStore
from ai.embedding_model import embedding_model


QDRANT_URL = "http://localhost:6400"
COLLECTION_NAME = "aiproject"


vector_store = (
    QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        url=QDRANT_URL
    )
)