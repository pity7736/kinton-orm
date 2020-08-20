from nyoibo import Entity

from kinton.db_client import DBClient


class Model(Entity):

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        await obj.save()
        return obj

    async def save(self, update_fields=()):
        if self.id is None:
            return await self._insert()
        await self._update(update_fields)

    async def _update(self, update_fields=()):
        fields = []
        values = []
        i = 1
        update_fields = update_fields or self._fields.keys()
        for field_name in update_fields:
            field_name = field_name.replace("_", "", 1)
            field = self._fields.get(f'_{field_name}')
            if field is None or field_name == 'id':
                continue
            fields.append(f'{field_name} = ${i}')
            values.append(getattr(self, field_name))
            i += 1
        fields = ', '.join(fields)
        values.append(self._id)
        sql = f'UPDATE {self.__class__.__name__.lower()} SET {fields} WHERE id = ${i}'
        db_client = DBClient()
        await db_client.update(sql, *values)

    async def _insert(self):
        fields = []
        values = []
        i = 1
        arguments = []
        for field in self._fields:
            if field != "_id":
                field_name = field.replace("_", "", 1)
                fields.append(field_name)
                values.append(f"${i}")
                arguments.append(getattr(self, field_name))
                i += 1
        fields = ", ".join(fields)
        values = ", ".join(values)
        db_client = DBClient()
        self._id = await db_client.insert(
            f"insert into {self.__class__.__name__.lower()} ({fields}) values "
            f"({values}) returning id",
            *arguments
        )
        return

    @classmethod
    async def get(cls, **criteria):
        conditions = " AND ".join(
            [f"{field} = ${i}" for i, field in enumerate(criteria.keys(), start=1)]
        )
        sql = f"select * from {cls.__name__.lower()}"
        if conditions:
            sql += f" where {conditions}"

        db_client = DBClient()
        result = await db_client.select(sql, *criteria.values())
        return cls(**result[0])
