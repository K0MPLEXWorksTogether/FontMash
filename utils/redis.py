#!/usr/bin/env python3

import redis.asyncio as redis
import redis.asyncio.client as Redis
import os
import asyncio

from errors import RedisConnectionError
from utils.logger import Logger


async def connect_redis(host: str, password: str) -> Redis:
    client: Redis = redis.Redis(
        host=host,
        port=17664,
        decode_responses=True,
        username="default",
        password=password,
    )
    logger = Logger().get_logger()

    try:
        pong: bool = await client.ping()
        if not pong:
            raise RedisConnectionError("[redis] Redis did not respond to PING.")

        logger.info("[redis] Connected successfully to Redis!")
        return client

    except RedisConnectionError as err:
        logger.error(str(err))
        await client.close()
        raise

    except redis.AuthenticationError as err:
        logger.error(str(err))
        await client.close()
        raise

    except Exception as err:
        logger.exception(f"[redis] Unexpected error while connecting: {err}")
        await client.close()
        raise RedisConnectionError("[redis] Failed to connect to Redis") from err

if __name__ == '__main__':
    asyncio.run(connect_redis(os.getenv('REDIS_HOST'), os.getenv('REDIS_PASSWORD')))