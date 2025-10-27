from collections.abc import AsyncIterator

from grpc.aio import ServicerContext

from pb.scrapli_grpc_pb2 import Command, Response

from .logger import log
from .scrapli_device import ScrapliDevice

__all__ = ("ScrapliHandler",)


async def get_response(request: Command, device: ScrapliDevice) -> Response:
    log.info(f"запрос команды {request.command!r} с устройства {request.host.host!r}")
    response = await device.send_command(
        command=request.command,
    )
    return Response(
        host=response.host,
        channel_input=response.channel_input,
        result=response.result,
        failed=response.failed,
        elapsed_time=response.elapsed_time,
    )


class ScrapliHandler:
    @classmethod
    async def handle_chat(
        cls,
        request_iterator: AsyncIterator[Command],
        context: ServicerContext[Command, Response],
    ) -> AsyncIterator[Response]:

        request = await anext(request_iterator)
        async with ScrapliDevice(request.host) as device:
            response = await get_response(request, device)
            yield response
            async for request in request_iterator:
                response = await get_response(request, device)
                yield response

    @classmethod
    async def handle(
        cls,
        request: Command,
        context: ServicerContext[Command, Response],
    ) -> Response:
        log.info(f"запрос команды {request.command!r} с устройства {request.host.host!r}")
        async with ScrapliDevice(request.host) as device:
            response = await get_response(request, device)
            return response
            return response
            return response
