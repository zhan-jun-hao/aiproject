from dataclasses import dataclass
from langchain_core.documents import Document
from rag.vector_store import vector_store


"""
    1.检索document
    2.转化为RetrievedDocument对象
    3.返回
"""
@dataclass
class RetrievedDocument:
    document: Document
    score: float


DEFAULT_TOP_K = 3
MIN_SCORE = 0.5

async def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[RetrievedDocument]:

    results = await vector_store.asimilarity_search_with_score(query=query, k=top_k)

    print("\n========== RAG DEBUG ==========")
    print("query:", query)

    for document, score in results:
        print(
            "raw:",
            document.metadata.get("doc_id"),
            "score:",
            score,
            "content:",
            document.page_content
        )

    retrieved_documents = []

    for document, score in results:

        if score < MIN_SCORE:
            print("被 Threshold 过滤:", document.metadata.get("doc_id"),score)
            continue

        item = RetrievedDocument(
            document=document,
            score=score
        )

        retrieved_documents.append(item)

    print(
        "最终保留:",
        [
            (
                item.document.metadata.get("doc_id"),
                item.score
            )
            for item in retrieved_documents
        ]
    )

    print("===============================\n")

    return retrieved_documents