import os

import asyncpg
from asyncpg import Connection


async def get_connection() -> Connection:
    connection = await asyncpg.connect(
        host=os.environ["KINTON_HOST"],
        user=os.environ["KINTON_USER"],
        database=os.environ["KINTON_DATABASE"],
        password=os.environ["KINTON_PASSWORD"],
        port=int(os.environ["KINTON_PORT"]),
    )
    return connection
