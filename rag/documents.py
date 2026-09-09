from langchain_core.documents import Document

documents = [
    Document(
        page_content="好课来平台课程购买后2天内可以申请退款。",
        metadata={"type": "refund"}
    ),
    Document(
        page_content="学习进度超过20%的课程不支持退款。",
        metadata={"type": "refund"}
    ),
    Document(
        page_content="特价课程不支持退款。",
        metadata={"type": "refund"}
    ),
    Document(
        page_content="优惠券领取后7天内有效。",
        metadata={"type": "coupon"}
    ),
]