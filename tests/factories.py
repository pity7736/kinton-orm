import factory

from tests.models import Category, Tag, Author


class CreateMixin:

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create():
            return await model_class.create(**kwargs)
        return create()

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class CategoryFactory(CreateMixin, factory.Factory):
    name = 'test name'
    description = 'test name'

    class Meta:
        model = Category


class TagFactory(CreateMixin, factory.Factory):
    name = factory.Sequence(lambda n: f'tag-{n}')

    class Meta:
        model = Tag


class AuthorFactory(CreateMixin, factory.Factory):
    name = factory.Faker('name')

    class Meta:
        model = Author
