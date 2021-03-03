from pytest import mark

from kinton.related import Related
from tests.models import Post


def test_foreign_key_field():
    post = Post()

    assert isinstance(post.category, Related)
    assert post.category_id is None
    assert isinstance(post.author, Related)
    assert post.author_id is None


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
    await post.author.fetch()

    assert post.id == created_post.id
    assert post.category.id == category_fixture.id
    assert post.author is None
