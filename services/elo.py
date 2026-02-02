#!/usr/bin/env python3

import math
import asyncio
from typing import Tuple

from services.font import FontService
from utils.logger import Logger


class ELOService:
    def __init__(self, font_service: FontService) -> None:
        self.font_service = font_service
        self.logger = Logger().get_logger()

    @classmethod
    async def create(cls) -> "ELOService":
        font_service = await FontService.create("font_leaderboard")
        return cls(font_service)

    @staticmethod
    def probability(rating_a: float, rating_b: float) -> float:
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))

    @classmethod
    def calculate(
        cls,
        r_a: float,
        r_b: float,
        k: float,
        outcome: int,
    ) -> Tuple[float, float]:
        p_a = cls.probability(r_a, r_b)
        p_b = cls.probability(r_b, r_a)

        new_r_a = r_a + k * (outcome - p_a)
        new_r_b = r_b + k * ((1 - outcome) - p_b)

        return new_r_a, new_r_b

    async def update_elo(
        self,
        font_a: str,
        font_b: str,
        outcome: int,
        k: float = 32.0,
    ) -> None:
        try:
            r_a = await self.font_service.get_elo(font_a)
            r_b = await self.font_service.get_elo(font_b)

            if r_a is None or r_b is None:
                self.logger.warning(
                    f"[elo] Missing ELO rating for '{font_a}' or '{font_b}'"
                )
                return

            new_r_a, new_r_b = self.calculate(r_a, r_b, k, outcome)

            await self.font_service.update_elo(font_a, new_r_a)
            await self.font_service.update_elo(font_b, new_r_b)

            self.logger.info(
                f"[elo] Match result: {font_a} vs {font_b} | "
                f"outcome={outcome} | "
                f"{r_a:.1f}->{new_r_a:.1f}, {r_b:.1f}->{new_r_b:.1f}"
            )

        except Exception as err:
            self.logger.error(f"[elo] Failed to update ELO: {err}")

if __name__ == "__main__":
    async def main() -> None:
        elo_service = await ELOService.create()
        font_a = "JetBrains Mono"
        font_b = "Fira Code"

        await elo_service.update_elo(font_a, font_b, 1)

    asyncio.run(main())