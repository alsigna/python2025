from collections.abc import AsyncIterator

from grpc.aio import ServicerContext
from pb.scrapli_grpc_pb2 import Command, Result

from .logger import log
from .scrapli_device import ScrapliDevice


async def get_result(request: Command, device: ScrapliDevice) -> Result:
    log.info(f"новый запрос: {request.host.host} / {request.command}")
    response = await device.cli.send_command(
        command=request.command,
    )
    return Result(
        host=request.host.host,
        channel_input=response.channel_input,
        result=response.result,
        elapsed_time=response.elapsed_time,
        failed=response.failed,
    )


class ScrapliServiceHandler:
    @classmethod
    async def handle(
        cls,
        request: Command,
        context: ServicerContext,
    ) -> Result:
        log.info(f"новый запрос: {request.host.host} / {request.command}")
        async with ScrapliDevice(host=request.host) as device:
            result = await get_result(request, device)

        return result

    @classmethod
    async def handle_chat(
        cls,
        request_iterator: AsyncIterator[Command],
        context: ServicerContext[Command, Result],
    ) -> AsyncIterator[Result]:
        request = await anext(request_iterator)
        async with ScrapliDevice(host=request.host) as device:
            result = await get_result(request, device)
            yield result

            async for request in request_iterator:
                result = await get_result(request, device)
                yield result
