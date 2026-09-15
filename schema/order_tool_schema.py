from pydantic import BaseModel


class OrderToolResult(BaseModel):
    orderNo: str
    courseTitle: str | None = None

    status: str | None = None
    payType: str | None = None

    coursePrice: str | None = None
    discountAmount: str | None = None
    payAmount: str | None = None

    createTime: str | None = None
    payTime: str | None = None