from nyoibo import Entity

from kinton.db_client import DBClient
from .meta import MetaModel
from ..exceptions import FieldDoesNotExists
from ..fields import ForeignKeyField


class Model(Entity, metaclass=MetaModel):

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
        update_fields = update_fields or self.meta.fields.keys()
        for field_name in update_fields:
            field_name = field_name.replace("_", "", 1)
            field = self.meta.fields.get(f'_{field_name}')
            if field is None or field_name == 'id':
                continue
            fields.append(f'{field_name} = ${i}')
            values.append(getattr(self, field_name))
            i += 1
        fields = ', '.join(fields)
        values.append(self._id)
        sql = f'UPDATE {self.meta.db_table} SET {fields} WHERE id = ${i}'
        db_client = DBClient()
        await db_client.update(sql, *values)

    async def _insert(self):
        fields = []
        values = []
        arguments = []
        i = 1
        for field_name, field in self.meta.fields.items():
            if field_name.endswith('_id') is False:
                field_name = field_name.replace("_", "", 1)
                if isinstance(field, ForeignKeyField):
                    instance = getattr(self, field_name)
                    field_name = f'{field_name}_id'
                    if instance:
                        setattr(self, field_name, instance.id)
                fields.append(field_name)
                values.append(f"${i}")
                arguments.append(getattr(self, field_name))
                i += 1
        fields = ", ".join(fields)
        values = ", ".join(values)
        db_client = DBClient()
        self._id = await db_client.insert(
            f"insert into {self.meta.db_table} ({fields}) values "
            f"({values}) returning id",
            *arguments
        )
        return

    @classmethod
    async def get(cls, **criteria):
        conditions = " AND ".join(
            [f"{field} = ${i}" for i, field in enumerate(criteria.keys(), start=1)]
        )
        sql = f"select * from {cls.meta.db_table}"
        if conditions:
            sql += f" where {conditions}"

        db_client = DBClient()
        result = await db_client.select(sql, *criteria.values())
        return cls(**result[0])

    @classmethod
    async def all(cls):
        db_client = DBClient()
        records = await db_client.select(f'select * from {cls.meta.db_table}')
        result = [cls(**record) for record in records]
        return result

    @classmethod
    async def filter(cls, **kwargs):
        conditions = []
        for i, field_name in enumerate(kwargs.keys(), start=1):
            if hasattr(cls, field_name) is False:
                raise FieldDoesNotExists(f'{cls.meta.db_table} does not have '
                                         f'"{field_name}" field')
            conditions.append(f'{field_name} = ${i}')

        sql = f'SELECT * FROM {cls.meta.db_table}'
        if conditions:
            conditions = ' AND '.join(conditions)
            sql += f' WHERE {conditions}'

        db_client = DBClient()
        records = await db_client.select(sql, *kwargs.values())
        result = tuple((cls(**record) for record in records))
        return result
