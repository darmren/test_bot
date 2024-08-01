from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class TestSG(StatesGroup):
    start = State()
    test = State()
    result = State()
