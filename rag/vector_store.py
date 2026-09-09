from langchain_core.vectorstores import InMemoryVectorStore
from ai.embedding_model import embedding_model
from .documents import documents

vector_store = InMemoryVectorStore(embedding_model)

vector_store.add_documents(documents)