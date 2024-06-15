"""
en: This file contains all the handlers for the bot.
ru: Этот файл содержит все обработчики для бота.
"""
import random
import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaAnimation, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from config import DB, ADMIN_ID, STATIC_PATH

from bot_messages import START_MESSAGE, HELP_MESSAGE, ADD_MESSAGE, VOICE_MESSAGE, CROWDED_MESSAGE, DELETE_MESSAGE
from bot_messages import START_MESSAGE_RU, HELP_MESSAGE_RU, CROWDED_MESSAGE_RU, REGISTRATION_MESSAGE_RU
from bot_messages import NOT_REGISTERED, REGISTRATION_MESSAGE

from utils import create_html_info

from keyboards import registration_keyboard, main_menu_keyboard
from keyboards import menu_button
from keyboards import switch_lang_register, switch_lang_register_ru, switch_lang_help, switch_lang_help_ru
from keyboards import registration_wrong, registration_wrong_ru
from keyboards import settings_menu_keyboard, time_menu_keyboard, words_menu_keyboard, check_menu_keyboard
from keyboards import settings_menu_keyboard_ru, time_menu_keyboard_ru, words_menu_keyboard_ru
from keyboards import main_menu_keyboard_ru, registration_keyboard_ru

router = Router()

db = DB


# en: States for the add content
# ru: Состояния для добавления контента
class AddContent(StatesGroup):
    check = State()
    en = State()
    ru = State()


# en: States for the delete content
# ru: Состояния для удаления контента
class DeleteContent(StatesGroup):
    check = State()


# en: States for the check content
# ru: Состояния для проверки контента
class CheckContent(StatesGroup):
    check = State()


# en: States for the time zone
# ru: Состояния для временной зоны
class TimeZone(StatesGroup):
    time_delta = State()


# en: States for the voice content
# ru: Состояния для голосового контента
class VoiceContent(StatesGroup):
    file_id = State()
    file_unique_id = State()


class VoiceCheck(StatesGroup):
    check = State()


def check_user(user_id: int) -> str:
    """
    en: Check if the user is in the database.
    ru: Проверка на наличие пользователя в базе данных.
    :param user_id: telegram user id
    :return: bool
    """
    users = [user['user_id'] for user in db.get_values('users')]
    if user_id not in users and user_id != ADMIN_ID:
        if len(users) > 100:
            return "CROWDED"
        return "NOT_REGISTERED"
    return "REGISTERED"


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    en: The command to start the bot.
    ru: Команда для запуска бота.
    """
    img_data = db.get_values('img_bot', 'name', 'header')
    if check_user(message.from_user.id) == "NOT_REGISTERED":
        if not img_data:
            await message.answer(
                START_MESSAGE,
                reply_markup=registration_keyboard(),
                parse_mode="HTML"
            )
        else:
            img_data = img_data[0]
            try:
                await message.answer_animation(
                    img_data["file_id"],
                    caption=START_MESSAGE,
                    reply_markup=registration_keyboard(),
                    parse_mode="HTML"
                )
            except Exception:
                file_path = os.path.join(STATIC_PATH, img_data["file_path"])
                file = FSInputFile(str(file_path))
                send_file = await message.answer_animation(
                    file,
                    caption=START_MESSAGE,
                    reply_markup=registration_keyboard(),
                    parse_mode="HTML"
                )
                db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'header')
    elif check_user(message.from_user.id) == "CROWDED":
        if not img_data:
            await message.answer(
                f"{CROWDED_MESSAGE}\n\n{CROWDED_MESSAGE_RU}",
                parse_mode="HTML"
            )
        else:
            img_data = img_data[0]
            try:
                await message.answer_animation(
                    img_data["file_id"],
                    caption=f"{CROWDED_MESSAGE}\n\n{CROWDED_MESSAGE_RU}",
                    parse_mode="HTML"
                )
            except Exception:
                file_path = os.path.join(STATIC_PATH, img_data["file_path"])
                file = FSInputFile(str(file_path))
                send_file = await message.answer_animation(
                    file,
                    caption=CROWDED_MESSAGE,
                    parse_mode="HTML"
                )
                db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'header')
    else:
        if not img_data:
            await message.answer(
                f"Welcome back, <b>{message.from_user.first_name}!</b>",
                reply_markup=menu_button.as_markup(),
                parse_mode="HTML"
            )
        else:
            img_data = img_data[0]
            try:
                await message.answer_animation(
                    img_data["file_id"],
                    caption=f"Welcome back, <b>{message.from_user.first_name}!</b>",
                    reply_markup=menu_button.as_markup(),
                    parse_mode="HTML"
                )
            except Exception:
                file_path = os.path.join(STATIC_PATH, img_data["file_path"])
                file = FSInputFile(str(file_path))
                send_file = await message.answer_animation(
                    file,
                    caption=f"Welcome back, <b>{message.from_user.first_name}!</b>",
                    reply_markup=menu_button.as_markup(),
                    parse_mode="HTML"
                )
                db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'header')


@router.callback_query(F.data == "register_ru")
async def register_ru(call: types.CallbackQuery):
    """
    en: The callback to switch the language to Russian.
    ru: Коллбэк для переключения языка на русский.
    """
    await call.message.edit_caption(
        caption=START_MESSAGE_RU,
        reply_markup=registration_keyboard_ru(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "register_en")
async def register_en(call: types.CallbackQuery):
    """
    en: The callback to switch the language to English.
    ru: Коллбэк для переключения языка на английский.
    """
    await call.message.edit_caption(
        caption=START_MESSAGE,
        reply_markup=registration_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "register")
async def register(call: types.CallbackQuery, state: FSMContext):
    """
    en: The callback to register the user.
    ru: Коллбэк для регистрации пользователя.
    """
    await state.set_state(TimeZone.time_delta)
    await state.update_data(time_delta=call.message.message_id)
    await call.message.edit_caption(
        caption=REGISTRATION_MESSAGE,
        reply_markup=switch_lang_register.as_markup(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "rules_timezone_ru")
async def rules_timezone_ru(call: types.CallbackQuery):
    """
    en: The callback to show the rules for the time zone.
    ru: Коллбэк для показа правил временной зоны.
    """
    await call.message.edit_caption(
        caption=REGISTRATION_MESSAGE_RU,
        reply_markup=switch_lang_register_ru.as_markup(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "rules_timezone_en")
async def rules_timezone_en(call: types.CallbackQuery):
    """
    en: The callback to show the rules for the time zone.
    ru: Коллбэк для показа правил временной зоны.
    """
    await call.message.edit_caption(
        caption=REGISTRATION_MESSAGE,
        reply_markup=switch_lang_register.as_markup(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "cancel_registration")
async def cancel_registration(call: types.CallbackQuery):
    """
    en: The callback to cancel the registration.
    ru: Коллбэк для отмены регистрации.
    """
    await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.message(TimeZone.time_delta)
async def time_zone(message: Message, state: FSMContext):
    """
    en: The message to set the time zone.
    ru: Сообщение для установки временной зоны.
    """
    # en: Check correct value
    # ru: Проверка корректного значения
    data = await state.get_data()
    message_id = data.get("time_delta")
    tz = message.text
    if not tz.isdigit():
        await message.delete()
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message_id,
            caption="You entered the wrong value. Value must be <b>integer</b>. Please, try again.\n\n",
            reply_markup=registration_wrong(),
            parse_mode="HTML"
        )
        await state.clear()
        return
    user_id = message.from_user.id
    db.add_value(
        'users',
        {
            "user_id": user_id,
            "full_name": message.from_user.full_name,
            "time_check": 0,
            "only_self": 1,
            "time_zone": tz
        }
    )
    await message.delete()
    await message.bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=message_id,
        caption="Registration was successful! Enjoy!",
        reply_markup=menu_button.as_markup(),
        parse_mode="HTML"
    )
    await state.clear()


@router.callback_query(F.data == "register_wrong_ru")
async def register_wrong_ru(call: types.CallbackQuery):
    """
    en: The callback to show the registration keyboard.
    ru: Коллбэк для показа клавиатуры регистрации.
    """
    await call.message.edit_caption(
        caption="Вы ввели неверное значение. Значение должно быть <b>целым числом</b>. "
                "Пожалуйста, попробуйте снова.",
        reply_markup=registration_wrong_ru(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data == "register_wrong_en")
async def register_wrong_en(call: types.CallbackQuery):
    """
    en: The callback to show the registration keyboard.
    ru: Коллбэк для показа клавиатуры регистрации.
    """
    await call.message.edit_caption(
        caption="You entered the wrong value. Value must be <b>integer</b>. Please, try again.",
        reply_markup=registration_wrong(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    en: The command to show the help message.
    ru: Команда для показа сообщения справки.
    """
    img_data = db.get_values('img_bot', 'name', 'help')
    if img_data:
        img_data = img_data[0]
        try:
            await message.answer_animation(
                img_data["file_id"],
                caption=HELP_MESSAGE,
                parse_mode="HTML",
                reply_markup=switch_lang_help.as_markup()
            )
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data["file_path"])
            file = FSInputFile(str(file_path))
            send_file = await message.answer_animation(
                file,
                caption=HELP_MESSAGE,
                parse_mode="HTML",
                reply_markup=switch_lang_help.as_markup()
            )
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'help')
    else:
        await message.answer(HELP_MESSAGE, parse_mode="HTML")


@router.callback_query(F.data == "help_ru")
async def help_ru(call: types.CallbackQuery):
    """
    en: The callback to show the help message.
    ru: Коллбэк для показа сообщения справки.
    """
    await call.message.edit_caption(
        caption=HELP_MESSAGE_RU,
        parse_mode="HTML",
        reply_markup=switch_lang_help_ru.as_markup()
    )
    await call.answer()


@router.callback_query(F.data == "help_en")
async def help_en(call: types.CallbackQuery):
    """
    en: The callback to show the help message.
    ru: Коллбэк для показа сообщения справки.
    """
    await call.message.edit_caption(
        caption=HELP_MESSAGE,
        parse_mode="HTML",
        reply_markup=switch_lang_help.as_markup()
    )
    await call.answer()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """
    en: The command to show the main menu.
    ru: Команда для показа главного меню.
    """
    if check_user(message.from_user.id) == "REGISTERED":
        img_data = db.get_values('img_bot', 'name', 'menu')
        if img_data:
            img_data = img_data[0]
            try:
                await message.answer_animation(
                    img_data["file_id"],
                    caption="Choose what you need:",
                    reply_markup=main_menu_keyboard()
                )
            except Exception:
                file_path = os.path.join(STATIC_PATH, img_data["file_path"])
                file = FSInputFile(str(file_path))
                send_file = await message.answer_animation(
                    file,
                    caption="Choose what you need:",
                    reply_markup=main_menu_keyboard()
                )
                db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'menu')
        else:
            await message.answer("Main menu. Choose what you need:", reply_markup=main_menu_keyboard())
    else:
        await message.answer(NOT_REGISTERED)
        await message.delete()


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """
    en: The command to show the settings menu.
    ru: Команда для показа меню настроек.
    """
    if check_user(message.from_user.id) == "REGISTERED":
        img_data = db.get_values('img_bot', 'name', 'settings')
        if img_data:
            img_data = img_data[0]
            try:
                await message.answer_animation(
                    img_data["file_id"],
                    caption="Choose what you need:",
                    reply_markup=settings_menu_keyboard()
                )
            except Exception:
                file_path = os.path.join(STATIC_PATH, img_data["file_path"])
                file = FSInputFile(str(file_path))
                send_file = await message.answer_animation(
                    file,
                    caption="Choose what you need:",
                    reply_markup=settings_menu_keyboard()
                )
                db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'settings')
        else:
            await message.answer("Settings. Choose what you need:", reply_markup=settings_menu_keyboard())
    else:
        await message.answer(NOT_REGISTERED)
        await message.delete()


@router.message(Command("add"))
async def add_content(message: Message, state: FSMContext):
    """
    en: The command to add the content.
    ru: Команда для добавления контента.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        await message.delete()
        return
    await state.set_state(AddContent.check)
    await message.answer(ADD_MESSAGE)


@router.message(AddContent.check)
async def add_content_check(message: Message, state: FSMContext):
    """
    en: The state to check the language of the phrase.
    ru: Состояние для проверки языка фразы.
    """
    await state.update_data(check=1)
    await message.reply(
        "You sent a phrase in <b>English</b>.\nWrite the translation into <b>Russian</b>.",
        parse_mode="HTML"
    )
    await state.update_data(en=message.text)
    await state.set_state(AddContent.ru)


@router.message(AddContent.ru)
async def add_content_ru(message: Message, state: FSMContext):
    """
    en: The command no add Russian phrase.
    ru: Команда для добавления русской фразы.
    """
    await state.update_data(ru=message.text)
    data = await state.get_data()
    en_phrase = data.get("en", 'No text')
    ru_phrase = data.get("ru", 'Текст отсутствует')
    await state.clear()
    tmp_dict = {
        "id": None,
        "user_id": message.from_user.id,
        "en": en_phrase,
        "ru": ru_phrase
    }
    db.add_value('content', tmp_dict)
    await message.answer(
        f"You've added the phrase:\n\n<b>en:</b> {en_phrase}\n\n<b>ru:</b> {ru_phrase}",
        parse_mode="HTML"
    )


@router.message(Command("delete"))
async def delete_content(message: Message, state: FSMContext):
    """
    en: The command to delete the content.
    ru: Команда для удаления контента.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        await message.delete()
        return
    if not db.get_values('content', 'user_id', message.from_user.id):
        await message.answer("You don't have any phrases.")
        return
    await state.set_state(DeleteContent.check)
    await message.answer(DELETE_MESSAGE)


@router.message(DeleteContent.check)
async def delete_content_check(message: Message, state: FSMContext):
    """
    en: The state to check the content for deletion.
    ru: Состояние для проверки контента на удаление.
    """
    content_en = db.get_values('content', 'en', message.text)
    content_ru = db.get_values('content', 'ru', message.text)
    content = content_en + content_ru
    if content:
        for phrase in content:
            db.delete_value('content', 'id', phrase['id'])
        await message.answer(f"The phrase <b>«{message.text}»</b> has been deleted.", parse_mode="HTML")
    else:
        await message.answer(f"The phrase <b>«{message.text}»</b> was not found.", parse_mode="HTML")
    await state.clear()


@router.message(Command("list"))
async def list_content(message: Message):
    """
    en: The command to show the list of the content.
    ru: Команда для показа списка контента.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        await message.delete()
        return
    content = db.get_values('content', 'user_id', message.from_user.id)
    get_phrases = create_html_info(message.from_user.full_name, content)
    if content:
        await message.reply_document(
            document=BufferedInputFile(
                file=get_phrases,
                filename=f"{message.from_user.full_name.replace(' ', '_')}.html"
            )
        )
    else:
        await message.answer("You don't have any phrases.")


# en: Block for handling the callback data
# ru: Блок обработки callback данных


@router.callback_query(F.data == "menu")
async def menu(call: types.CallbackQuery):
    """
    en: The callback to show the menu.
    ru: Коллбэк для показа меню.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'menu')
    if img_data:
        img_data = img_data[0]
        try:
            await call.message.answer_animation(
                img_data["file_id"],
                caption="Choose what you need:",
                reply_markup=main_menu_keyboard()
            )
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data["file_path"])
            file = FSInputFile(str(file_path))
            send_file = await call.message.answer_animation(
                file,
                caption="Choose what you need:",
                reply_markup=main_menu_keyboard()
            )
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'menu')
    else:
        await call.message.answer("Main menu", reply_markup=main_menu_keyboard())
    await call.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "menu_ru")
async def menu_ru(call: types.CallbackQuery):
    """
    en: The callback to show the menu.
    ru: Коллбэк для показа меню.
    """
    await call.message.edit_caption(caption="Выберите, что вам нужно:", reply_markup=main_menu_keyboard_ru())
    await call.answer()


@router.callback_query(F.data == "menu_en")
async def menu_en(call: types.CallbackQuery):
    """
    en: The callback to show the menu.
    ru: Коллбэк для показа меню.
    """
    await call.message.edit_caption(caption="Choose what you need:", reply_markup=main_menu_keyboard())
    await call.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu(call: types.CallbackQuery):
    """
    en: The callback to show the main menu.
    ru: Коллбэк для показа главного меню.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'menu')
    if img_data:
        img_data = img_data[0]
        try:
            new_animation = InputMediaAnimation(
                media=img_data["file_id"],
                caption="Choose what you need:"
            )
            await call.message.edit_media(new_animation, reply_markup=main_menu_keyboard())

        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data["file_path"])
            file = FSInputFile(str(file_path))
            new_animation = InputMediaAnimation(
                media=file,
                caption="Choose what you need:"
            )
            send_file = await call.message.edit_media(new_animation, reply_markup=main_menu_keyboard())
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'menu')
    else:
        await call.message.answer("Main menu", reply_markup=main_menu_keyboard())
        await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "add")
async def add(call: types.CallbackQuery, state: FSMContext):
    """
    en: The callback to add the content.
    ru: Коллбэк для добавления контента.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    await call.message.answer(ADD_MESSAGE)
    await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(AddContent.check)
    await call.answer()


@router.callback_query(F.data == "check")
async def check(call: types.CallbackQuery, state: FSMContext):
    """
    en: The callback to check the content.
    ru: Коллбэк для проверки контента.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'start')
    if img_data:
        img_data = img_data[0]
        try:
            new_animation = InputMediaAnimation(
                media=img_data["file_id"],
                caption="Let's check\n\nНачнем проверку"
            )
            await call.message.edit_media(new_animation)
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data["file_path"])
            file = FSInputFile(str(file_path))
            new_animation = InputMediaAnimation(
                media=file,
                caption="Let's check\n\nНачнем проверку"
            )
            send_file = await call.message.edit_media(new_animation)
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'start')
    else:
        await call.message.answer("Let's check\n\nНачнем проверку")
        await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    random_task = random.randint(1, 3)
    voice_data = db.get_values('voice', 'user_id', call.from_user.id)
    text_data = db.get_values('content', 'user_id', call.from_user.id)
    if db.get_values('users', 'user_id', call.from_user.id)[0]["only_self"]:
        text_data.extend(db.get_values('content', 'user_id', ADMIN_ID))
    if voice_data and text_data:
        if random_task % 2 == 0:
            random_voice = random.choice(voice_data)
            await call.message.answer_voice(
                random_voice["file_id"],
                caption=f"Translate this phrase",
                parse_mode="HTML"
            )
            await state.set_state(VoiceCheck.check)
            await state.update_data(check=random_voice["id"])
        else:
            random_phrase = random.choice(text_data)
            await call.message.answer(
                f"Translate phrase:\n\n<b>«{random_phrase['en']}»</b>\n",
                parse_mode="HTML"
            )
            await state.set_state(CheckContent.check)
            await state.update_data(check=random_phrase["id"])
    else:
        if text_data:
            random_phrase = random.choice(text_data)
            await call.message.answer(
                f"Translate phrase:\n\n<b>«{random_phrase['en']}»</b>\n",
                parse_mode="HTML"
            )
            await state.set_state(CheckContent.check)
            await state.update_data(check=random_phrase["id"])
        elif voice_data:
            random_voice = random.choice(voice_data)
            await call.message.answer_voice(
                random_voice["file_id"],
                caption="Translate this phrase",
                parse_mode="HTML"
            )
            await state.set_state(VoiceCheck.check)
            await state.update_data(check=random_voice["id"])
        else:
            await call.message.answer("You don't have any words. Please, add them.")
    await call.answer()


@router.callback_query(F.data == "continue")
async def continue_check(call: types.CallbackQuery, state: FSMContext):
    """
    en: The callback to continue the check.
    ru: Коллбэк для продолжения проверки.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    random_task = random.randint(1, 3)
    voice_data = db.get_values('voice', 'user_id', call.from_user.id)
    text_data = db.get_values('content', 'user_id', call.from_user.id)
    if db.get_values('users', 'user_id', call.from_user.id)[0]['only_self']:
        text_data.extend(db.get_values('content', 'user_id', ADMIN_ID))
    if voice_data and text_data:
        if random_task % 2 == 0:
            random_voice = random.choice(voice_data)
            await call.message.answer_voice(
                random_voice['file_id'],
                caption=f"Translate this phrase",
                parse_mode="HTML"
            )
            await state.set_state(VoiceCheck.check)
            await state.update_data(check=random_voice['id'])
        else:
            random_phrase = random.choice(text_data)
            await call.message.answer(
                f"Translate phrase:\n\n<b>«{random_phrase['en']}»</b>\n",
                parse_mode="HTML"
            )
            await state.set_state(CheckContent.check)
            await state.update_data(check=random_phrase['id'])
    else:
        if text_data:
            random_phrase = random.choice(text_data)
            await call.message.answer(
                f"Translate phrase:\n\n<b>«{random_phrase['en']}»</b>\n",
                parse_mode="HTML"
            )
            await state.set_state(CheckContent.check)
            await state.update_data(check=random_phrase['id'])
        elif voice_data:
            random_voice = random.choice(voice_data)
            await call.message.answer_voice(
                random_voice["file_id"],
                caption=f"Translate this phrase",
                parse_mode="HTML"
            )
            await state.set_state(VoiceCheck.check)
            await state.update_data(check=random_voice['id'])
        else:
            await call.message.answer("You don't have any words. Please, add them.")
    await call.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "cancel")
async def cancel_check(call: types.CallbackQuery):
    """
    en: The callback to cancel the check.
    ru: Коллбэк для отмены проверки.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    await call.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.message(VoiceCheck.check)
async def voice_check(message: Message, state: FSMContext):
    """
    en: The callback to check the voice message.
    ru: Коллбэк для проверки голосового сообщения.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        return
    data = await state.get_data()
    await state.clear()
    voice_id = data.get("check")
    translate = db.get_values('voice', 'id', voice_id)
    if translate:
        translate = translate[0]
        if message.text.lower() == translate["translate"].lower():
            await message.answer("Correct!", reply_markup=check_menu_keyboard())
        else:
            await message.answer(
                f"Incorrect! Correct answer:\n\n<b>«{translate['translate']}»</b>",
                reply_markup=check_menu_keyboard(),
                parse_mode="HTML"
            )


@router.message(CheckContent.check)
async def check_answer(message: Message, state: FSMContext):
    """
    en: The message to check the answer.
    ru: Сообщение для проверки контента.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        return
    data = await state.get_data()
    await state.clear()
    content_id = data.get("check")
    translate = db.get_values('content', 'id', content_id)
    if translate:
        translate = translate[0]
        if message.text.lower() == translate["ru"].lower():
            await message.reply("Correct!", reply_markup=check_menu_keyboard())
        else:
            await message.reply(
                f"Incorrect! Correct answer:\n\n<b>«{translate['ru']}»</b>",
                reply_markup=check_menu_keyboard(),
                parse_mode="HTML"
            )


@router.callback_query(F.data == "settings_menu")
async def settings(call: types.CallbackQuery):
    """
    en: The callback to show the settings menu.
    ru: Коллбэк для показа меню настроек.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'settings')
    if img_data:
        img_data = img_data[0]
        try:
            new_animation = InputMediaAnimation(
                media=img_data['file_id'],
                caption="Set time or set phrases to learn:"
            )
            await call.message.edit_media(new_animation, reply_markup=settings_menu_keyboard())
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data['file_path'])
            file = FSInputFile(str(file_path))
            new_animation = InputMediaAnimation(
                media=file,
                caption="Set time or set phrases to learn:"
            )
            send_file = await call.message.edit_media(new_animation, reply_markup=settings_menu_keyboard())
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'settings')
    else:
        await call.message.answer("Settings", reply_markup=settings_menu_keyboard())
        await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "settings_menu_ru")
async def settings_ru(call: types.CallbackQuery):
    """
    en: The callback to show the settings menu.
    ru: Коллбэк для показа меню настроек.
    """
    await call.message.edit_caption(
        caption="Установите время или настройте фразы для изучения:",
        reply_markup=settings_menu_keyboard_ru()
    )
    await call.answer()


@router.callback_query(F.data == "settings_menu_en")
async def settings_en(call: types.CallbackQuery):
    """
    en: The callback to show the settings menu.
    ru: Коллбэк для показа меню настроек.
    """
    await call.message.edit_caption(
        caption="Set time or set phrases to learn:",
        reply_markup=settings_menu_keyboard()
    )
    await call.answer()


@router.callback_query(F.data == "time_menu")
async def time_menu(call: types.CallbackQuery):
    """
    en: The callback to show the time menu.
    ru: Коллбэк для показа меню времени.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'time_setting')
    if img_data:
        img_data = img_data[0]
        try:
            new_animation = InputMediaAnimation(
                media=img_data["file_id"],
                caption="Set the time for regular checking:"
            )
            await call.message.edit_media(new_animation, reply_markup=time_menu_keyboard())
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data["file_path"])
            file = FSInputFile(str(file_path))
            new_animation = InputMediaAnimation(
                media=file,
                caption="Set the time for regular checking:"
            )
            send_file = await call.message.edit_media(new_animation, reply_markup=time_menu_keyboard())
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'time_setting')
    else:
        await call.message.answer("Time menu", reply_markup=time_menu_keyboard())
        await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "time_menu_ru")
async def time_menu_ru(call: types.CallbackQuery):
    """
    en: The callback to show the time menu.
    ru: Коллбэк для показа меню времени.
    """
    await call.message.edit_caption(
        caption="Установите время для регулярной проверки:",
        reply_markup=time_menu_keyboard_ru()
    )
    await call.answer()


@router.callback_query(F.data == "time_menu_en")
async def time_menu_en(call: types.CallbackQuery):
    """
    en: The callback to show the time menu.
    ru: Коллбэк для показа меню времени.
    """
    await call.message.edit_caption(
        caption="Set the time for regular checking:",
        reply_markup=time_menu_keyboard()
    )
    await call.answer()


@router.callback_query(F.data == "words_menu")
async def words_menu(call: types.CallbackQuery):
    """
    en: The callback to show the words menu.
    ru: Коллбэк для показа меню слов.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    img_data = db.get_values('img_bot', 'name', 'phrases_setting')
    if img_data:
        img_data = img_data[0]
        try:
            new_animation = InputMediaAnimation(
                media=img_data['file_id'],
                caption="Set the phrases to learn: only phrases added by you or all phrases stored in the bot."
            )
            await call.message.edit_media(new_animation, reply_markup=words_menu_keyboard())
        except Exception:
            file_path = os.path.join(STATIC_PATH, img_data['file_path'])
            file = FSInputFile(str(file_path))
            new_animation = InputMediaAnimation(
                media=file,
                caption="Set the phrases to learn: only phrases added by you or all phrases stored in the bot."
            )
            send_file = await call.message.edit_media(new_animation, reply_markup=words_menu_keyboard())
            db.update_value('img_bot', 'file_id', send_file.animation.file_id, 'name', 'phrases_setting')
    else:
        await call.message.answer("Words menu", reply_markup=words_menu_keyboard())
        await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data == "words_menu_ru")
async def words_menu_ru(call: types.CallbackQuery):
    """
    en: The callback to show the words menu.
    ru: Коллбэк для показа меню слов.
    """
    await call.message.edit_caption(
        caption="Установите фразы для изучения: только фразы добавленные вами или все фразы, хранящиеся в боте.",
        reply_markup=words_menu_keyboard_ru()
    )
    await call.answer()


@router.callback_query(F.data == "words_menu_en")
async def words_menu_en(call: types.CallbackQuery):
    """
    en: The callback to show the words menu.
    ru: Коллбэк для показа меню слов.
    """
    await call.message.edit_caption(
        caption="Set the phrases to learn: only phrases added by you or all phrases stored in the bot.",
        reply_markup=words_menu_keyboard()
    )
    await call.answer()


@router.callback_query(F.data.endswith("_time"))
async def time_menu(call: types.CallbackQuery):
    """
    en: The callback to set the for regular checking .
    ru: Коллбэк для установки времени для регулярной проверки.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    time_dict = {
        "morning_time": 0,
        "day_time": 1,
        "evening_time": 2
    }
    db.update_value(
        'users',
        'time_check',
        time_dict[call.data],
        'user_id',
        call.from_user.id
    )
    await call.message.answer(
        f"Time has been set: <b>{call.data.replace('_', ' ').capitalize()}</b>",
        parse_mode="HTML"
    )
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


@router.callback_query(F.data.endswith("_phrases"))
async def words_menu(call: types.CallbackQuery):
    """
    en: The callback to set the words to learn.
    ru: Коллбэк для установки слов для изучения.
    """
    if check_user(call.from_user.id) != "REGISTERED":
        await call.answer(NOT_REGISTERED)
        return
    words_dict = {
        "only_self_phrases": 0,
        "all_phrases": 1
    }
    db.update_value(
        'users',
        'only_self',
        words_dict[call.data],
        'user_id',
        call.from_user.id
    )
    await call.message.answer(
        f"Words to learn: <b>{call.data.replace('_', ' ').capitalize()}</b>",
        parse_mode="HTML")
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()


# en: Block for handling the voice messages
# ru: Блок обработки голосовых сообщений
@router.message(F.voice)
async def voice_handler(message: Message, state: FSMContext):
    """
    en: The message to add the voice message.
    ru: Сообщение для добавления голосового сообщения.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        await message.delete()
        return
    await state.update_data(file_id=message.voice.file_id)
    await state.update_data(file_unique_id=message.voice.file_unique_id)
    await state.set_state(VoiceContent.file_id)
    await message.answer(VOICE_MESSAGE)


@router.message(VoiceContent.file_id)
async def voice_translate(message: Message, state: FSMContext):
    """
    en: The message to add the translation to the voice message.
    ru: Сообщение для добавления перевода к голосовому сообщению.
    """
    data = await state.get_data()
    file_id = data.get("file_id")
    file_unique_id = data.get("file_unique_id")
    if not file_id or not file_unique_id:
        await message.answer("You haven't added a voice message.")
        await state.clear()
        return
    translate = message.text
    user_id = message.from_user.id
    db.add_value('voice', {
        "user_id": user_id,
        "file_id": file_id,
        "file_unique_id": file_unique_id,
        "translate": translate
    })
    await message.answer(
        f"Voice message has been added with translation:\n\n<b>«{translate}»</b>",
        parse_mode="HTML")
    await state.clear()


# en: Block for handling regular reply text messages
# ru: Блок обработки обычных текстовых сообщений
@router.message(F.text)
async def check_reply(message: Message):
    """
    en: The message to reply regular checking.
    ru: Сообщение для ответа на регулярную проверку.
    """
    if check_user(message.from_user.id) != "REGISTERED":
        await message.answer(NOT_REGISTERED)
        await message.delete()
        return
    if message.reply_to_message:
        if message.reply_to_message.voice:
            answer_phrase = message.text.lower()
            file_unique_id = message.reply_to_message.voice.file_unique_id
            data = db.get_values('voice', columns='file_unique_id', value=file_unique_id)
            if data:
                if answer_phrase == data[0]["translate"].lower():
                    await message.reply("Correct!")
                else:
                    await message.reply(
                        f"Incorrect! Correct answer:\n\n<b>«{data[0]['translate']}»</b>",
                        parse_mode="HTML"
                    )
            else:
                await message.reply("I can't find the voice message in the database.")
        else:
            phrase = message.reply_to_message.text.split(":\n\n«")[-1][:-1]
            data = db.get_values('content', 'en', phrase)
            if data:
                if message.text.lower() == data[0]["ru"].lower():
                    await message.reply("Correct!")
                else:
                    await message.reply(
                        f"Incorrect! Correct answer:\n\n<b>«{data[0]['ru']}»</b>",
                        parse_mode="HTML"
                    )
            else:
                await message.reply(
                    f"I can't find the phrase <b>«{phrase}»</b> in the database.",
                    parse_mode="HTML")
    else:
        await message.bot.delete_message(message.chat.id, message.message_id)
