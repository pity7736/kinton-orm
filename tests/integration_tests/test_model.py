from unittest.mock import AsyncMock

import asyncpg
from pytest import mark, fixture

from kinton import Model, fields


class Category(Model):
    _id = fields.IntegerField()
    _name = fields.CharField()
    _description = fields.CharField()


@fixture
def db_connection(db_connection, mocker):
    connection_mock = mocker.patch.object(asyncpg, 'connect', new_callable=AsyncMock)
    connection_mock.return_value = db_connection
    return db_connection


@fixture
async def category_fixture(db_connection):
    return await Category.create(
        name='test name',
        description='test description'
    )


@mark.asyncio
async def test_get_by_id(category_fixture):
    category = await Category.get(id=category_fixture.id)

    assert category.id == category_fixture.id
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_get_by_name(category_fixture):
    category = await Category.get(name='test name')

    assert category.id == category_fixture.id
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_get_by_id_and_name(category_fixture):
    category = await Category.get(
        name='test name',
        description='test description'
    )

    assert category.id == category_fixture.id
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_get_without_params(category_fixture):
    category = await Category.get()
    assert category.id == category_fixture.id
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_save(db_connection):
    new_category = Category(name='test name', description='test description')
    await new_category.save()

    category = await Category.get(id=new_category.id)
    assert category.id == new_category.id
    assert category.name == new_category.name
    assert category.description == new_category.description


@mark.asyncio
async def test_save_with_values_by_setters(db_connection):
    new_category = Category()
    new_category.name = 'test name'
    new_category.description = 'test description'
    await new_category.save()

    category = await Category.get(id=new_category.id)
    assert category.id == new_category.id
    assert category.name == new_category.name
    assert category.description == new_category.description


@mark.asyncio
async def test_create(db_connection):
    new_category = await Category.create(
        name='test name',
        description='test description'
    )

    category = await Category.get(id=new_category.id)
    assert category.id == new_category.id
    assert category.name == new_category.name
    assert category.description == new_category.description


values = (
    ('new test name', 'new test name'),
    (12345, '12345')
)


@mark.parametrize('name, result_name', values)
@mark.asyncio
async def test_update_with_save(name, result_name, category_fixture):
    old_name = category_fixture.name
    id = category_fixture.id
    category_fixture.name = name
    await category_fixture.save()

    category = await Category.get(id=id)
    assert category.id == category_fixture.id
    assert category.name != old_name
    assert category.name == result_name
    assert category.description == category_fixture.description


@mark.asyncio
async def test_update_specific_fields(category_fixture):
    old_description = category_fixture.description
    old_name = category_fixture.name
    category_fixture.description = 'new test description'
    category_fixture.name = 'new test name'
    await category_fixture.save(update_fields=('description',))

    category = await Category.get(id=category_fixture.id)

    assert category.name == old_name
    assert category.description != old_description
    assert category.description == 'new test description'


@mark.asyncio
async def test_update_specific_fields_with_non_existent_fields(category_fixture):
    old_description = category_fixture.description
    old_name = category_fixture.name
    category_fixture.description = 'new test description'
    category_fixture.name = 'new test name'
    await category_fixture.save(update_fields=('description', 'non_existent_field'))

    category = await Category.get(id=category_fixture.id)

    assert category.name == old_name
    assert category.description != old_description
    assert category.description == 'new test description'
