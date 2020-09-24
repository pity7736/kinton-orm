from kinton.queryset import QuerySet


class Related:

    def __init__(self, from_instance, field_name, to_model):
        self._from_instance = from_instance
        self._field_name = field_name
        self._to_model = to_model

    async def fetch(self):
        instance_id = getattr(self._from_instance, f'{self._field_name}_id')
        instance = await QuerySet(model=self._to_model).get(id=instance_id)
        setattr(self._from_instance, self._field_name, instance)
