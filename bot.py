from datetime import datetime

import requests
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from orders_app.enums import OrderStatusEnum

BOT_TOKEN = '6845960244:AAEqZSwtsNb3zaj2uDtZ6HplPPzYPaFB28U'
#API_URL = "https://belmemorial.ru/api"
API_URL = "http://250.51.126.124:8960/api"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Заказы"),
    )
    return builder.as_markup(resize_keyboard=True)


@dp.message(lambda message: message.text == "Вернуться в главное меню")
async def back_to_main_menu(message: types.Message):
    print('hello')
    main_keyboard = get_main_keyboard()
    await message.answer(
        "Выберите действие:",
        reply_markup=main_keyboard,
    )


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
        response = requests.put(api_url, json=data)
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
        logging.error(f"Error: {str(e)}")


async def get_user_orders(chat_id):
    response = requests.get(f'{API_URL}/orders/get_orders_by_chat_id/', params={'chat_id': chat_id})
    orders = response.json() if response.status_code == 200 else None
    return orders


class OrderFinishStates(StatesGroup):
    WAITING_FOR_PHOTO = State()


@dp.message(F.photo)
async def handle_completed_order(message: types.Message, state: FSMContext):
    order_data = await state.get_data()
    order_id = order_data.get('order_id')
    print(order_id)
    await message.answer("Спасибо за предоставленные изображения. Ваш заказ завершен!")
    # response = requests.patch(f'{API_URL}/orders/{order_id}/',
    #                           params={'images': message.photo, 'status': OrderStatusEnum.COMPLETED.name})
    print(f'{API_URL}/orders/{order_id}/')
    response = requests.patch(f'{API_URL}/orders/{order_id}/', params={'status': OrderStatusEnum.COMPLETED.name})
    print(response)
    if response.status_code == 200:
        await message.answer("Заказ успешно завершен!")
    else:
        await message.answer("Произошла ошибка при завершении заказа. Попробуйте позже.")


@dp.message(lambda message: message.text.startswith("Завершить заказ №"))
async def finish_order(message: types.Message, state: FSMContext):
    order_id = message.text.split()[3]
    await state.update_data(order_id=order_id)
    await message.answer("Для завершения заказа, прикрепите изображение(я) с выполненной работой.")


@dp.message(Command("reset_state"))
async def reset_state(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Состояние сброшено.")


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

        keyboard.row(
            KeyboardButton(text="Вернуться в главное меню")
        )
        await message.answer("Выберите заказ:", reply_markup=keyboard.as_markup(resize_keyboard=True))
    else:
        await message.answer("У вас нет активных заказов.")


@dp.message(lambda message: message.text.startswith("заказ №"))
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
    response = requests.get(f'{API_URL}/orders/{order_id}')
    order_details = response.json() if response.status_code == 200 else None
    return order_details


@dp.message(lambda message: message.text.startswith("Информация по заказу №"))
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
                         f"{deceased_info.get('patronymic', '')}\n")

        details_text += f"Кладбище: {deceased_info.get('cemetery_name', '')}, {deceased_info.get('cemetery_municipality_name', '')}\n"
        await message.answer(details_text)
    else:
        await message.answer("Не удалось получить информацию о заказе. Попробуйте позже.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
