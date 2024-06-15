"""
en: This is a configuration file for the bot. Here are the main settings and variables.
ru: Это файл конфигурации для бота. Здесь находятся основные настройки и переменные.
"""

import dotenv
import os

from db import Database

dotenv.load_dotenv()

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Load database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "data", "database.db")

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

DB = Database(DATABASE_PATH)

# en: List for the time check
# ru: Список времени проверки
TIME_CHECK = [
    lambda x: 8 <= x <= 13,
    lambda x: 13 <= x <= 18,
    lambda x: 18 <= x <= 23
]

# Dicts for create tables in database

USERS_TABLE = {
    "table_name": "users",
    "fields": {
        "user_id": "INTEGER NOT NULL PRIMARY KEY",
        "full_name": "TEXT NOT NULL",
        "time_check": "INTEGER NOT NULL",
        "only_self": "INTEGER NOT NULL",
        "time_zone": "INTEGER NOT NULL"
    },
    "foreign_keys": None
}

CONTENT_TABLE = {
    "table_name": "content",
    "fields": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "en": "TEXT NOT NULL",
        "ru": "TEXT NOT NULL"
    },
    "foreign_keys": {
        "key": "user_id",
        "reference": "users(user_id)",
        "on_delete": "CASCADE",
        "on_update": "CASCADE"
    }
}

VOICE_TABLE = {
    "table_name": "voice",
    "fields": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "file_unique_id": "TEXT NOT NULL",
        "file_id": "TEXT NOT NULL",
        "translate": "TEXT NOT NULL"
    },
    "foreign_keys": {
        "key": "user_id",
        "reference": "users(user_id)",
        "on_delete": "CASCADE",
        "on_update": "CASCADE"
    }
}

IMG_BOT_TABLE = {
    "table_name": "img_bot",
    "fields": {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "file_path": "TEXT NOT NULL",
        "file_id": "TEXT NOT NULL"
    },
    "foreign_keys": None
}
