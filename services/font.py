#!/usr/bin/env python3

import os
import asyncio
from typing import List, Tuple, Optional
import random
from redis.asyncio import Redis

from utils.redis import connect_redis
from utils.logger import Logger
from errors.ConnectionError import RedisConnectionError


class FontService:
    def __init__(self, client: Redis, key: str) -> None:
        self.client = client
        self.key = key
        self.logger = Logger().get_logger()

    @classmethod
    async def create(cls, key: str) -> "FontService":
        try:
            client = await connect_redis(
                os.getenv("REDIS_HOST"),
                os.getenv("REDIS_PASSWORD"),
            )
            return cls(client, key)
        except RedisConnectionError as conn_err:
            Logger().get_logger().error(
                f"[fonts] Could not connect to redis: {conn_err}"
            )
            raise

    async def add(self, font: str, elo: float) -> None:
        try:
            await self.client.zadd(self.key, {font: elo})
            self.logger.info(
                f"[fonts] Added font '{font}' with ELO {elo}"
            )
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while adding {font}: {err}"
            )

    async def get_elo(self, font: str) -> Optional[float]:
        try:
            elo = await self.client.zscore(self.key, font)
            self.logger.debug(
                f"[fonts] Retrieved ELO for '{font}': {elo}"
            )
            return elo
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while getting elo for {font}: {err}"
            )
            return None
    
    async def head_on_head(self) -> List[Tuple[str, float]]:
        try:
            count = await self.client.zcard(self.key)
            if count < 2:
                self.logger.warning(
                    "[fonts] Not enough fonts for head-to-head"
                )
                return []

            i, j = random.sample(range(count), 2)
            results = []
            for idx in (i, j):
                entry = await self.client.zrevrange(
                    self.key, idx, idx, withscores=True
                )
                if entry:
                    results.append(entry[0])

            self.logger.debug(
                f"[fonts] Head-to-head matchup: {results}"
            )
            return results
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while finding head-to-head: {err}"
            )
            return []

    async def update_elo(self, font: str, new_elo: float) -> None:
        try:
            await self.client.zadd(self.key, {font: new_elo})
            self.logger.info(
                f"[fonts] Updated ELO for '{font}' → {new_elo}"
            )
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while updating elo for {font}: {err}"
            )

    async def increment_elo(self, font: str, delta: float) -> Optional[float]:
        try:
            new_elo = await self.client.zincrby(self.key, delta, font)
            self.logger.info(
                f"[fonts] Incremented ELO for '{font}' by {delta} → {new_elo}"
            )
            return new_elo
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while incrementing elo for {font}: {err}"
            )
            return None

    async def leaderboard(
        self,
        start: int = 0,
        end: int = -1,
        descending: bool = True,
    ) -> List[Tuple[str, float]]:
        try:
            if descending:
                board = await self.client.zrevrange(
                    self.key, start, end, withscores=True
                )
            else:
                board = await self.client.zrange(
                    self.key, start, end, withscores=True
                )

            self.logger.debug(
                f"[fonts] Retrieved leaderboard entries {start}..{end}"
            )
            return board
        except Exception as err:
            self.logger.error(
                f"[fonts] Uncaught exception while fetching leaderboard: {err}"
            )
            return []


if __name__ == "__main__":
    async def main():
        font_service = await FontService.create("font_leaderboard")

        head_on_head = await font_service.head_on_head()

    asyncio.run(main())
