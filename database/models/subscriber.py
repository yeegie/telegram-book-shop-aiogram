from tortoise import Model
from tortoise.fields import IntField, TextField, BooleanField, BigIntField, DatetimeField

class Subscriber(Model):
    id = IntField(pk=True)

    user_id = BigIntField(unique=True)
    is_active = BooleanField(null=False)

    date_start = DatetimeField()
    date_end = DatetimeField()

    class Meta:
        table = 'subscriber'
