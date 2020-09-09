from nyoibo.entities.meta_entity import MetaEntity

from kinton import fields
from kinton.fields import ForeignKeyField
from kinton.utils import camel_case_to_snake_case


class Meta:

    __slots__ = ('_fields', '_db_table')

    def __init__(self, model):
        self._fields = model._fields
        self._db_table = camel_case_to_snake_case(model.__name__)

    @property
    def fields(self):
        return self._fields

    @property
    def db_table(self):
        return self._db_table

    @db_table.setter
    def db_table(self, value):
        self._db_table = value


class MetaModel(MetaEntity):

    def __new__(mcs, name, bases, namespace):
        meta_class = namespace.pop('Meta', None)
        foreign_key_ids = {}
        for attr, field in namespace.items():
            if isinstance(field, ForeignKeyField):
                new_attr = f'{attr}_id'
                foreign_key_ids[new_attr] = fields.IntegerField()

        namespace.update(foreign_key_ids)
        cls = super().__new__(mcs, name, bases, namespace)
        meta = Meta(model=cls)
        if meta_class:
            meta.db_table = meta_class.db_table
        cls.meta = meta
        return cls
