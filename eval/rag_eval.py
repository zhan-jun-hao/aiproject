import asyncio

from eval.rag_eval_cases import RAG_EVAL_CASES
from rag.retriever import retrieve


def calculate_recall_at_k(
        actual_doc_ids: list[str],
        expected_doc_ids: set[str],
        k: int
) -> float:

    retrieved_ids = set(
        actual_doc_ids[:k]
    )

    hit_count = len(
        retrieved_ids
        & expected_doc_ids
    )

    return (
        hit_count
        / len(expected_doc_ids)
    )


async def main():

    # =========================
    # 正样本指标
    # =========================
    total_recall_1 = 0.0
    total_recall_3 = 0.0

    positive_count = 0

    # =========================
    # 负样本指标
    # =========================
    negative_count = 0

    # 负样本经过 Threshold 后
    # 仍然召回知识的数量
    false_retrieval_count = 0

    # 记录错误召回的 Top1 Score
    false_retrieval_top1_scores = []

    for index, case in enumerate(
        RAG_EVAL_CASES,
        start=1
    ):

        # retrieve 内部已经进行了
        # TopK + Threshold 过滤
        results = await retrieve(
            query=case["question"],
            top_k=4
        )

        actual_doc_ids = [
            item.document.metadata.get(
                "doc_id"
            )
            for item in results
        ]

        expected_doc_ids = (
            case["expected_doc_ids"]
        )

        print(
            f"\n========== Case {index} =========="
        )

        print(
            f"问题：{case['question']}"
        )

        # =========================
        # 正样本
        # =========================
        if expected_doc_ids:

            positive_count += 1

            recall_1 = calculate_recall_at_k(
                actual_doc_ids,
                expected_doc_ids,
                1
            )

            recall_3 = calculate_recall_at_k(
                actual_doc_ids,
                expected_doc_ids,
                3
            )

            total_recall_1 += recall_1
            total_recall_3 += recall_3

            print(
                "类型：正样本"
            )

            print(
                f"预期：{expected_doc_ids}"
            )

            print(
                f"Recall@1：{recall_1:.2%}"
            )

            print(
                f"Recall@3：{recall_3:.2%}"
            )

        # =========================
        # 负样本
        # =========================
        else:

            negative_count += 1

            print(
                "类型：负样本"
            )

            print(
                "预期：不应该召回任何知识"
            )

            # 经过 Threshold 后
            # 还有结果，说明发生错误召回
            if results:

                false_retrieval_count += 1

                false_retrieval_top1_scores.append(
                    results[0].score
                )

                print(
                    "结果：❌ 发生错误召回"
                )

            else:

                print(
                    "结果：✅ 成功拒绝召回"
                )

        # =========================
        # 打印实际召回结果
        # =========================
        print(
            "实际召回："
        )

        if not results:

            print(
                "无召回结果"
            )

        for rank, item in enumerate(
            results,
            start=1
        ):

            print(
                f"Top{rank} "
                f"score={item.score:.4f} "
                f"doc_id="
                f"{item.document.metadata.get('doc_id')}"
            )

            print(
                f"    "
                f"{item.document.page_content}"
            )

    # =========================
    # 最终结果
    # =========================

    print(
        "\n=============================="
    )

    print(
        "RAG Eval"
    )

    # =========================
    # 正样本最终指标
    # =========================
    if positive_count > 0:

        recall_at_1 = (
            total_recall_1
            / positive_count
        )

        recall_at_3 = (
            total_recall_3
            / positive_count
        )

        print(
            f"正样本数：{positive_count}"
        )

        print(
            f"Recall@1："
            f"{recall_at_1:.2%}"
        )

        print(
            f"Recall@3："
            f"{recall_at_3:.2%}"
        )

    # =========================
    # 负样本最终指标
    # =========================
    if negative_count > 0:

        false_retrieval_rate = (
            false_retrieval_count
            / negative_count
        )

        print(
            f"负样本数：{negative_count}"
        )

        print(
            f"错误召回数："
            f"{false_retrieval_count}"
        )

        print(
            f"False Retrieval Rate："
            f"{false_retrieval_rate:.2%}"
        )

        if false_retrieval_top1_scores:

            print(
                f"错误召回最高 Score："
                f"{max(false_retrieval_top1_scores):.4f}"
            )

    print(
        "=============================="
    )


if __name__ == "__main__":
    asyncio.run(
        main()
    )