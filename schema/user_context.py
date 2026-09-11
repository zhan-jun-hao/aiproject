from contextvars import ContextVar, Token
from dataclasses import dataclass

'''
    1._ 是命名约定, 外部最好不要直接操作
    2.ContextVar是上下文局部变量 对应ThreadLocal 传入两个参数: 这个上下文的名字和默认值
    3.@dataclass很像record类, 自动构建全参构造方法
    4.@staticmethod是静态方法, 对应static方法
    5.set返回的是一个token, 它能够恢复set前的状态 与reset配合
'''

@dataclass
class UserContext:
    user_id: int
    role: int

_user_context: ContextVar[UserContext | None] = ContextVar(
    "user_context",
    default=None
)


class UserContextHolder:

    @staticmethod
    def set(context: UserContext) -> Token:
        return _user_context.set(context)

    @staticmethod
    def get() -> UserContext | None:
        return _user_context.get()

    @staticmethod
    def reset(token):
        _user_context.reset(token)