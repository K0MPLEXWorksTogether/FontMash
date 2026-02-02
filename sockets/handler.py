#!/usr/bin/env python3

import json
import asyncio
from websockets import WebSocketServerProtocol

from services.font import FontService
from sockets.broadcaster import Broadcaster
from utils.logger import Logger
from services.elo import ELOService


class Handler:
    def __init__(self, font_service: FontService, broadcaster: Broadcaster) -> None:
        self.font_service = font_service
        self.broadcaster = broadcaster
        self.logger = Logger().get_logger()
        self.elo = ELOService(font_service)

    async def __call__(self, websocket: WebSocketServerProtocol) -> None:
        await self.broadcaster.register(websocket)

        try:
            matchup = await self.font_service.head_on_head()
            await websocket.send(json.dumps({
                "type": "matchup",
                "fonts": matchup
            }))

            async for message in websocket:
                data = json.loads(message)
                choice = data.get("choice")

                if choice not in (1, 2):
                    continue

                outcome = 1 if choice == 1 else 0
                await self.elo.update_elo(matchup[0][0], matchup[1][0], outcome)

                leaderboard = await self.font_service.leaderboard(0, 9)
                await self.broadcaster.broadcast({
                    "type": "leaderboard",
                    "data": leaderboard,
                })

                matchup = await self.font_service.head_on_head()
                await websocket.send(json.dumps({
                    "type": "matchup",
                    "fonts": matchup,
                }))
        except Exception as err:
            self.logger.error(f"[handler]: Could not handle socket client: {err}")
        finally:
            await self.broadcaster.unregister(websocket)