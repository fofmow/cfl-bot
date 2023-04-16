from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from tools.reminders import remind_users_about_notes


async def set_start_commands(_):
    await bot.set_my_commands([
        BotCommand("/home", "Главное Меню  🏠"),
    ])


async def on_startup(_):
    scheduler = AsyncIOScheduler()
    five_minutes_trigger = IntervalTrigger(minutes=5)
    scheduler.add_job(remind_users_about_notes, trigger=five_minutes_trigger)
    scheduler.start()
    
    await set_start_commands(_)
    await remind_users_about_notes()
