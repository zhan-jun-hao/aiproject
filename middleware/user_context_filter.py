from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from schema.user_context import UserContext, UserContextHolder


class UserContextMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app,
        internal_secret: str,
        require_internal_secret: bool = True,
        ignored_paths: list[str] | None = None
    ):
        super().__init__(app)
        self.internal_secret = internal_secret
        self.require_internal_secret = require_internal_secret
        self.ignored_paths = ignored_paths or []

    async def dispatch(self, request: Request, call_next):

        if request.url.path in self.ignored_paths:
            return await call_next(request)

        actual_secret = request.headers.get("X-Internal-Secret")

        trusted = (actual_secret is not None
                   and
                   actual_secret == self.internal_secret)


        if self.require_internal_secret and not trusted:
            return JSONResponse(
                status_code=401,
                content={
                    "code": 401,
                    "msg": "Request must pass through gateway",
                    "data": None
                }
            )

        token = None

        try:
            if trusted:
                user_id = request.headers.get("X-User-Id")
                user_role = request.headers.get("X-User-Role")

                # 两个都没有，允许继续
                if user_id is None and user_role is None:
                    return await call_next(request)

                # 只传了其中一个，非法
                if user_id is None or user_role is None:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "code": 401,
                            "msg": "Invalid user context",
                            "data": None
                        }
                    )

                try:
                    context = UserContext(
                        user_id=int(user_id),
                        role=int(user_role)
                    )
                except ValueError:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "code": 401,
                            "msg": "Invalid user context",
                            "data": None
                        }
                    )

                token = UserContextHolder.set(context)

            return await call_next(request)

        finally:
            if token is not None:
                UserContextHolder.reset(token)