from nyoibo import Entity

from kinton.utils import get_connection


class Model(Entity):

    @classmethod
    async def get(cls, **criteria):
        fields = tuple(criteria.keys())[0]
        sql = f'select * from categories where {fields} = $1'
        connection = await get_connection()
        result = await connection.fetchrow(sql, *criteria.values())
        return cls(**result)
