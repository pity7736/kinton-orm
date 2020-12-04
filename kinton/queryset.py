from kinton.db_client import DBClient
from kinton.exceptions import ObjectDoesNotExists, MultipleObjectsReturned
from kinton.queryset_result import QuerySetResult
from kinton.utils import validate_model_fields


class QuerySet:

    def __init__(self, model):
        self._model = model
        self._criteria = {}
        self._get = False
        self._fields = '*'

    def __await__(self):
        return self._run_query().__await__()

    async def _run_query(self):
        conditions = []
        validate_model_fields(self._model, self._criteria.keys())
        validate_model_fields(self._model, self._fields)
        for i, field_name in enumerate(self._criteria.keys(), start=1):
            conditions.append(f'{field_name} = ${i}')

        table_name = self._model.meta.db_table
        sql = f'SELECT {self._fields} FROM {table_name}'
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
        return QuerySetResult(model=self._model, records=records)

    async def get_or_none(self, **criteria):
        try:
            return await self.get(**criteria)
        except (ObjectDoesNotExists, MultipleObjectsReturned):
            return None

    def only(self, *fields) -> 'QuerySet':
        queryset = self.__class__(model=self._model)
        queryset._get = self._get
        queryset._criteria = self._criteria
        queryset._fields = ', '.join(fields)
        return queryset

    def all(self) -> 'QuerySet':
        return self.filter()

    def filter(self, **criteria) -> 'QuerySet':
        queryset = self.__class__(model=self._model)
        queryset._criteria = self._get_new_criteria(criteria)
        return queryset

    def get(self, **criteria) -> 'QuerySet':
        queryset = self.__class__(model=self._model)
        queryset._criteria = self._get_new_criteria(criteria)
        queryset._get = True
        return queryset

    def _get_new_criteria(self, criteria):
        new_criteria = self._criteria.copy()
        new_criteria.update(**criteria)
        return new_criteria
