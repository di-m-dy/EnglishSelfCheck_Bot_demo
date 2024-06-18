"""
en: The main file of the bot.
ru: Основной файл бота.
"""
import asyncio
import random
import logging
from aiogram import Bot, Dispatcher


from handlers import router
from config import BOT_TOKEN, ADMIN_ID, TIME_CHECK, DB
from utils import detect_time


# en: Enable logging
# ru: Включаем логирование
logging.basicConfig(level=logging.INFO)

db = DB

# en: Bot object
# ru: Объект бота
bot = Bot(token=BOT_TOKEN)
# en: Dispatcher
# ru: Диспетчер
dp = Dispatcher()
dp.include_router(router)


async def send_message():
    users = db.get_values('users')
    for user in users:
        user_id = user.get('user_id')
        time_zone = user.get('time_zone')
        time_check = user.get('time_check')
        only_self = user.get('only_self')
        user_time = detect_time(time_zone).hour
        if TIME_CHECK[time_check](user_time):
            random_task = random.randint(1, 3)
            voice_content = db.get_values('voice', 'user_id', user_id)
            content = db.get_values('content', 'user_id', user_id)
            if only_self:
                content.extend(db.get_values('content', 'user_id', ADMIN_ID))
            if content and voice_content:
                if random_task % 3 == 0:
                    random_data = random.choice(voice_content)
                    file_id = random_data.get('file_id')
                    try:
                        await bot.send_voice(
                            user_id,
                            file_id,
                            caption="Listen to the voice message and <b>reply</b> with the translated text.",
                            parse_mode='HTML'
                        )
                    except Exception as e:
                        await bot.send_message(ADMIN_ID, f"Try send voice to {user_id} Error: {e}")
                else:
                    random_data = random.choice(content)
                    en = random_data.get('en', 'No words')
                    try:
                        await bot.send_message(
                            user_id,
                            f"<b>Reply to this message</b> with the translation into Russian:\n\n<b>«{en}»</b>",
                            parse_mode='HTML')
                    except Exception as e:
                        await bot.send_message(ADMIN_ID, f"Try send message to {user_id} Error: {e}")
            elif content:
                random_data = random.choice(content)
                en = random_data.get('en', 'No words')
                try:
                    await bot.send_message(
                        user_id,
                        f"<b>Reply to this message</b> with the translation into Russian:\n\n<b>«{en}»</b>",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    await bot.send_message(ADMIN_ID, f"Try send message to {user_id} Error: {e}")
            elif voice_content:
                random_data = random.choice(voice_content)
                file_id = random_data.get('file_id')
                try:
                    await bot.send_voice(
                        user_id,
                        file_id,
                        caption="Listen to the voice message and <b>reply</b> with the translated text.",
                        parse_mode='HTML'
                    )
                except Exception as e:
                    await bot.send_message(ADMIN_ID, f"Try send voice to {user_id} Error: {e}")
            else:
                try:
                    await bot.send_message(user_id, "You don't have any words. Please, add them.")
                except Exception as e:
                    await bot.send_message(ADMIN_ID, f"Try send default message to {user_id} Error: {e}")
            if len(users) > 100:
                await asyncio.sleep(0.2)


async def scheduler():
    while True:
        await send_message()
        await asyncio.sleep(1200)


async def on_startup():
    asyncio.create_task(scheduler())


async def main():
    """
    en: Start the bot
    ru: Запускаем бота
    """
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
