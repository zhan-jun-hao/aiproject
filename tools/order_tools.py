import logging

from langchain_core.tools import tool

from infrastructure.JavaServerClient import JavaServerClient
from schema.common_schema import Result
from schema.order_schema import CourseOrderBasicVo
from schema.order_tool_schema import OrderToolResult
from schema.user_context import UserContextHolder


logger = logging.getLogger("uvicorn.error")


@tool
async def query_order(orderNo: str) -> str:
    """
    根据订单号查询订单状态。

    当用户询问订单状态、支付状态、退款状态时调用此工具。

    :param orderNo: 订单号
    :return: 订单结构化 JSON 数据
    """

    context = UserContextHolder.get()

    if context is None:
        return '{"success": false, "message": "用户还未登录"}'

    headers = {
        "X-User-Id": str(context.user_id),
        "X-User-Role": str(context.role),
    }

    try:
        java_client = JavaServerClient(
            base_url="http://localhost:8080",
            internal_secret="zhanjunhao"
        )

        response = await java_client.get(
            f"/api/main/inner/orders/payment/{orderNo}",
            headers=headers
        )

        response.raise_for_status()

        result = Result[CourseOrderBasicVo].model_validate(
            response.json()
        )

        if result.code != 200:
            return (
                '{"success": false, '
                f'"message": "{result.msg}"'
                '}'
            )

        data = result.data

        if data is None:
            return '{"success": false, "message": "未查询到订单信息"}'

        order_result = OrderToolResult(
            orderNo=data.orderNo,
            courseTitle=data.courseTitle,
            status=data.status.label if data.status else None,
            payType=data.payType.label if data.payType else None,
            coursePrice=(
                f"{data.coursePrice / 100:.2f} 元"
                if data.coursePrice is not None
                else None
            ),
            discountAmount=(
                f"{data.discountAmount / 100:.2f} 元"
                if data.discountAmount is not None
                else None
            ),
            payAmount=(
                f"{data.payAmount / 100:.2f} 元"
                if data.payAmount is not None
                else None
            ),
            createTime=(
                str(data.createTime)
                if data.createTime
                else None
            ),
            payTime=(
                str(data.payTime)
                if data.payTime
                else None
            )
        )

        return order_result.model_dump_json()

    except Exception:
        logger.exception(
            "订单查询失败，orderNo=%s",
            orderNo
        )

        return '{"success": false, "message": "订单服务暂时无法访问，请稍后重试"}'