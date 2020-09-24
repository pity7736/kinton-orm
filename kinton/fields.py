from nyoibo import fields
from nyoibo.fields import LinkField

from kinton.related import Related


class Field:

    def __init__(self, **kwargs):
        kwargs.setdefault('immutable', False)
        super().__init__(**kwargs)


class CharField(Field, fields.StrField):
    pass


class IntegerField(Field, fields.IntField):
    pass


class ForeignKeyField(Field, LinkField):
    _valid_values = (Related,)
