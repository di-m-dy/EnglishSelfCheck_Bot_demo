"""
en: This module contains the keyboards for the bot.
ru: Этот модуль содержит клавиатуры для бота.
"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def registration_keyboard():
    """
    en: The registration keyboard.
    ru: Клавиатура регистрации.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="register_ru")],
        [InlineKeyboardButton(text="[ SignUp ]", callback_data="register")],
        [InlineKeyboardButton(text="[ Cancel ]", callback_data="cancel_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def registration_keyboard_ru():
    """
    en: The registration keyboard.
    ru: Клавиатура регистрации.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="register_en")],
        [InlineKeyboardButton(text="[ Регистрация ]", callback_data="register")],
        [InlineKeyboardButton(text="[ Отмена ]", callback_data="cancel_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def registration_wrong():
    """
    en: The registration keyboard.
    ru: Клавиатура регистрации.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="register_wrong_ru")],
        [InlineKeyboardButton(text="[ SignUp ]", callback_data="register")],
        [InlineKeyboardButton(text="[ Cancel ]", callback_data="cancel_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def registration_wrong_ru():
    """
    en: The registration keyboard.
    ru: Клавиатура регистрации.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="register_wrong_en")],
        [InlineKeyboardButton(text="[ Регистрация ]", callback_data="register")],
        [InlineKeyboardButton(text="[ Отмена ]", callback_data="cancel_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def main_menu_keyboard():
    """
    en: The keyboard of menu buttons.
    ru: Клавиатура главного меню.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="menu_ru")],
        [InlineKeyboardButton(text="[ Let's check ]", callback_data="check")],
        [InlineKeyboardButton(text="[ Add ]", callback_data="add")],
        [InlineKeyboardButton(text="[ Settings ]", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def main_menu_keyboard_ru():
    """
    en: The keyboard of menu buttons.
    ru: Клавиатура главного меню.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="menu_en")],
        [InlineKeyboardButton(text="[ Начнем проверку ]", callback_data="check")],
        [InlineKeyboardButton(text="[ Добавить ]", callback_data="add")],
        [InlineKeyboardButton(text="[ Настройки ]", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def settings_menu_keyboard():
    """
    en: The settings menu keyboard.
    ru: Клавиатура меню настроек.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="settings_menu_ru")],
        [InlineKeyboardButton(text="[ Set time for check ]", callback_data="time_menu")],
        [InlineKeyboardButton(text="[ Whose words to learn? ]", callback_data="words_menu")],
        [InlineKeyboardButton(text="<< return", callback_data="main_menu")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def settings_menu_keyboard_ru():
    """
    en: The settings menu keyboard.
    ru: Клавиатура меню настроек.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="settings_menu_en")],
        [InlineKeyboardButton(text="[ Настроить время ]", callback_data="time_menu")],
        [InlineKeyboardButton(text="[ Чьи слова учить? ]", callback_data="words_menu")],
        [InlineKeyboardButton(text="<< назад", callback_data="main_menu")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def time_menu_keyboard():
    """
    en: The time menu keyboard.
    ru: Клавиатура меню времени.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="time_menu_ru")],
        [InlineKeyboardButton(text="morning [8.00-13.00]", callback_data="morning_time")],
        [InlineKeyboardButton(text="afternoon [13.00-18.00]", callback_data="day_time")],
        [InlineKeyboardButton(text="evening [18.00-23.00]", callback_data="evening_time")],
        [InlineKeyboardButton(text="<< return", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def time_menu_keyboard_ru():
    """
    en: The time menu keyboard.
    ru: Клавиатура меню времени.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="time_menu_en")],
        [InlineKeyboardButton(text="утро [8.00-13.00]", callback_data="morning_time")],
        [InlineKeyboardButton(text="день [13.00-18.00]", callback_data="day_time")],
        [InlineKeyboardButton(text="вечер [18.00-23.00]", callback_data="evening_time")],
        [InlineKeyboardButton(text="<< назад", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def words_menu_keyboard():
    """
    en: The words menu keyboard.
    ru: Клавиатура меню слов.
    """
    buttons = [
        [InlineKeyboardButton(text=">> switch language >>", callback_data="words_menu_ru")],
        [InlineKeyboardButton(text="[ Only my words ]", callback_data="only_self_phrases")],
        [InlineKeyboardButton(text="[ All words ]", callback_data="all_phrases")],
        [InlineKeyboardButton(text="<< return", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def words_menu_keyboard_ru():
    """
    en: The words menu keyboard.
    ru: Клавиатура меню слов.
    """
    buttons = [
        [InlineKeyboardButton(text="<< переключить язык <<", callback_data="words_menu_en")],
        [InlineKeyboardButton(text="[ Только мои слова ]", callback_data="only_self_phrases")],
        [InlineKeyboardButton(text="[ Все слова ]", callback_data="all_phrases")],
        [InlineKeyboardButton(text="<< назад", callback_data="settings_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def check_menu_keyboard():
    """
    en: The check menu keyboard.
    ru: Клавиатура меню проверки.
    """
    buttons = [
        [InlineKeyboardButton(text="continue", callback_data="continue")],
        [InlineKeyboardButton(text="cancel", callback_data="cancel")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


# en: The keyboard for the main menu.
# ru: Клавиатура для главного меню.
menu_button = InlineKeyboardBuilder()
menu_button.add(InlineKeyboardButton(text="[ MENU | МЕНЮ ]", callback_data="menu"))


# en: The keyboard for switching the language at the registration stage.
# ru: Клавиатура для переключения языка на этапе регистрации.
switch_lang_register = InlineKeyboardBuilder()
switch_lang_register.add(InlineKeyboardButton(text=">> switch language >>", callback_data="rules_timezone_ru"))

switch_lang_register_ru = InlineKeyboardBuilder()
switch_lang_register_ru.add(InlineKeyboardButton(text="<< переключить язык <<", callback_data="rules_timezone_en"))


# en: The keyboard for switching the language at the help stage.
# ru: Клавиатура для переключения языка на этапе инструкций.
switch_lang_help = InlineKeyboardBuilder()
switch_lang_help.add(InlineKeyboardButton(text=">> switch language >>", callback_data="help_ru"))

switch_lang_help_ru = InlineKeyboardBuilder()
switch_lang_help_ru.add(InlineKeyboardButton(text="<< переключить язык <<", callback_data="help_en"))
