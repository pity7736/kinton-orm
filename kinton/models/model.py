from nyoibo import Entity

from kinton.utils import get_connection


class Model(Entity):

    @classmethod
    async def get(cls, **criteria):
        conditions = " AND ".join(
            [f"{field} = ${i}" for i, field in enumerate(criteria.keys(), start=1)]
        )
        sql = "select * from categories"
        if conditions:
            sql += f' where {conditions}'

        connection = await get_connection()
        result = await connection.fetchrow(sql, *criteria.values())
        return cls(**result)
