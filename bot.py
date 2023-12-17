from datetime import datetime

import requests
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from orders_app.enums import OrderStatusEnum

BOT_TOKEN = '6845960244:AAEqZSwtsNb3zaj2uDtZ6HplPPzYPaFB28U'
API_URL = "https://belmemorial.ru/api"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Список заказов",  request_contact=True),
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.contact)
async def handle_orders_button(message: types.Message):
    try:
        telegram_phone = message.contact.phone_number
        telegram_phone = telegram_phone.lstrip('+7')

        response = requests.get(f'{API_URL}/orders/get_orders_by_phone/', params={'phone_number': telegram_phone})
        orders = response.json()
        if response.status_code == 200:
            orders_text = '\n'.join([f"Заказ №{order['id']} "
                                     f"{datetime.strptime(order['date'], '%Y-%m-%d').strftime('%d.%m.%Y')} "
                                     f"{order['service_name']}"
                                     for order in orders])

            await message.answer(f"Список заказов:\n{orders_text}", parse_mode="Markdown")
        elif response.status_code == 404:
            await message.answer("Нет активных заказов")
        else:
            await message.answer("Не удалось получить список заказов. Попробуйте позже.")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже.")
        logging.error(f"Error: {str(e)}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
