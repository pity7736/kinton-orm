import asyncio
import os
from unittest.mock import AsyncMock

import asyncpg
import uvloop
from asyncpg import Connection
from asyncpg.pool import Pool
from asyncpg.transaction import Transaction
from pytest import fixture

from tests.factories import CategoryFactory


@fixture(scope='session')
def schema():
    sql_file = f'{os.path.dirname(__file__)}/db.sql'
    with open(sql_file) as f:
        sql = f.read()
    print('sql', sql)
    return sql


@fixture(scope='session')
def event_loop():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@fixture(scope='session')
async def db_pool():
    pool: Pool = await asyncpg.create_pool(
        host=os.environ['KINTON_HOST'],
        user=os.environ['KINTON_USER'],
        database=os.environ['KINTON_DATABASE'],
        password=os.environ['KINTON_PASSWORD'],
        port=int(os.environ['KINTON_PORT']),
        min_size=2
    )
    print('pool created')
    close = Connection.close
    Connection.close = AsyncMock()
    yield pool
    print('closing pool')
    Connection.close = close
    await pool.close()
    print('pool closed')


@fixture
async def db_connection(db_pool, schema, mocker):
    connection: Connection = await db_pool.acquire()
    transaction: Transaction = connection.transaction()
    connect_mock = mocker.patch.object(asyncpg, 'connect', new_callable=AsyncMock)
    connect_mock.return_value = connection
    await transaction.start()
    await connection.execute(schema)
    yield connection
    print('doing rollback')
    await transaction.rollback()
    print('rollback done!')
    print('releasing connection')
    await db_pool.release(connection)


@fixture
async def category_fixture(db_connection):
    return await CategoryFactory.create(
        name='test name',
        description='test description'
    )
