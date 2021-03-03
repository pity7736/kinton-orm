from nyoibo import Entity

from kinton.db_client import DBClient
from kinton.fields import ForeignKeyField, ManyToManyField
from kinton.queryset import QuerySet
from kinton.related import Related, ManyToManyRelated
from .meta import MetaModel


class Model(Entity, metaclass=MetaModel):

    def _additional_value(self, key, field, value):
        if isinstance(field, ForeignKeyField) and value is None:
            return Related(from_instance=self, field_name=key, to_model=field.to)
        if isinstance(field, ManyToManyField):
            return ManyToManyRelated(
                from_instance=self,
                field_name=key,
                to_model=field.to
            )
        return value

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
            if field_name.endswith('_id') is False and \
                    isinstance(field, ManyToManyField) is False:
                field_name = field_name.replace("_", "", 1)
                if isinstance(field, ForeignKeyField):
                    instance = getattr(self, field_name)
                    field_name = f'{field_name}_id'
                    if isinstance(instance, field.to):
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
    def get_or_none(cls, **criteria):
        return QuerySet(model=cls).get_or_none(**criteria)

    @classmethod
    def get(cls, **criteria):
        return QuerySet(model=cls).get(**criteria)

    @classmethod
    def all(cls):
        return QuerySet(model=cls).all()

    @classmethod
    def filter(cls, **criteria):
        return QuerySet(model=cls).filter(**criteria)
