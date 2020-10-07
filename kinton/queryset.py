from kinton.db_client import DBClient
from kinton.exceptions import FieldDoesNotExists, ObjectDoesNotExists, \
    MultipleObjectsReturned


class QuerySet:

    def __init__(self, model):
        self._model = model
        self._criteria = {}
        self._get = False

    def __await__(self):
        return self._run_query().__await__()

    async def _run_query(self):
        conditions = []
        for i, field_name in enumerate(self._criteria.keys(), start=1):
            if hasattr(self._model, field_name) is False:
                raise FieldDoesNotExists(f'{self._model.meta.db_table} does not have '
                                         f'"{field_name}" field')
            conditions.append(f'{field_name} = ${i}')

        table_name = self._model.meta.db_table
        sql = f'SELECT * FROM {table_name}'
        if conditions:
            conditions = ' AND '.join(conditions)
            sql += f' WHERE {conditions}'

        db_client = DBClient()
        records = await db_client.select(sql, *self._criteria.values())
        if self._get:
            if not records:
                raise ObjectDoesNotExists('Object does not exists')
            if len(records) > 1:
                raise MultipleObjectsReturned(f'multiple objects {table_name} returned')
            return self._model(**records[0])
        return tuple((self._model(**record) for record in records))

    async def get_or_none(self, **criteria):
        try:
            return await self.get(**criteria)
        except (ObjectDoesNotExists, MultipleObjectsReturned):
            return None

    def get(self, **criteria):
        queryset = self.__class__(model=self._model)
        queryset._criteria = criteria
        queryset._get = True
        return queryset

    def all(self) -> 'QuerySet':
        return self.filter()

    def filter(self, **criteria) -> 'QuerySet':
        queryset = self.__class__(model=self._model)
        queryset._criteria = criteria
        return queryset
