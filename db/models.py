from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.BigIntField()
    name = fields.CharField(max_length=100, default=1)
    username = fields.CharField(max_length=255, default=1)
    dificulity = fields.IntField(default=1)
    hod = fields.CharField(max_length=100)
    lives = fields.IntField(default=3)
    game_at = fields.DatetimeField()
    referral_id = fields.IntField(default=0)
    extra_life = fields.IntField(default=0)

    class Meta:
        table = "users"
