from kinton.utils import get_connection


class DBClient:

    async def insert(self, query, *values):
        connection = await get_connection()
        result = await connection.fetchval(query, *values)
        await connection.close()
        return result

    async def update(self, query, *values):
        connection = await get_connection()
        await connection.execute(query, *values)
        await connection.close()

    async def select(self, query, *values):
        connection = await get_connection()
        result = await connection.fetch(query, *values)
        await connection.close()
        return result
