from tortoise import Model
from tortoise.fields import IntField, TextField, BooleanField, BigIntField, DatetimeField, FloatField

class Sales(Model):
    id = IntField(pk=True)

    user_id = BigIntField(null=False)
    username = TextField(null=True, default='none')
    book_id = IntField(null=False)
    price = FloatField(null=False)
    address = TextField(null=True, default='none')
    telephone = TextField(null=True, default='none')
    email = TextField(null=True, default='none')
    purchase_date = DatetimeField(auto_now_add=True)
    status = TextField(default='Обработка заказа')
    finished = BooleanField(default=False)

    class Meta:
        table = 'sales'
