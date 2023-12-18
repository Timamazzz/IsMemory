import requests
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = '6845960244:AAEqZSwtsNb3zaj2uDtZ6HplPPzYPaFB28U'
API_URL = "https://belmemorial.ru/api"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text="Заказы"),
            )
            await message.answer(
                "Выберите действие:",
                reply_markup=builder.as_markup(resize_keyboard=True),
            )
        elif response.status_code == 404:
            await message.answer("Исполнителя с таким номером телефона нет в системе")
        else:
            await message.answer("Произошла ошибка при отправке данных. Попробуйте позже.")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже.")
        logging.error(f"Error: {str(e)}")


async def get_user_orders(chat_id):
    orders = requests.get(f'{API_URL}/orders/get_orders_by_chat_id/', params={'chat_id': chat_id})
    return orders if orders else None


@dp.message(lambda message: message.text == "Заказы")
async def view_all_orders(message: types.Message):
    chat_id = message.chat.id
    orders = await get_user_orders(chat_id)
    if orders:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for order in orders:
            keyboard.add(KeyboardButton(text=f"заказ № {order['id']} {order['date'].strftime('%d.%m.%Y')}\n {order['service_name']}"))
        await message.answer("Выберите заказ:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет активных заказов.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
