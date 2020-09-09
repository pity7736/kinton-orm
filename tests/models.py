from kinton import Model, fields


class Category(Model):
    _id = fields.IntegerField()
    _name = fields.CharField()
    _description = fields.CharField()


class Tag(Model):
    _id = fields.IntegerField()
    _name = fields.CharField()


class Post(Model):
    _id = fields.IntegerField()
    _title = fields.CharField()
    _category = fields.ForeignKeyField(to=Category)
    _tag = fields.ForeignKeyField(to=Tag)
