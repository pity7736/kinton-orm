from nyoibo import fields


class Field:

    def __init__(self, private=False, immutable=False, default_value=None,
                 choices=None):
        super().__init__(
            private=private,
            immutable=immutable,
            default_value=default_value,
            choices=choices,
        )


class CharField(Field, fields.StrField):
    pass


class IntegerField(Field, fields.IntField):
    pass
