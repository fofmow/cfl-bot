import ormar

from ..settings import BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta): ...
    
    id: int = ormar.Integer(primary_key=True)
    tg_id: int = ormar.Integer(minimum=0, unique=True, index=True)
