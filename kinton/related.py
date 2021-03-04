from kinton.db_client import DBClient
from kinton.queryset import QuerySet
from kinton.queryset_result import QuerySetResult


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
        self._table_name = (
            f'{self._from_instance.meta.db_table}_{self._to_model.meta.db_table}'
        )

    async def add(self, *related):
        assert related
        db_client = DBClient()
        query = (
            f'insert into {self._table_name} '
            f'({self._from_instance.meta.db_table}_id, '
            f'{self._to_model.meta.db_table}_id) values'
        )
        values = []
        related_ids = []
        for i, related in enumerate(related, start=2):
            if isinstance(related, self._to_model) is False:
                raise ValueError(f'Related must be {self._to_model} instance, got '
                                 f'{type(related)} instead')
            values.append(f'($1, ${i})')
            related_ids.append(related.id)

        query += f' {", ".join(values)};'
        await db_client.insert(
            query,
            self._from_instance.id,
            *related_ids
        )

    async def all(self):
        query = f'select * from {self._table_name} where ' \
                f'{self._from_instance.meta.db_table}_id = $1'
        db_client = DBClient()
        records = await db_client.select(query, self._from_instance.id)
        return QuerySetResult(model=self._to_model, records=records)
