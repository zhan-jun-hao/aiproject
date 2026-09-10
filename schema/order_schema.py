from datetime import datetime
from enum import Enum

from pydantic import BaseModel


from enum import IntEnum


'''
    定义枚举
    CourseOrderStatusEnum(1).label >> 已支付
'''
class CourseOrderStatusEnum(IntEnum):
    PENDING_PAYMENT = 0
    PAID = 1
    CANCELLED = 2
    REFUNDED = 3
    CLOSED = 4

    @property
    def label(self) -> str:
        labels = {
            self.PENDING_PAYMENT: "待支付",
            self.PAID: "已支付",
            self.CANCELLED: "已取消",
            self.REFUNDED: "已退款",
            self.CLOSED: "已关闭",
        }

        return labels[self]


class CourseOrderPayTypeEnum(IntEnum):
    UNPAID = 0
    WECHAT = 1
    ALIPAY = 2
    MOCK = 3

    @property
    def label(self) -> str:
        return {
            self.UNPAID: "未支付",
            self.WECHAT: "微信支付",
            self.ALIPAY: "支付宝支付",
            self.MOCK: "模拟支付",
        }[self]

class CourseOrderBasicVo(BaseModel):
    id: int
    orderNo: str
    userId: int
    courseId: int

    courseTitle: str
    coverUrl: str | None = None

    coursePrice: int

    userCouponId: int | None = None
    couponName: str | None = None

    discountAmount: int
    payAmount: int

    status: CourseOrderStatusEnum
    payType: CourseOrderPayTypeEnum

    expireTime: datetime
    payTime: datetime | None = None
    createTime: datetime