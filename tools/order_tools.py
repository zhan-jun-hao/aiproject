from langchain_core.tools import tool
import httpx

from schema.common_schema import Result
from schema.order_schema import CourseOrderBasicVo


@tool
async def query_order(order_id: str) -> str:
    """
    根据订单号查询订单状态
    当用户询问订单状态、支付状态、退款状态时调用此工具
    :param order_id: 订单id
    :return:
    """
    headers = {
        "X-User-Id": "1",
        "X-User-Role": "1",
        "X-Internal-Secret": "zhanjunhao"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8080/api/main/inner/orders/payment/{order_id}",
            timeout=10,
            headers=headers,
        )

    response.raise_for_status()

    result = Result[CourseOrderBasicVo].model_validate(
        response.json(),
    )

    # 转换成了对象
    if result.code != 200:
        return result.msg

    data = result.data

    return (
            f"订单号：{data.orderNo}\n"
            f"课程名称：{data.courseTitle}\n"
            f"订单状态：{data.status.label}\n"
            f"支付方式：{data.payType.label}\n"
            f"订单金额：{data.coursePrice / 100:.2f} 元\n"
            f"优惠金额：{data.discountAmount / 100:.2f} 元\n"
            f"实付金额：{data.payAmount / 100:.2f} 元\n"
            f"创建时间：{data.createTime}\n"
            f"支付时间：{data.payTime or '尚未支付'}"
    )