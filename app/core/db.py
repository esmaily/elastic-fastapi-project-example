import databases
import ormar

import sqlalchemy
from datetime import datetime
# from pydantic import datetime
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
    title: str = ormar.String(max_length=255, nullable=False)
    content: str = ormar.Text(nullable=False)
    author: str = ormar.String(max_length=150, nullable=False)
    created_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)
    updated_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)


engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)
