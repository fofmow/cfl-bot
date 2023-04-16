from datetime import datetime

import ormar
from ormar.queryset.queryset import QuerySet

from .note_category import NoteCategory
from .user import User
from ..settings import BaseMeta


class NoteReminderLevel:
    LESS_19_MINUTES = 0
    NINETEEN_MINUTES = 1
    ONE_HOUR = 2
    NINE_HOURS = 3
    ONE_DAY = 4
    SIX_DAYS = 5
    THIRTY_DAYS = 6
    ONE_HUNDRED_DAYS = 7


class NoteExecutor(QuerySet):
    @staticmethod
    async def get_names(user: User) -> list[str]:
        return [note.name for note in await user.notes.filter(is_completed=False).all()]


class Note(ormar.Model):
    class Meta(BaseMeta):
        queryset_class = NoteExecutor
    
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128)
    content: str = ormar.Text()
    reminder_level = ormar.SmallInteger(default=NoteReminderLevel.LESS_19_MINUTES)
    creation_dt = ormar.DateTime(default=datetime.utcnow)
    creator = ormar.ForeignKey(User, related_name="notes")
    category = ormar.ForeignKey(NoteCategory)
    is_completed = ormar.Boolean(default=False)
