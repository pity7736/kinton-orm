from nyoibo import Entity

from kinton.utils import get_connection


class Model(Entity):

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        await obj.save()
        return obj

    async def save(self):
        fields = []
        values = []
        arguments = []
        i = 1
        for field in self._fields:
            if field != "_id":
                field_name = field.replace("_", "", 1)
                fields.append(field_name)
                values.append(f"${i}")
                arguments.append(getattr(self, field_name))
                i += 1

        fields = ", ".join(fields)
        values = ", ".join(values)
        connection = await get_connection()
        self._id = await connection.fetchval(
            f"insert into {self.__class__.__name__.lower()} ({fields}) values "
            f"({values}) returning id",
            *arguments,
        )

    @classmethod
    async def get(cls, **criteria):
        conditions = " AND ".join(
            [f"{field} = ${i}" for i, field in enumerate(criteria.keys(), start=1)]
        )
        sql = f"select * from {cls.__name__.lower()}"
        if conditions:
            sql += f" where {conditions}"

        connection = await get_connection()
        result = await connection.fetchrow(sql, *criteria.values())
        return cls(**result)
