from aiogram.fsm.state import StatesGroup, State

class RegistrationState(StatesGroup):
    full_name = State()
    phone = State()
