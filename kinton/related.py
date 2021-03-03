from kinton.db_client import DBClient
from kinton.queryset import QuerySet


class Related:

    def __init__(self, from_instance, field_name, to_model):
        self._from_instance = from_instance
        self._field_name = field_name
        self._to_model = to_model

    async def fetch(self):
        instance_id = getattr(self._from_instance, f'{self._field_name}_id')
        instance = None
        if instance_id:
            instance = await QuerySet(model=self._to_model).get(id=instance_id)
        setattr(self._from_instance, self._field_name, instance)


class ManyToManyRelated:

    def __init__(self, from_instance, field_name, to_model):
        self._from_instance = from_instance
        self._field_name = field_name
        self._to_model = to_model

    async def add(self, related):
        db_client = DBClient()
        table_name = f'{self._from_instance.meta.db_table}_' \
                     f'{self._to_model.meta.db_table}'
        query = f'insert into {table_name} ({self._from_instance.meta.db_table}_id,' \
                f'{self._to_model.meta.db_table}_id) values ($1, $2);'
        await db_client.insert(
            query,
            self._from_instance.id,
            related.id
        )
