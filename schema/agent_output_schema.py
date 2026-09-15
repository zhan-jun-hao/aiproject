from pydantic import BaseModel, Field


class OrderCard(BaseModel):
    """
    订单展示信息
    """

    orderNo: str
    status: str
    payType: str | None = None
    payAmount: str
    payTime: str | None = None


class CourseCard(BaseModel):
    """
    课程展示信息
    """

    title: str
    subtitle: str | None = None
    categoryName: str | None = None
    teacherName: str | None = None
    chargeType: str | None = None
    price: str | None = None
    episodeCount: int | None = None
    buyCount: int | None = None
    summary: str | None = None

class AgentAnswer(BaseModel):

    message: str = Field(
        description="最终回答，必须使用简体中文"
    )

    order: OrderCard | None = None

    course: CourseCard | None = None

    suggestions: list[str] = Field(
        default_factory=list,
        max_length=3,
        description=(
            "给用户的后续问题建议。"
            "每一项必须使用简体中文，"
            "禁止使用英文生成问题。"
            "如果没有合适的中文建议则返回空数组。"
        )
    )