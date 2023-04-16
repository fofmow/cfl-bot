import ormar
from ormar.queryset.queryset import QuerySet

from . import User
from ..settings import BaseMeta


class NoteCategoryExecutor(QuerySet):
    @staticmethod
    async def get_names(user: User) -> list[str]:
        return [cat.name for cat in await user.categories.all()]


class NoteCategory(ormar.Model):
    class Meta(BaseMeta):
        tablename = "note_categories"
        queryset_class = NoteCategoryExecutor
    
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=64)
    creator = ormar.ForeignKey(User, related_name="categories")
