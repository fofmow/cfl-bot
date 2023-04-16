import logging

import sqlalchemy
from aiogram import executor

from config import DATABASE_URL
from handlers import dp
from storage.settings import metadata
from tools.middlewares import UserAddingMiddleware

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    
    logging.basicConfig(level=logging.INFO)
    
    dp.setup_middleware(UserAddingMiddleware())
    executor.start_polling(dp, skip_updates=True)
