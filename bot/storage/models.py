import databases
import ormar
import sqlalchemy
from config import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta): ...
    
    id: int = ormar.Integer(primary_key=True)
    tg_id: int = ormar.Integer(minimum=0, unique=True, index=True)
    
    def __str__(self):
        return f"User {self.full_name} (@{self.username}, ID {self.id})\n"


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
