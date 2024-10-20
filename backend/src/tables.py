from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.CharField(primary_key=True, max_length=26)
    username = fields.CharField(max_length=64, unique=True)
    family_name = fields.CharField(max_length=255)
    given_name = fields.CharField(max_length=255)
