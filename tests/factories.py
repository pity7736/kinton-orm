import factory

from tests.models import Category


class CategoryFactory(factory.Factory):
    name = 'test name'
    description = 'test name'

    class Meta:
        model = Category

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create():
            return await model_class.create(**kwargs)
        return create()
