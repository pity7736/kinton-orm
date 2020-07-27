from kinton import Model, fields


def test_model():
    class Example(Model):
        _id = fields.IntegerField()
        _value = fields.CharField()

    example = Example(id=1, value='hi world')

    assert example.id == 1
    assert example.value == 'hi world'
