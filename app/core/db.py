import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)

class Article(ormar.Model):
    class Meta(BaseMeta):
        tablename = "articles"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=155,  nullable=False)
    content: bool = ormar.Boolean(default=True, nullable=False)
    author: bool = ormar.Boolean(default=True, nullable=False)
    created_at: bool = ormar.Boolean(default=True, nullable=False)

engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)