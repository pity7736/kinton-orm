from nyoibo import fields

from kinton.related import Related, ManyToManyRelated


class Field:

    def __init__(self, **kwargs):
        kwargs.setdefault('immutable', False)
        super().__init__(**kwargs)


class CharField(Field, fields.StrField):
    pass


class IntegerField(Field, fields.IntField):
    pass


class ForeignKeyField(Field, fields.LinkField):
    _valid_values = (Related,)


class ManyToManyField(Field, fields.LinkField):
    _valid_values = (ManyToManyRelated,)
