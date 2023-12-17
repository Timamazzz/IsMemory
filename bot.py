import logging
from aiogram import Bot, Dispatcher, types
import requests
from aiogram.enums import ParseMode

BOT_TOKEN = '6845960244:AAEqZSwtsNb3zaj2uDtZ6HplPPzYPaFB28U'
API_URL = "https://belmemorial/api"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['get_orders'])
async def get_orders(message: types.Message):
    try:
        telegram_phone = message.contact.phone_number

        response = requests.get(f'{API_URL}/orders/get_orders_by_phone', params={'phone_number': telegram_phone})
        orders = response.json()

        if response.status_code == 200:
            orders_text = '\n'.join([f"{order['id']}. {order['name']}" for order in orders])
            await message.answer(f"Список заказов:\n{orders_text}", parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("Не удалось получить список заказов. Попробуйте позже.")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже.")
        logging.error(f"Error: {str(e)}")
