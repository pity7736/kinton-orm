from pytest import mark, raises

from tests.factories import AuthorFactory, TagFactory
from tests.models import Post, Tag


@mark.asyncio
async def test_add_related(category_fixture, db_connection):
    author = await AuthorFactory.create()
    tag = await TagFactory.create()
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    await post.tag.add(tag)

    result = await db_connection.fetchrow(
        'select * from post_tag where post_id = $1 and tag_id = $2',
        post.id,
        tag.id
    )
    assert result['post_id'] == post.id
    assert result['tag_id'] == tag.id


@mark.asyncio
async def test_add_several_related(category_fixture, db_connection):
    author = await AuthorFactory.create()
    tags = await TagFactory.create_batch(2)
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    await post.tag.add(*tags)

    result = await post.tag.all()
    assert len(result) == 2


@mark.asyncio
async def test_add_several_related_with_more_created(category_fixture, db_connection):
    author = await AuthorFactory.create()
    tag1, tag2, tag3 = await TagFactory.create_batch(3)
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    await post.tag.add(tag1, tag2)

    result = await post.tag.all()
    assert len(result) == 2


@mark.asyncio
async def test_add_empty(category_fixture):
    author = await AuthorFactory.create()
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    with raises(AssertionError):
        await post.tag.add()


@mark.asyncio
async def test_add_wrong_values(category_fixture):
    author = await AuthorFactory.create()
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    with raises(ValueError) as e:
        await post.tag.add(1, 2, 'hi')

    assert str(e.value) == "Related must be <class 'tests.models.Tag'> instance, got " \
                           "<class 'int'> instead"


@mark.asyncio
async def test_all(category_fixture):
    author = await AuthorFactory.create()
    tag1, tag2, tag3 = await TagFactory.create_batch(3)
    post = await Post.create(
        title='post title',
        category=category_fixture,
        author=author
    )
    await post.tag.add(tag1, tag2)

    result = await post.tag.all()
    assert len(result) == 2
    for tag in result:
        assert isinstance(tag, Tag)
        assert tag.id
        assert tag.name
