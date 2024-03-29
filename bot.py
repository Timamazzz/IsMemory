import os
from datetime import datetime

import requests
import asyncio
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from orders_app.enums import OrderStatusEnum

#BOT_TOKEN = '6845960244:AAEqZSwtsNb3zaj2uDtZ6HplPPzYPaFB28U'
BOT_TOKEN = '7115409811:AAEGwdzxIiXhXuKJDefBgm8vzeB7qR-oOp8'
API_URL = "https://belmemorial.ru/api"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

# API_URL = 'http://51.250.126.124:3031/api'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Заказы"),
    )
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Поделиться номером телефона", request_contact=True),
    )
    await message.answer(
        "Поделиться",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.contact)
async def shared_contact(message: types.Message):
    try:
        phone_number = message.contact.phone_number
        chat_id = message.chat.id

        api_url = f'{API_URL}/orders/executors/set_data/'
        data = {'phone_number': phone_number, 'chat_id': chat_id}

        response = requests.put(api_url, json=data, headers=HEADERS)

        if response.status_code == 200:
            main_keyboard = get_main_keyboard()
            await message.answer(
                "Выберите действие:",
                reply_markup=main_keyboard,
            )
        elif response.status_code == 404:
            await message.answer("Исполнителя с таким номером телефона нет в системе")
        else:
            await message.answer("Произошла ошибка при отправке данных. Попробуйте позже.")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже.")


async def get_user_orders(chat_id):
    response = requests.get(f'{API_URL}/orders/get_orders_by_chat_id/', params={'chat_id': chat_id}, headers=HEADERS)
    orders = response.json() if response.status_code == 200 else None
    return orders


@dp.message(lambda message: message.text == "Заказы")
async def view_all_orders(message: types.Message):
    chat_id = message.chat.id
    orders = await get_user_orders(chat_id)
    if orders:
        keyboard = ReplyKeyboardBuilder()
        for order in orders:
            order_date = datetime.strptime(order['date'], '%Y-%m-%d')
            formatted_date = order_date.strftime('%d.%m.%Y')
            keyboard.add(KeyboardButton(text=f"заказ № {order['id']} {formatted_date}\n {order['service_name']}"))
        keyboard.adjust(2)

        keyboard.row(
            KeyboardButton(text="Вернуться в главное меню")
        )
        await message.answer("Выберите заказ:", reply_markup=keyboard.as_markup(resize_keyboard=True))
    else:
        await message.answer("У вас нет активных заказов.")


@dp.message(lambda message: message.text.startswith("заказ №") if message.text else None)
async def order_actions(message: types.Message):
    order_id = message.text.split()[2]
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=f"Информация по заказу № {order_id}"),
        types.KeyboardButton(text=f"Завершить заказ № {order_id}"),
    )
    builder.row(
        KeyboardButton(text="Заказы"),
        KeyboardButton(text="Вернуться в главное меню"),
    )
    await message.answer(f"#{order_id}", reply_markup=builder.as_markup(resize_keyboard=True))


async def get_order_details(order_id):
    response = requests.get(f'{API_URL}/orders/{order_id}', headers=HEADERS)
    order_details = response.json() if response.status_code == 200 else None
    return order_details


@dp.message(lambda message: message.text.startswith("Информация по заказу №") if message.text else None)
async def view_order_details(message: types.Message):
    order_id = message.text.split()[4]
    order_details = await get_order_details(order_id)

    if order_details:
        details_text = f"Детали заказа № {order_id}:\n"
        details_text += f"Название услуги: {order_details['service_name']}\n"

        order_date = datetime.strptime(order_details['date'], '%Y-%m-%d')
        formatted_date = order_date.strftime('%d.%m.%Y')
        details_text += f"Дата: {formatted_date}\n"

        deceased_info = order_details.get('deceased', {})
        details_text += (f"Усопший:  {deceased_info.get('first_name', '')} "
                         f"{deceased_info.get('last_name', '')} "
                         f"{deceased_info.get('patronymic', '')} \n")

        details_text += f"Кладбище: {deceased_info.get('cemetery_name', '')}, {deceased_info.get('cemetery_municipality_name', '')}\n"

        coordinates = order_details.get('coordinates')
        if coordinates:
            details_text += f"Координаты участка: {coordinates[0][0]}\n"
        else:
            details_text += "Координаты участка отсутствуют.\n"

        await message.answer(details_text)
    else:
        await message.answer("Не удалось получить информацию о заказе. Попробуйте позже.")


@dp.message(lambda message: message.text.startswith("Завершить заказ №") if message.text else None)
async def finish_order(message: types.Message, state: FSMContext):
    order_id = message.text.split()[3]
    await state.update_data(order_id=order_id)
    await state.update_data(images=[])
    finish_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Завершить")],
            [KeyboardButton(text="Заказы")],
        ],
        resize_keyboard=True,
    )
    order_data = await state.get_data()
    await message.answer(
        "Для завершения заказа, прикрепите изображение(я) с выполненной работой.",
        reply_markup=finish_keyboard,
    )


@dp.message(lambda message: message.text == "Завершить")
async def process_finish_order(message: types.Message, state: FSMContext):
    order_data = await state.get_data()
    order_id = order_data.get('order_id')
    images = order_data.get('images', [])

    if images:
        response = requests.put(f'{API_URL}/orders/{order_id}/',
                                json={'images': images,
                                      'status': OrderStatusEnum.COMPLETED.name},
                                headers=HEADERS)
        print('response', response.json())
        if response.status_code == 200:
            await message.answer("Спасибо за предоставленные изображения. Ваш заказ завершен!")
            main_keyboard = get_main_keyboard()
            await message.answer(
                "Выберите действие:",
                reply_markup=main_keyboard,
            )
            await state.clear()
        else:
            await message.answer("Произошла ошибка при завершении заказа. Попробуйте позже.")
    else:
        await message.answer("Пожалуйста, прикрепите фотографии перед завершением заказа.")


@dp.message(F.photo)
async def handle_completed_order(message: types.Message, state: FSMContext):
    order_data = await state.get_data()
    order_id = order_data.get('order_id')
    if order_id:
        images = order_data.get('images', [])

        file_info = await bot.get_file(message.photo[-1].file_id)
        file_path = file_info.file_path

        file_extension = os.path.splitext(file_path)[1]

        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        response = requests.get(file_url, headers=HEADERS)
        file_name = f"{message.photo[0].file_id}{file_extension}"

        if response.status_code == 200:
            with open(os.path.join('media', file_name), 'wb') as file:
                file.write(response.content)
            images.append({"file": file_name, "original_name": file_path})
            await state.update_data(images=images)
        else:
            await message.answer("Ошибка отправки фото")
    else:
        await message.answer("Выберите заказ для завершения")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
