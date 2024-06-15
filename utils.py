"""
en: The module with utility functions.
ru: Модуль с утилитарными функциями.
"""
from datetime import datetime, timezone, timedelta
from io import StringIO


def detect_time(delta):
    datetime_now = datetime.now(timezone(timedelta(hours=delta)))
    return datetime_now


def create_html_info(name, phrases):
    """
    Create html file with user information
    """
    f = StringIO()
    f.write(
        "<!DOCTYPE html>\n"\
        "<html>\n"\
        "<head>\n"\
        "<meta charset=\"utf-8\">\n"\
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"\
        "<title>Users of bot</title>\n"\
        "<style>\n"\
        "table {\n"\
        "width: 100%;\n"\
        "border-collapse: collapse;\n"\
        "}\n"\
        "table, th, td {\n"\
        "border: 1px solid black;\n"\
        "}\n"\
        "th, td {\n"\
        "padding: 8px;\n"\
        "text-align: left;\n"\
        "}\n"\
        "th {\n"\
        "background-color: #f2f2f2;\n"\
        "}\n"\
        "</style>\n"\
        "</head>\n"\
        "<body>\n"\
        f"<h2 align=\"center\">Phrases of {name}</h2>\n"\
        f"<h3 align=\"center\">Count of phrases: {len(phrases)}</h3>\n"
        "<table align=\"center\" border='1'>\n"\
        "<tr>\n"\
        "<th>№</th>\n"\
        "<th>en_phrase</th>\n"\
        "<th>ru_phrase</th>\n"\
        "</tr>\n"
    )
    for n, phrase in enumerate(phrases, 1):
        f.write(
            "<tr>\n"\
            f"<td>{n}</td>\n"\
            f"<td>{phrase['en']}</td>\n"\
            f"<td>{phrase['ru']}</td>\n"\
            "</tr>\n"
        )
    f.write(
        "</table>\n"\
        "</body>\n"\
        "</html>"
    )
    return f.getvalue().encode('utf-8')
