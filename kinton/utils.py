import os
import re

import asyncpg
from asyncpg import Connection

from kinton.exceptions import FieldDoesNotExists


async def get_connection() -> Connection:
    connection = await asyncpg.connect(
        host=os.environ["KINTON_HOST"],
        user=os.environ["KINTON_USER"],
        database=os.environ["KINTON_DATABASE"],
        password=os.environ["KINTON_PASSWORD"],
        port=int(os.environ["KINTON_PORT"]),
    )
    return connection


def camel_case_to_snake_case(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def validate_model_fields(model, fields):
    if fields != '*':
        if isinstance(fields, str):
            fields = fields.split(', ')
        for field in fields:
            if hasattr(model, field) is False:
                raise FieldDoesNotExists(f'{model.meta.db_table} does not have '
                                         f'"{field}" field')
