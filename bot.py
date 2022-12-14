"""_summary_
    username @wuzoRepotuBot 
    name tgWeatherReport
    t.me/wuzoRepotuBot
"""

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_settings import bot_config
import handlers
import machines

bot: Bot = Bot(token=bot_config.botapi_token)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, storage=storage)


if __name__ == '__main__':

    menu_commands = {
        '/start': 'Начать работу',
        '/help': 'Поддержка'
    }

    handlers_dict = {
        '/start': handlers.start_message,
        '/help': handlers.help_message,
        'Погода в другом месте': handlers.city_start,
        'Установить свой город': handlers.user_city,
        'other city chose': handlers.city_chosen,
        'user city chose': handlers.city_user_chosen,
        'Меню': handlers.start_message,
        'sticker': handlers.sticker_echo
    }
    dp.register_message_handler(handlers_dict['other city chose'], state=machines.ChoiceCityWeather.waiting_city)
    dp.register_message_handler(handlers_dict['user city chose'], state=machines.ChoiceUserCity.waiting_city)
    dp.register_message_handler(handlers_dict['sticker'], content_types='sticker')
    bot_config.register_handlers(dp, handlers_dict)

    executor.start_polling(dp, skip_updates=True, on_startup=bot_config.set_main_menu(menu_commands))
    
