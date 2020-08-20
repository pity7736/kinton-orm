from kinton.utils import get_connection


class DBClient:

    async def insert(self, query, *values):
        connection = await get_connection()
        return await connection.fetchval(query, *values)

    async def update(self, query, *values):
        connection = await get_connection()
        await connection.execute(query, *values)

    async def select(self, query, *values):
        connection = await get_connection()
        return await connection.fetch(query, *values)
