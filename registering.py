import sqlite3
import keyboards as nav
from aiogram import Bot, types
from config import TOKEN


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)


def sql_start():
    global conn, cur
    conn = sqlite3.connect("subscriber.db")
    cur = conn.cursor()
    if conn:
        print("Data base connected OK!")
    cur.execute("CREATE TABLE IF NOT EXISTS list_pr(user_id, case_involved)")
    cur.execute("CREATE TABLE IF NOT EXISTS list_zka(user_id, involved)")
    cur.execute("CREATE TABLE IF NOT EXISTS list_ug(user_id, involved)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS list_user("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "user_id INTEGER UNIQUE NOT NULL,"
        " first_name UNIQUE NOT NULL, "
        "active INTEGER DEFAULT 1)"
    )
    conn.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO list_pr VALUES (?, ?)", tuple(data.values()))
        conn.commit()


async def sql_add_command_zka(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO list_zka VALUES (?, ?)", tuple(data.values()))
        conn.commit()


async def sql_add_command_ug(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO list_ug VALUES (?, ?)", tuple(data.values()))
        conn.commit()


async def aql_read(message):
    for ret in cur.execute("SELECT * FROM list_user").fetchall():
        await bot.send_message(
            message.chat.id,
            f"Статистика користувачів" f":\n\n№ : <b>{ret[0]}</b>\nІм'я: {ret[2]}",
            reply_markup=nav.mainMenu,
        )


async def aql_read_pr(message):
    for ret in cur.execute("SELECT * FROM list_pr").fetchall():
        await bot.send_message(
            message.chat.id,
            f"Статистика записів по"
            f"\nПеречинському районному суду"
            f"\nзапит: {ret[1]}",
            reply_markup=nav.mainMenu,
        )


async def aql_read_zka(message):
    for ret in cur.execute("SELECT * FROM list_zka").fetchall():
        await bot.send_message(
            message.chat.id,
            f"Статистика записів по"
            f"\nЗакарпатському апеляційному суду"
            f"\nзапит: {ret[1]}",
            reply_markup=nav.mainMenu,
        )
