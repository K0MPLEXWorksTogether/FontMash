#!/usr/bin/env python3

import asyncio
from websockets.asyncio.server import serve
from utils.logger import Logger
import os

from services.font import FontService
from sockets.broadcaster import Broadcaster
from sockets.handler import Handler


async def main() -> None:
    font_service = await FontService.create("font_leaderboard")
    broadcaster = Broadcaster()
    handler = Handler(font_service, broadcaster)
    logger = Logger().get_logger()

    PORT = int(os.getenv("PORT"))
    async with serve(handler, "0.0.0.0", PORT):
        logger.info(f"WebSocket running at ws://localhost:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
