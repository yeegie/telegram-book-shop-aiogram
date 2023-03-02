from tortoise import Model
from tortoise.fields import IntField, TextField, DateField, BooleanField

class Book(Model):
    id = IntField(pk=True)

    title = TextField(null=False)
    description = TextField(null=False)
    author = TextField(null=False)
    genre = TextField(null=False)
    releaseDate = TextField(null=False)

    price = IntField(null=False)

    limited = BooleanField(null=True)
    quantity = IntField(null=True)

    likes = IntField(null=True)
    dislikes = IntField(null=True)

    photo = TextField(null=True)

    class Meta:
        table = 'book'
