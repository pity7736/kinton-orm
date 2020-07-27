from unittest.mock import AsyncMock

import asyncpg
from pytest import mark

from kinton import Model, fields


class Category(Model):
    _id = fields.IntegerField()
    _name = fields.CharField()
    _description = fields.CharField()


@mark.asyncio
async def test_get_by_id(db_connection, mocker):
    connection_mock = mocker.patch.object(asyncpg, 'connect',
                                          new_callable=AsyncMock)
    connection_mock.return_value = db_connection
    result_id = await db_connection.fetchval(
        'insert into categories ("name", "description") values ($1, $2) '
        'returning id',
        "test name",
        "test description"
    )

    category = await Category.get(id=result_id)

    assert category.id == result_id
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_get_by_name(db_connection, mocker):
    connection_mock = mocker.patch.object(asyncpg, 'connect',
                                          new_callable=AsyncMock)
    connection_mock.return_value = db_connection
    result_id = await db_connection.fetchval(
        'insert into categories ("name", "description") values ($1, $2) '
        'returning id',
        "test name",
        "test description"
    )
    category = await Category.get(name='test name')

    assert category.id == result_id
    assert category.name == 'test name'
    assert category.description == 'test description'
