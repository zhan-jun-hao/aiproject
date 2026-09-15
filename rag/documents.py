from langchain_core.documents import Document


documents = [
    Document(
        page_content="好课来平台课程购买后2天内可以申请退款。",
        metadata={
            "doc_id": "refund_time_limit",
            "type": "refund",
            "title": "退款时间限制",
            "source": "platform_rule"
        }
    ),

    Document(
        page_content="学习进度超过20%的课程不支持退款。",
        metadata={
            "doc_id": "refund_progress_limit",
            "type": "refund",
            "title": "退款学习进度限制",
            "source": "platform_rule"
        }
    ),

    Document(
        page_content="特价课程不支持退款。",
        metadata={
            "doc_id": "refund_special_course",
            "type": "refund",
            "title": "特价课程退款规则",
            "source": "platform_rule"
        }
    ),

    Document(
        page_content="优惠券领取后7天内有效。",
        metadata={
            "doc_id": "coupon_validity",
            "type": "coupon",
            "title": "优惠券有效期",
            "source": "platform_rule"
        }
    ),
]