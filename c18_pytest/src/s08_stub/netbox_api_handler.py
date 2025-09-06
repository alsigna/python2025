from types import TracebackType
from typing import Any, Literal, Self

import httpx


class NetboxAPIHandler:
    def __init__(self, base_url: str, token: str, session_limit: int = 10) -> None:
        self.base_url = base_url
        self.token = token
        self.session_limit = session_limit
        self.session: httpx.Client | httpx.AsyncClient | None = None

    def __enter__(self) -> Self:
        self.session = httpx.Client(
            transport=httpx.HTTPTransport(
                verify=False,
                limits=httpx.Limits(
                    max_connections=self.session_limit,
                ),
            ),
            base_url=self.base_url,
            headers={
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json",
                "Accept-Charset": "application/json",
                "User-Agent": "demo-python2025",
            },
        )
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        assert isinstance(self.session, httpx.Client)
        if self.session is not None:
            self.session.close()
        self.session = None
        return False

    async def __aenter__(self) -> Self:
        self.session = httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(
                verify=False,
                limits=httpx.Limits(
                    max_connections=self.session_limit,
                ),
            ),
            base_url=self.base_url,
            headers={
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "demo-python2025",
            },
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        assert isinstance(self.session, httpx.AsyncClient)
        if self.session is not None:
            await self.session.aclose()
        self.session = None
        return False

    def get(self, url: str, params: list[tuple[str, Any]] | None = None) -> list[dict[str, Any]]:
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")

        assert isinstance(self.session, httpx.Client), f"{type(self.session)=}"
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        response_json = response.json()

        if "results" not in response_json:
            return [response_json]

        result: list[dict[str, Any]] = response_json.get("results", [])
        while (url := response_json.get("next")) is not None:
            response = self.session.get(url=url)
            response.raise_for_status()
            response_json = response.json()
            result.extend(response_json.get("results", []))

        return result

    async def aget(self, url: str, params: list[tuple[str, Any]] | None = None) -> list[dict[str, Any]]:
        if self.session is None:
            raise RuntimeError("метод используется в контекстном менеджере")
        assert isinstance(self.session, httpx.AsyncClient)
        response: httpx.Response = await self.session.get(url=url, params=params)
        response.raise_for_status()
        response_json = response.json()

        if "results" not in response_json:
            return [response_json]

        result: list[dict[str, Any]] = response_json.get("results", [])
        while (url := response_json.get("next")) is not None:
            response = await self.session.get(url=url)
            response.raise_for_status()
            response_json = response.json()
            result.extend(response_json.get("results", []))

        return result
