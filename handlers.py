from aiogram import types
from aiogram.dispatcher import FSMContext
# import asyncio
# import aioschedule

import machines
from database import orm
from api_requests import api_request

async def start_message(message: types.Message):
    
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = (
        types.KeyboardButton('Погода в моём городе'),
        types.KeyboardButton('Погода в другом месте'),
        types.KeyboardButton('История'),
        types.KeyboardButton('Установить свой город')
    )
    markup.add(*btns)
    
    text = f'Привет {message.from_user.first_name}, я бот, который расскажет тебе о погоде на сегодня'    
    await message.answer(text, reply_markup=markup)
    
async def help_message(message: types.Message):
    pass

async def user_city(message: types.Message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Введите название города'
    await message.answer(text, reply_markup=markup)
    await machines.ChoiceUserCity.waiting_city.set()
    
    
async def city_user_chosen(message: types.Message, state: FSMContext):
    await state.update_data(waiting_city=message.text.title())
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = (
        types.KeyboardButton('Погода в моём городе'),
        types.KeyboardButton('Погода в другом месте'),
        types.KeyboardButton('История'),
        types.KeyboardButton('Установить свой город')
    )
    markup.add(*btns)
    city = await state.get_data()
    text = "Идём в меню"
    if city.get('waiting_city') != 'Меню':
        text = 'Ваш город выбран: {}'.format(city.get('waiting_city'))        
        # здесь запись в БД
    await message.answer(text, reply_markup=markup)
    await state.finish()

    
async def city_start(message: types.Message):
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Введите название города'
    await message.answer(text, reply_markup=markup)
    await machines.ChoiceCityWeather.waiting_city.set()

async def city_chosen(message: types.Message, state: FSMContext):
    await state.update_data(waiting_city=message.text.title())
    markup = types.reply_keyboard.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = (
        types.KeyboardButton('Погода в моём городе'),
        types.KeyboardButton('Погода в другом месте'),
        types.KeyboardButton('История'),
        types.KeyboardButton('Установить свой город')
    )
    markup.add(*btns)
    city = await state.get_data()
    if city.get('waiting_city') != 'Меню':
        data = api_request.get_weather(city.get('waiting_city'))['fact']
        text = '\n'.join((f'Погода в городе: {city.get("waiting_city")}',
        f'Температура: {data["temp"]} C',
        f'Ощущается как: {data["feels_like"]} C',
        f'Скорость ветра: {data["wind_speed"]}м/с',
        f'Давление: {data["pressure_mm"]}мм'))
        await message.answer(text, reply_markup=markup)
    else:
        await message.answer(city.get('waiting_city'), reply_markup=markup)
    await state.finish()
    

# async def reminder():
#     await print('Hello')

# async def scheduler():
#     aioschedule.every().day.at('8:00').do(reminder)
#     aioschedule.every().day.at('15:00').do(reminder)
#     aioschedule.every().day.at('20:00').do(reminder)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)

