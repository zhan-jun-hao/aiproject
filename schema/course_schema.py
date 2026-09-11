from enum import IntEnum

from pydantic import BaseModel


class CourseChargeTypeEnum(IntEnum):
    FREE = 0
    PAID = 1
    VIP_FREE = 2

    @property
    def label(self) -> str:
        labels = {
            self.FREE: "免费",
            self.PAID: "付费",
            self.VIP_FREE: "VIP免费",
        }
        return labels[self]


class ClientCourseDetailVo(BaseModel):
    """
    客户端课程详情
    """

    # 课程ID
    id: int

    # 课程分类名称
    categoryName: str

    # 课程标题
    title: str

    # 课程副标题/卖点文案
    subtitle: str

    # 封面图URL
    coverUrl: str

    # 讲师名称
    teacherName: str

    # 课程摘要
    summary: str

    # 课程详情
    detail: str

    # 课程售价，单位：分
    price: int

    # 章节数量
    episodeCount: int

    # 购买人数/销量
    buyCount: int

    # 收费类型：0免费 1付费 2VIP免费
    chargeType: CourseChargeTypeEnum