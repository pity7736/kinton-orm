from kinton.db_client import DBClient
from kinton.exceptions import FieldDoesNotExists, ObjectDoesNotExists


class QuerySet:

    def __init__(self, model):
        self._model = model

    async def all(self):
        db_client = DBClient()
        records = await db_client.select(f'select * from {self._model.meta.db_table}')
        result = [self._model(**record) for record in records]
        return result

    async def get(self, **criteria):
        conditions = " AND ".join(
            [f"{field} = ${i}" for i, field in enumerate(criteria.keys(), start=1)]
        )
        sql = f"select * from {self._model.meta.db_table}"
        if conditions:
            sql += f" where {conditions}"

        db_client = DBClient()
        result = await db_client.select(sql, *criteria.values())
        if not result:
            raise ObjectDoesNotExists('Object does not exists')
        return self._model(**result[0])

    async def filter(self, **criteria):
        conditions = []
        for i, field_name in enumerate(criteria.keys(), start=1):
            if hasattr(self._model, field_name) is False:
                raise FieldDoesNotExists(f'{self._model.meta.db_table} does not have '
                                         f'"{field_name}" field')
            conditions.append(f'{field_name} = ${i}')

        sql = f'SELECT * FROM {self._model.meta.db_table}'
        if conditions:
            conditions = ' AND '.join(conditions)
            sql += f' WHERE {conditions}'

        db_client = DBClient()
        records = await db_client.select(sql, *criteria.values())
        result = tuple((self._model(**record) for record in records))
        return result
