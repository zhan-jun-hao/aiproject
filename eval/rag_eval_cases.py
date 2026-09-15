RAG_EVAL_CASES = [

    # =========================
    # 正样本：退款时间限制
    # =========================
    {
        "question": "买了课程之后几天内可以退款？",
        "expected_doc_ids": {
            "refund_time_limit"
        }
    },

    {
        "question": "课程买了三天了还能退款吗？",
        "expected_doc_ids": {
            "refund_time_limit"
        }
    },

    # =========================
    # 正样本：学习进度限制
    # =========================
    {
        "question": "学习进度超过20%还能退款吗？",
        "expected_doc_ids": {
            "refund_progress_limit"
        }
    },

    {
        "question": "我已经学了30%的课程，可以退吗？",
        "expected_doc_ids": {
            "refund_progress_limit"
        }
    },

    # =========================
    # 正样本：特价课程
    # =========================
    {
        "question": "特价课程可以申请退款吗？",
        "expected_doc_ids": {
            "refund_special_course"
        }
    },

    {
        "question": "打折特价课支持退款吗？",
        "expected_doc_ids": {
            "refund_special_course"
        }
    },

    # =========================
    # 正样本：优惠券
    # =========================
    {
        "question": "优惠券可以用多久？",
        "expected_doc_ids": {
            "coupon_validity"
        }
    },

    {
        "question": "优惠券领取之后什么时候过期？",
        "expected_doc_ids": {
            "coupon_validity"
        }
    },

    {
        "question": "我八天前领取的优惠券还能用吗？",
        "expected_doc_ids": {
            "coupon_validity"
        }
    },

    # =========================
    # 正样本：一个问题涉及多条退款规则
    # =========================
    {
        "question": "刚买的课程可以退吗？",
        "expected_doc_ids": {
            "refund_time_limit",
            "refund_progress_limit",
            "refund_special_course"
        }
    },

    # =========================
    # 负样本：知识库中没有答案
    # =========================
    {
        "question": "Java HashMap 底层是怎么实现的？",
        "expected_doc_ids": set()
    },

    {
        "question": "TCP 为什么要三次握手？",
        "expected_doc_ids": set()
    },

    {
        "question": "今天天气怎么样？",
        "expected_doc_ids": set()
    },

    {
        "question": "平台支持提现吗？",
        "expected_doc_ids": set()
    },

    {
        "question": "这门课程的老师是谁？",
        "expected_doc_ids": set()
    },

    {
        "question": "怎么修改登录密码？",
        "expected_doc_ids": set()
    },
]