import asyncio
from unittest.mock import AsyncMock, MagicMock

if __name__ == "__main__":
    mock = MagicMock(foo=AsyncMock(return_value=42))
    # mock.foo это awaitable объект
    print(asyncio.run(mock.foo()))
