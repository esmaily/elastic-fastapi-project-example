import databases
import ormar

import sqlalchemy
from datetime import datetime
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



from app.core.elasticsearch import es,index_name
@ormar.post_save(Article)
async def after_save_article(sender, instance, **kwargs):
    article={
        "title": instance.title,
        "content": instance.content,
        "author": instance.author,
        "created_at": instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    es.index(index=index_name, body=article)


engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)
