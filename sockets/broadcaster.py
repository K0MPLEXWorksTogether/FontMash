#!/usr/bin/env python3

import json
import asyncio
from typing import Set
from websockets import ServerConnection
from utils.logger import Logger


class Broadcaster:
    def __init__(self) -> None:
        self.clients: Set[ServerConnection] = set()
        self.logger = Logger().get_logger()

    async def register(self, websocket: ServerConnection) -> None:
        try:
            self.clients.add(websocket)
        except Exception as err:
            self.logger.error(f"[broacaster] Could not register client: {err}")

    async def unregister(self, websocket: ServerConnection) -> None:
        try:
            self.clients.discard(websocket)
        except Exception as err:
            self.logger.error(f"[broacaster] Could not unregister client: {err}")

    async def broadcast(self, message: dict) -> None:
        try:
            if not self.clients:
                return

            payload = json.dumps(message)
            await asyncio.gather(
                *[client.send(payload) for client in self.clients],
                return_exceptions=True,
            )
        except Exception as err:
            self.logger.error(f"[broacaster] Could not broadcast: {err}")
