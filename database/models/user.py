from tortoise import Model
from tortoise.fields import IntField, TextField, DateField, BooleanField, BigIntField

class User(Model):
    id = IntField(pk=True)

    type = TextField(default='user')

    user_id = BigIntField(unique=True)
    username = TextField(null=True)

    class Meta:
        table = 'user'

    @property
    def is_admin(self):
        return self.type == 'admin'
