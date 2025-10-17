import base64
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import TypeVar

import grpc
from google.protobuf.message import Message
from grpc.aio import ClientCallDetails, StreamStreamCall, UnaryUnaryCall

__all__ = (
    "ClientSSAuthInterceptor",
    "ClientUUAuthInterceptor",
)

Request = TypeVar("Request", bound=Message)
Response = TypeVar("Response", bound=Message)


class ClientAuthInterceptorMixIn:
    def __init__(self, username: str, password: str) -> None:
        self.token = base64.b64encode(f"{username}:{password}".encode()).decode()

    def _get_updated_metadata(self, client_call_details: ClientCallDetails) -> ClientCallDetails:
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        else:
            metadata = []

        metadata.append(("authorization", f"Basic {self.token}"))

        return grpc.aio.ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
        )


class ClientUUAuthInterceptor(
    ClientAuthInterceptorMixIn,
    grpc.aio.UnaryUnaryClientInterceptor,
):
    async def intercept_unary_unary(
        self,
        continuation: Callable[
            [ClientCallDetails, Request],
            Awaitable[UnaryUnaryCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request: Request,
    ) -> Response:
        new_details = self._get_updated_metadata(client_call_details)
        return await continuation(new_details, request)


class ClientSSAuthInterceptor(
    ClientAuthInterceptorMixIn,
    grpc.aio.StreamStreamClientInterceptor,
):
    async def intercept_stream_stream(
        self,
        continuation: Callable[
            [ClientCallDetails, AsyncIterator[Request]],
            Awaitable[StreamStreamCall[Request, Response]],
        ],
        client_call_details: ClientCallDetails,
        request_iterator: AsyncIterator[Request],
    ) -> AsyncIterator[Response]:
        new_details = self._get_updated_metadata(client_call_details)
        return await continuation(new_details, request_iterator)
