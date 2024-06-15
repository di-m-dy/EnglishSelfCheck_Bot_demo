"""
en: Messages for the application
ru: Сообщения для приложения
"""
START_MESSAGE = ("Hi! I am a bot for <b>self-checking</b> your English knowledge.\n"
                 "Add words or phrases to test yourself later. Learn with pleasure – you can do it!")

START_MESSAGE_RU = ("Привет! Я бот для <b>самопроверки</b> знаний английского языка.\n"
                    "Добавь слова или фразы, чтобы проверить себя позже. Учись с удовольствием – ты сможешь!")

CROWDED_MESSAGE = "The bot is crowded. Please, try again later."

CROWDED_MESSAGE_RU = "Бот перегружен. Пожалуйста, попробуйте позже."

HELP_MESSAGE = ("The rules are simple!\n\n"
                "There are two types of checks - regular and spontaneous.\n\n"
                "For <b>regular checks</b>, "
                "specify a convenient time interval in the settings to receive phrases for testing.\n\n"
                "Make sure to <b>reply to the message</b> with your answer.\n\n"
                "For a spontaneous test, press the <b>«let's check»</b> button.\n\n"
                "You can also add a phrase via a <b>voice message</b>, just <b>send</b> it to me.\n\n"
                "/add - command to add the text with phrase you need or press the <b>«add»</b> button in the menu\n\n"
                "/list - show all your phrases.\n\n"
                "/settings - change the settings.\n\n"
                "/delete - delete a phrase.\n")

HELP_MESSAGE_RU = ("Правила просты!\n\n"
                   "Есть два вида проверок - регулярные и спонтанные.\n\n"
                   "Для <b>регулярных проверок</b> "
                   "укажите удобный временной интервал в настройках для получения фраз для тестирования.\n\n"
                   "Обязательно именно <b>ответьте на сообщение</b> своим переводом.\n\n"
                   "Для спонтанного теста нажмите кнопку <b>«начнем проверку»</b>.\n\n"
                   "Также можно добавить фразу <b>голосовым сообщением</b>, просто <b>отправьте</b> его мнею\n\n"
                   "/add - команда для добавления фразы для запоминания или жми кнопку <b>«add»</b> в меню\n\n"
                   "/list - показать все ваши фразы.\n\n"
                   "/settings - изменить настройки.\n\n"
                   "/delete - удалить фразу.\n")

ADD_MESSAGE = "Write the English phrase you want to add."

DELETE_MESSAGE = "Write the English phrase you want to delete."

VOICE_MESSAGE = "Write the translation of the voice phrase."

REGISTRATION_MESSAGE = ("First, let's synchronize our watches.\n\n"
                        "Send the number that represents the time difference from Greenwich Mean Time.\n\n"
                        "For example:\n\n"
                        "If you are in London, send <b>«0»</b>\n"
                        "If you are in Moscow, send <b>«3»</b>\n"
                        "If you are in Yekaterinburg, send <b>«5»</b>")

REGISTRATION_MESSAGE_RU = ("Сначала давайте синхронизируем наши часы.\n\n"
                           "Отправьте число, которое представляет разницу времени от среднего времени по Гринвичу.\n\n"
                           "Например:\n\n"
                           "Если вы в Лондоне, отправьте <b>«0»</b>\n"
                           "Если вы в Москве, отправьте <b>«3»</b>\n"
                           "Если вы в Екатеринбурге, отправьте <b>«5»</b>")

NOT_REGISTERED = ("You are not registered. Please, start the bot.\n\n"
                  "Вы не зарегистрированы. Пожалуйста, запустите бота.\n\n"
                  "/start")
