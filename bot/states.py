from aiogram.dispatcher.filters.state import StatesGroup, State


class CategoryOperation(StatesGroup):
    input_name = State()
    
    choosing_for_removing = State()


class NoteOperation(StatesGroup):
    input_name = State()
    input_content = State()
    input_category = State()


class CardPractice(StatesGroup):
    input_category = State()
    viewing = State()


class Donate(StatesGroup):
    input_amount = State()
