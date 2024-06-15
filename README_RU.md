# English Self-Check Bot
### Telegram Bot для Самопроверки Выученных Фраз

![python](https://img.shields.io/badge/python-3.9-blue)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.7.0-blue)

![pic](static/for_readme/header.gif)

[README - English](README_EN.md)

## Краткое описание:

Телеграм бот на aiogram для самопроверки выученных фраз английского языка.

## Идея:

В данном боте реализована идея работы с собственной памятью, на примере запоминания английских слов, фраз или выражений. При желании, шаблон бота можно применять для любой задачи, связанной с памятью. Добавляйте все, что хотите потом вспомнить и повторить: повторение изученного материала, мимолётные впечатления. Один из социальных функций такого шаблона может быть приложение для профилактики деменции.

![pic](static/for_readme/start.gif)

![pic](static/for_readme/lets_start.gif)

![pic](static/for_readme/settings.gif)

![pic](static/for_readme/audio.gif)

## Принцип работы бота:

- Вы добавляете в него любой текст на английском языке, после чего будет предложено ввести перевод. Также можно добавлять фразы аудио сообщением.
- Для проверки существует два режима: регулярный и спонтанный.
    - Регулярный режим: в настройках можно выбрать время суток, когда бот будет с периодичностью в 20 минут присылать фразы для проверки. Ответьте на сообщение переводом этой фразы.
    - Спонтанный режим: нажимая на кнопку “Let's check”, бот начинает присылать фразы одну за другой до тех пор, пока вы не остановите проверку.
- В настройках можно выбрать фразы, которые бот будет присылать: либо только те, которые добавили вы, либо все ваши вместе с фразами, предустановленными администратором бота.
- Удобный интерфейс с инлайн клавиатурой позволяет легко навигировать внутри бота, включая функцию переключения языка интерфейса.

## Основные команды:

- /start - запуск бота
- /help - инструкции по командам
- /add - добавить текст фразы в базу данных
- /menu - активация главного меню
- /settings - активация меню настроек
- /list - запрос списка фраз, которые добавил пользователь (присылает HTML файл с таблицей фраз и перевода)
- /delete - удаление фразы

**Примечания:**

- Для добавления фразы аудиосообщением не нужно использовать команду /add. Любое аудио сообщение бот интерпретирует как запрос на добавление.
- Любое сообщение, не являющееся спонтанным или ответом на фразу в регулярном режиме, будет удалено для предотвращения флуда. Если все сделано правильно, бот отправит сообщение “Correct” или “Incorrect”.

## Дополнительная информация:

- В директории находится шаблон базы данных example.db. Сделайте копию, переименовав ее в database.db. Работа с базой данных реализована с помощью sqlite3.
- Лимит пользователей - 100 человек. При использовании команды /start бот проверяет текущее количество человек.
- Для соблюдения лимита запросов (30 запросов в секунду) в модуле bot реализована проверка на количество пользователей.

## Зависимости:

- aiofiles==23.2.1
- aiogram==3.7.0
- aiohttp==3.9.5
- aiosignal==1.3.1
- annotated-types==0.7.0
- attrs==23.2.0
- certifi==2024.6.2
- frozenlist==1.4.1
- idna==3.7
- magic-filter==1.0.12
- multidict==6.0.5
- pydantic==2.7.4
- pydantic_core==2.18.4
- python-dotenv==1.0.1
- typing_extensions==4.12.2
- yarl==1.9.4

## Инструкция по установке:

1. Клонировать репозиторий
2. Создать виртуальное окружение в директории проекта

```bash
python -m venv .venv
```

3. Установить необходимые библиотеки

```bash
bashCopy code
pip install aiogram python-dotenv
```

4. Создайте файл .env и установить переменные окружения

```visual
BOT_TOKEN=YOUR_TOKEN
ADMIN_ID=YOUR_ID
```

5. Сделать копию файла базы данных `example.db` и переименовать в `database.db`, убедившись, что файл базы данных находится в директории `data/`.
6. Запустить файл `bot.py`.
7. Для развертывания бота через `systemd`, используйте пример unit-файла `english_check_bot.service`:

```visual
[Unit]
Description=English_Self_Check_Bot
After=network.target

[Service]
EnvironmentFile=/etc/environment
ExecStart=/path/to/project/EnglishSelfCheckBot_demo/.venv/bin/python /path/to/project/EnglishSelfCheckBot_demo/bot.py
ExecReload=/path/to/project/EnglishSelfCheckBot_demo/.venv/bin/python /path/to/project/EnglishSelfCheckBot_demo/bot.py
WorkingDirectory=/path/to/project/EnglishSelfCheckBot_demo/
KillMode=process
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

8. Добавьте unit-файл в systemd и активируйте сервис:

```bash
sudo systemctl enable english_check_bot.service
```

9. Запустите сервис:

```bash
sudo systemctl start english_check_bot.service
```