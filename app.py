#!/usr/bin/env python3

import asyncio
from websockets.asyncio.server import serve

from services.font import FontService
from sockets.broadcaster import Broadcaster
from sockets.handler import Handler


async def main() -> None:
    font_service = await FontService.create("font_leaderboard")
    broadcaster = Broadcaster()
    handler = Handler(font_service, broadcaster)

    async with serve(handler, "localhost", 8765):
        logger.info('WebSocket running at ws://localhost:8765')
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
