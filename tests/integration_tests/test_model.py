from pytest import mark, fixture, raises

from kinton import Model, fields
from kinton.exceptions import FieldDoesNotExists, ObjectDoesNotExists, \
    MultipleObjectsReturned
from kinton.related import Related
from tests.factories import CategoryFactory
from tests.models import Category, Post


# TODO:
# related queries
# connection pool
# prefetch related objects
# backwards queries
# testing utils
# OR queries
# many to many relationship
#


@fixture
async def category_fixture(db_connection):
    return await CategoryFactory.create(
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


def test_override_db_table():
    class SomeModel(Model):
        _value = fields.CharField()

        class Meta:
            db_table = 'another_table_name'

    assert SomeModel.meta.db_table == 'another_table_name'


model_names = (
    ('SomeModel', 'some_model'),
    ('Category', 'category'),
    ('NameOfModel', 'name_of_model'),
    ('Rate1', 'rate1'),
    ('Rate1OrRate2', 'rate1_or_rate2'),
)


@mark.parametrize('model_name, db_table', model_names)
def test_db_table_name(model_name, db_table):
    SomeModel = type(model_name, (Model,), {})
    assert SomeModel.meta.db_table == db_table


@mark.asyncio
async def test_all(db_connection):
    for i in range(5):
        await CategoryFactory.create(
            name=f'name test {i}',
            description=f'description test {i}'
        )

    categories = await Category.all()
    assert len(categories) == 5


@mark.asyncio
async def test_filter(category_fixture):
    categories = await Category.filter(name='test name')

    category = categories[0]
    assert len(categories) == 1
    assert category.name == 'test name'
    assert category.description == 'test description'


@mark.asyncio
async def test_filter_without_records(db_connection):
    categories = await Category.filter(name='test')
    assert categories == ()


@mark.asyncio
async def test_filter_without_conditions(db_connection):
    for _ in range(5):
        await CategoryFactory.create()

    categories = await Category.filter()
    assert len(categories) == 5


@mark.asyncio
async def test_with_from_field_condition(db_connection):
    with raises(FieldDoesNotExists) as e:
        await Category.filter(non_existing_field='hi')
    assert str(e.value) == 'category does not have "non_existing_field" field'


def test_foreign_key_field():
    post = Post()

    assert isinstance(post.category, Related)
    assert post.category_id is None
    assert isinstance(post.tag, Related)
    assert post.tag_id is None


@mark.asyncio
async def test_create_with_foreign_key_field(category_fixture):
    post = await Post.create(title='post title', category=category_fixture)

    assert post.category == category_fixture
    assert post.category_id == category_fixture.id


@mark.asyncio
async def test_create_with_foreign_key_field_id(category_fixture):
    post = await Post.create(title='post title', category_id=category_fixture.id)

    assert isinstance(post.category, Related)
    assert post.category_id == category_fixture.id


@mark.asyncio
async def test_get_related_object(category_fixture):
    created_post = await Post.create(title='test title', category=category_fixture)

    post = await Post.get(title='test title')
    await post.category.fetch()
    await post.tag.fetch()

    assert post.id == created_post.id
    assert post.category.id == category_fixture.id
    assert post.tag is None


@mark.asyncio
async def test_raise_object_does_not_exitst_in_get_query(db_connection):
    with raises(ObjectDoesNotExists) as e:
        await Category.get(id=1)

    assert str(e.value) == 'Object does not exists'


@mark.asyncio
async def test_get_or_none(db_connection):
    assert await Category.get_or_none(id=1) is None


@mark.asyncio
async def test_get_or_none_with_multiple_objects(db_connection):
    await CategoryFactory.create(name='test')
    await CategoryFactory.create(name='test')
    assert await Category.get_or_none(name='test') is None


@mark.asyncio
async def test_get_multiple_objects_returned(db_connection):
    await CategoryFactory.create(name='test')
    await CategoryFactory.create(name='test')
    with raises(MultipleObjectsReturned):
        await Category.get(name='test')
