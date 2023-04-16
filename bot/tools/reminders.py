from datetime import datetime, timedelta
from typing import Iterable

from aiogram.utils.markdown import hspoiler

from buttons import remember_note_button
from storage.models import User
from storage.models.note import NoteReminderLevel, Note
from tools.misc import choice_random_signature, send_text_from_bot
from tools.note_signatures import *


async def get_notes_created_ago(
        current_status: NoteReminderLevel,
        minutes_passed: int | None = None,
        days_passed: int | None = None
) -> list[Note] | None:
    if minutes_passed and days_passed:
        raise ValueError("Give only one parameter (minutes_passed or days_passed)!")
    
    if days_passed:
        minutes_passed = days_passed * 24 * 60
    
    need_status_notes = await Note.objects.filter(
        reminder_level=current_status,
        is_completed=False
    ).all()
    
    now = datetime.utcnow()
    return [note for note in need_status_notes if (note.creation_dt + timedelta(minutes=minutes_passed)) < now]


async def get_notes_sorted_by_periods():
    more_19_minutes = await get_notes_created_ago(NoteReminderLevel.LESS_19_MINUTES, minutes_passed=19)
    more_1_hour = await get_notes_created_ago(NoteReminderLevel.NINETEEN_MINUTES, minutes_passed=60)
    more_9_hours = await get_notes_created_ago(NoteReminderLevel.ONE_HOUR, minutes_passed=540)
    more_1_day = await get_notes_created_ago(NoteReminderLevel.NINE_HOURS, days_passed=1)
    more_6_days = await get_notes_created_ago(NoteReminderLevel.ONE_DAY, days_passed=6)
    more_30_days = await get_notes_created_ago(NoteReminderLevel.SIX_DAYS, days_passed=30)
    more_100_days = await get_notes_created_ago(NoteReminderLevel.THIRTY_DAYS, days_passed=100)
    return more_19_minutes, more_1_hour, more_9_hours, more_1_day, more_6_days, more_30_days, more_100_days


async def remind_users_about_notes():
    more_19_minutes, more_1_hour, more_9_hours, more_1_day, more_6_days, more_30_days, more_100_days = \
        await get_notes_sorted_by_periods()
    
    signatures = {
        "more_19_minutes": NINETEEN_MINUTES_SIGNATURES,
        "more_1_hour": ONE_HOUR_SIGNATURES,
        "more_9_hours": NINE_HOURS_SIGNATURES,
        "more_1_day": ONE_DAY_SIGNATURES,
        "more_6_days": SIX_DAYS_SIGNATURES,
        "more_30_days": THIRTY_DAYS_SIGNATURES,
        "more_100_days": ONE_HUNDRED_DAYS_SIGNATURES,
    }
    for k, v in signatures.items():
        if k in locals().keys():
            signature = await choice_random_signature(v)
            await send_messages_to_users(locals().get(k), signature)
    
    await change_notes_status_after_notification(
        more_19_minutes, more_1_hour, more_9_hours, more_1_day, more_6_days, more_30_days, more_100_days
    )


async def send_messages_to_users(notes: Iterable[Note], signature: str):
    for note in notes:
        user = await User.objects.get(id=note.creator.id)
        await send_text_from_bot(
            user.tg_id,
            f"<b>{signature}</b>\n\n"
            f"<b>{note.name}</b>\n{hspoiler(note.content) if note.content else ''}",
            markup=remember_note_button
        )


async def change_notes_status_after_notification(more_19_minutes, more_1_hour, more_9_hours,
                                                 more_1_day, more_6_days, more_30_days, more_100_days):
    new_statuses = {
        "more_19_minutes": NoteReminderLevel.NINETEEN_MINUTES,
        "more_1_hour": NoteReminderLevel.ONE_HOUR,
        "more_9_hours": NoteReminderLevel.NINE_HOURS,
        "more_1_day": NoteReminderLevel.ONE_DAY,
        "more_6_days": NoteReminderLevel.SIX_DAYS,
        "more_30_days": NoteReminderLevel.THIRTY_DAYS,
        "more_100_days": NoteReminderLevel.ONE_HUNDRED_DAYS,
    }
    for k, v in new_statuses.items():
        if k in locals().keys():
            for note in locals().get(k):
                await note.update(reminder_level=v)
                if k == "more_100_days":
                    await note.update(is_completed=True)
