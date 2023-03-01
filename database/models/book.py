from tortoise import Model
from tortoise.fields import IntField, TextField, DateField, BooleanField

class Book(Model):
    id = IntField(pk=True)

    title = TextField(null=False)
    description = TextField(null=False)
    author = TextField(null=False)
    genre = TextField(null=False)
    releaseDate = DateField(null=False)

    price = IntField(null=False)

    limited = BooleanField(null=False)
    quantity = IntField()

    likes = IntField()
    dislikes = IntField()

    photo = TextField(null=False)

    class Meta:
        table = 'book'
