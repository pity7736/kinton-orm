import os

import asyncpg
from asyncpg import Connection
from nyoibo import Entity


class Model(Entity):

    @classmethod
    async def get(cls, id=None, name=None):
        if id:
            field = 'id'
            param = id
        else:
            field = 'name'
            param = name

        sql = f'select * from categories where {field} = $1'
        connection: Connection = await asyncpg.connect(
            host=os.environ['KINTON_HOST'],
            user=os.environ['KINTON_USER'],
            database=os.environ['KINTON_DATABASE'],
            password=os.environ['KINTON_PASSWORD'],
            port=int(os.environ['KINTON_PORT']),
        )
        result = await connection.fetchrow(sql, param)
        return cls(**result)
