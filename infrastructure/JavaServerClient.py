import httpx
from httpx import Response


class JavaServerClient:

    def __init__(
        self,
        base_url: str,
        internal_secret: str,
        timeout: int = 10
    ):
        self.base_url = base_url
        self.internal_secret = internal_secret
        self.timeout = timeout

    async def get(
        self,
        path: str,
        headers: dict | None = None
    ) -> Response:

        request_headers = {
            "X-Internal-Secret": self.internal_secret
        }
        # 如果用户传了headers 就合并字典
        if headers:
            request_headers.update(headers)

        url = self.base_url + path

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.get(url,headers=request_headers)