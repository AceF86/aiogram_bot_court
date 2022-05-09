import time
from telegram.ext import Updater
from telegram import ParseMode
from config import TOKEN, MASTER
import sqlite3
import json

token = TOKEN
admin_id = MASTER
json_file = "data/data_pr.json"
sqlite_file = "subscriber.db"

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
updater = Updater(token)


def send_msg(chat_id, message):
    updater.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)


def check2(json_data, sql_data):
    result = []
    for client in sql_data:
        for check_data in json_data:
            if check_data["number"].find(client[1]) > -1:
                result.append((client, check_data))
    return result


def del_by_name(name):
    cur.execute(f'DELETE FROM list_pr WHERE case_involved="{name}"')
    conn.commit()


def main():
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    cur.execute("SELECT * FROM list_pr")
    clients = cur.fetchall()
    res2 = check2(json_data, clients)

    for row, i in res2:

        msg = (
            f"👋 Доброго дня!\nЗапит за номером справи <b>{row[1]}</b>, знайдено:"
            f"\nПеречинський районний суд\n"
            f"\nДата/Час засідання:\n<b>{i['date']} год.</b>\n\n"
            f"Номер справи: № {i['number']}\nСуддя:{i['judge']}\n\n"
            f"Сторони по справі:\n<b>{i['involved']}</b>\n\n"
            f"Суть позову:\n<b>{i['description']}</b>\n\n"
            f"📲 Також подивитися дату судового засідання можна на "
            f"\nвебпорталі https://pr.zk.court.gov.ua/."
            f"\n\n<b>Підписка видаленна</b>🗑."
        )
        try:
            send_msg(row[0], msg)
            time.sleep(20)
        except Exception as ex:
            msg = f"Неможливо {ex} відправити повідомлення:\n{msg}"
            send_msg(admin_id, msg)
        else:
            del_by_name(row[1])

    return res2


main()
