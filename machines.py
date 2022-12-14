from aiogram.dispatcher.filters.state import State, StatesGroup

class ChoiceCityWeather(StatesGroup):
    waiting_city = State()
    
class ChoiceUserCity(StatesGroup):
    waiting_city = State()