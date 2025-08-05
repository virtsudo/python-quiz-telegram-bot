from aiogram.fsm.state import StatesGroup, State


class Status(StatesGroup):
    set_number_of_quiz = State()
    game_state = State()
