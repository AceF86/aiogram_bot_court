import logging
import subprocess

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from aiogram_calendar import simple_cal_callback2, SimpleCalendar2
from aiogram.dispatcher.filters import Text
import speech_recognition as sr
from gtts import gTTS
from active_user import Database
from datetime import date
from config import TOKEN
from lemmatize_text import UkrainianStemmer
import keyboards as nav
import registering
import asyncio
import json

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    registering.sql_start()


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

db = Database("subscriber.db")


class GetCase(StatesGroup):
    case = State()


class GetWord(StatesGroup):
    surname = State()


class GetCalendar(StatesGroup):
    den = State()
    forma = State()
    judge = State()


class RegUser(StatesGroup):
    user_id = State()
    name = State()


class GetWordZka(StatesGroup):
    surname_zka = State()


class GetCaseZka(StatesGroup):
    case_zka = State()


class RegUserZka(StatesGroup):
    user_id_zka = State()
    name_zka = State()


class GetWordUg(StatesGroup):
    surname_ug = State()


class GetCaseUg(StatesGroup):
    case_ug = State()


class RegUserUg(StatesGroup):
    user_id_ug = State()
    name_ug = State()


class GetCalendarUg(StatesGroup):
    den = State()
    forma = State()
    judge = State()


class GetVoice(StatesGroup):
    voiceT = State()


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id, message.from_user.first_name)
        await message.answer("👋Доброго дня {0.first_name}!".format(message.from_user))
        with open("foto/PRC.jpg", "rb") as jpg:
            await message.answer_photo(
                jpg,
                "Я Віртуальний асистент <b>Перечинського районного суду</b>."
                "\n\nЯ вмію находити дату судового засідання за прізвищем,"
                " ім'ям і за номером справи, а також сповіщаю про дату "
                "і час засідання.\nЯкщо набрати команду /голос або \n/voice"
                ", я озвучу текст та надішлю вам його.",
            )
            await asyncio.sleep(1)
            await message.answer(
                "Наше спілкування буде проходити так:\n- Вибираєте🕹 розділ в меню"
                "\n- Натискаєте📲 на кнопки в меню\n- А я Вам відпишу📨.",
            )
            with open("data/prc.mp3", "rb") as file:
                await message.answer_voice(file, reply_markup=nav.mainMenu)


@dp.message_handler(commands=["check"])
async def check(message: types.Message):
    await registering.aql_read(message)


@dp.message_handler(commands=["checkpr"])
async def checkpr(message: types.Message):
    await registering.aql_read_pr(message)


@dp.message_handler(commands=["checkzka"])
async def checkzka(message: types.Message):
    await registering.aql_read_zka(message)


@dp.message_handler(commands=["voice", "голос"])
async def voice(message: types.Message):
    await message.answer(
        "{0.first_name} надішліть мені текстове повідомлення, а"
        " я озвучу і надішлю Вам його."
        "\n\nЩоб скасувати натисніть на👉 /cancel".format(message.from_user),
        reply_markup=nav.markupregistr,
    )
    await GetVoice.voiceT.set()


@dp.message_handler(commands=["uzhhorod", "ужгород"])
async def uzhhorod(message: types.Message):
    await message.answer(
        "{0.first_name} в даному розділі, нажавши🕹 на ниже вказані кнопки👇,"
        " можна подивитися дату засідання Ужгородського міськрайонного суду"
        " та підписатися на отриманя📩 сповіщення про дату, час "
        "судового засідання:"
        "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І. і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи⌨ - набираємо 304/555/20 і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 📩Push сповіщення - сервіс на отримання сповіщення"
        " дати засідання.\n\nЩоб озвучити текст введіть команду /голос або /voice.".format(
            message.from_user
        ),
        reply_markup=nav.markupsearch_ug,
    )


@dp.message_handler(content_types=["voice"])
async def voice_message_handler(message):
    with open("data/data_pr.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "data/voice.ogg")

        process = subprocess.run(
            ["ffmpeg\\ffmpeg.exe", "-i", "data/voice.ogg", "data/voice.wav"],
            input=b"y",
            stderr=subprocess.DEVNULL,
        )
        if process.returncode != 0:
            raise Exception("Something went wrong")

        response = {"success": True, "error": None, "transcription": None}
        try:
            r = sr.Recognizer()

            user_audio_file = sr.AudioFile("data/voice.wav")
            with user_audio_file as source:
                user_audio = r.record(source)
                text = r.recognize_google(user_audio, language="uk-UK")
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"

        stemObj = UkrainianStemmer(text.replace("'", " "))

        flag = True
        for i in data1:
            if stemObj.stem_word() in i["involved"].lower().replace('"', " ").replace(
                "'", " "
            ):
                news2 = (
                    f"Ваш запит: {text}\n\n"
                    f"Перечи́нський районний суд\n\n"
                    f"Суддя:{i['judge']}\n\n"
                    f"Номер справи:{i['number']}\n\n"
                    f"Дата/Час:<b>{i['date']}</b>\n\n"
                    f"Сторони по справі:\n<b>{i['involved']}</b>\n\n"
                    f"Суть позову:\n<b>{i['description']}</b>\n\n"
                    f"Форма судочинства:\n{i['forma']}"
                )
                await message.answer(news2, reply_markup=nav.mainMenu)
                flag = False

        if flag:
            await message.answer(
                f"Ваш запит: {text}\nЯкщо нічого не з'явилося, можливо неправильно введене слово або справа "
                f"ще не призначена до розгляду.\nВи також можете відвідати Наш вебпортал.",
                reply_markup=nav.mainMenu,
            )


# Головне меню
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == "🔙Назат в меню":
        await message.answer("Головне меню", reply_markup=nav.mainMenu)  # Головне меню

    elif message.text == "☎️Контактні данні":  # Головне меню
        await message.answer(
            "<u><b>{0.first_name} контактні дані:</b></u> \n\n\n📍 E-mail📧: "
            "inbox@pr.zk.court.gov.ua\n\n\n📍 Телефон📞: (03145)2-11-96\n\n\n📍 "
            "Адреса📮: пл. Народна, 15, м. Перечин, 89200.\n\n\n📍 Карти🗺 проїзду 🚖 👇.".format(
                message.from_user
            ),
            reply_markup=nav.markupkartu,
        )

    elif message.text == "🗺Карти проїзду":
        await message.answer("Карти проїзду 🚗.")
        with open("foto/perechin.jpg", "rb") as file:
            await message.answer_photo(file, reply_markup=nav.markupgeoa)
        with open("foto/perechin1.jpg", "rb") as file:
            await message.answer_photo(file, reply_markup=nav.markupgeo)

    elif message.text == "📢Оголошення про виклик":  # Головне меню
        await message.answer(
            "{0.first_name} перейшовши на вебпортал, можна передивитися всі "
            "оголошення про виклик до суду.".format(message.from_user),
            reply_markup=nav.markupnews,
        )

    elif message.text == "Відео інструкція":
        await message.answer(
            "{0.first_name} відео інструкція, як працювати в чаті."
            " Під кожною кнопкою є посилання на відео. При натисканні кнопки "
            "заявиться відео на дану тематику. Нажавши на *🔙Назат* "
            "все зникне.".format(message.from_user),
            reply_markup=nav.inline_button,
        )

    # Головне меню
    elif message.text == "📃Електронний Суд":
        with open("foto/electroniccourt.jpg", "rb") as file:
            await message.answer_photo(
                file,
                "{0.first_name} електронний суд дозволяє подавати учасникам судового"
                " процесу до суду документи в електронному вигляді, а також надсилати"
                " таким учасникам процесуальних документів в електронному вигляді, "
                "паралельно з документами у паперовому вигляді відповідно до "
                'процесуального законодавства.\n\n<a href="https://id.court.gov.ua/">'
                "Перейти в Електронний Суд🔗.</a>\n\n.".format(message.from_user),
                reply_markup=nav.markupmobileapp,
            )

    elif message.text == "📲Завантажити офіційний мобільний додаток єСуд":
        await message.answer(
            "Також Ви можете скористатися Нашим офіційним мобільним додатком <b>Електронного суду в "
            "Україні єСуд</b> призначеним для доступу до Електронного суду з мобільних пристроїв. "
            "<b>Для використання додатку Вам необхідно бути зареєстрованим в електронному "
            'кабінеті</b>.\n\n<a href="https://cabinet.court.gov.ua">Перейти в Електронний'
            " кабінет🔗.</a>\n\n.",
            reply_markup=nav.markup16,
        )

    # Головне меню
    elif message.text == "📝Заяви":
        await message.answer(
            "{0.first_name} графік📋 приймання громадян та видачі копій судових рішень.\n\n"
            "    <u>З ПН. по ПТ.</u>\nз 08:00🕗 до 17:00🕔\n\n  <u>Обідня перерва</u>\nз "
            "12:00🕛 до 13:00🕐\n\nВиберіть <b>зразок заяви</b> зі списку👇.".format(
                message.from_user
            ),
            reply_markup=nav.markuplist1,
        )

    elif message.text == "📑Список заяв":
        await message.answer("<b>Список заяв</b>📑", reply_markup=nav.markupexample)

    elif message.text == "📅Дата засідання":
        if message.chat.type == "private":
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id, message.from_user.first_name)
            await message.answer(
                "{0.first_name} в даному розділі можна подивитися дату засідання нажавши🕹 "
                "на ниже вказані кнопки👇:"
                "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І і відправляємо📥"
                "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи - набираємо 304/555/20 і відправляємо📥"
                "\n\n📍 Натискаємо📲 на 🗓️Пошук за датою - вибираємо дату і прізвище судді"
                "\n\nЩоб озвучити текст введіть команду /голос або /voice.".format(
                    message.from_user
                ),
                reply_markup=nav.markupsearch,
            )

    # Головне меню
    elif message.text == "🔖Пошук за номером справи":
        await message.answer(
            "{0.first_name} набираємо⌨ згідно зразків "
            "304/555/20 або 555/20 і відправляємо📥."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /stop.".format(message.from_user),
            reply_markup=nav.markupstop,
        )
        await GetCase.case.set()

    elif message.text == "🗓️Пошук за датою":
        await message.answer(
            "{0.first_name} щоб розпочати пошук виберіть дату та слідуйте👉 подальшим інструкціям."
            " Щоб скасувати пошук натисніть на👉 /stop.".format(message.from_user),
            reply_markup=await SimpleCalendar().start_calendar(),
        )

        await GetCalendar.den.set()

    elif message.text == "🎫Пошук за прізвищем та ім’ям":
        await message.answer(
            "{0.first_name} набирати можна з малої букви, а апостроф в тексті "
            "заміняємо на пробіл."
            "\n\n<b>Попередження</b>❗, якщо буде введено тільки прізвище або ім’я, "
            "то Вам видасть всі засідання призначені на дане прізвище або ім’я."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /stop.".format(message.from_user),
            reply_markup=nav.markupstop,
        )
        await GetWord.surname.set()

    elif message.text == "📩Push сповіщення":
        await message.answer(
            "{0.first_name} в цьому розділі можна скористатися сервісом *<b>Push"
            " сповіщення</b>*.\nСуть сервісу проста, Ви отримаєте📩 сповіщення про дату, час "
            "судового засідання.\n\nЩоб підписатися✍🏻 на сервіс Вам потрібно набрати⌨ "
            "*<b>так</b>* і відправити📥 та слідувати👉 подальшим інструкціям."
            "\n\nЩоб скасувати підписку натисніть\nна👉 /cancel.".format(
                message.from_user
            ),
            reply_markup=nav.markupregistr,
        )
        await RegUser.user_id.set()

    elif message.text == "⚖️Апеляційний суд":  # Головне меню
        if message.chat.type == "private":
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id, message.from_user.first_name)
            await message.answer(
                "{0.first_name} в даному розділі, нажавши🕹 на ниже вказані кнопки👇,"
                " можна подивитися дату засідання Закарпатського апеляційного суду"
                " та підписатися на отриманя📩 сповіщення про дату, час "
                "судового засідання:"
                "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І. і відправляємо📥"
                "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи⌨ - набираємо 304/555/20 і відправляємо📥"
                "\n\n📍 Натискаємо📲 на 📩Push сповіщення - сервіс на отримання сповіщення"
                " дати засідання.\n\nЩоб озвучити текст введіть команду /голос або /voice.".format(
                    message.from_user
                ),
                reply_markup=nav.markupsearch_zka,
            )

    elif message.text == "🎫Пошук за прізвищем та ім’ям zka":
        await message.answer(
            "{0.first_name} набирати можна з малої букви, а апостроф в тексті "
            "заміняємо на пробіл.\n\n<b>Попередження</b>❗, якщо буде введено "
            "тільки прізвище або ім’я, то Вам видасть всі засідання призначені на "
            "дане прізвище або ім’я."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /pass.".format(message.from_user),
            reply_markup=nav.markuppass,
        )
        await GetWordZka.surname_zka.set()

    elif message.text == "🔖Пошук за номером справи zka":
        await message.answer(
            "{0.first_name} набираємо⌨ згідно зразків "
            "304/555/20 або 555/20 і відправляємо📥."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /pass.".format(message.from_user),
            reply_markup=nav.markuppass,
        )
        await GetCaseZka.case_zka.set()

    elif message.text == "📩Push сповіщення zka":
        await message.answer(
            "{0.first_name} в цьому розділі можна скористатися сервісом *<b>Push"
            " сповіщення</b>*.\nСуть сервісу проста, Ви отримаєте📩 сповіщення про дату, час "
            "судового засідання.\n\nЩоб підписатися✍🏻 на сервіс Вам потрібно набрати⌨ "
            "*<b>так</b>* і відправити📥 та слідувати👉 подальшим інструкціям."
            "\n\nЩоб скасувати підписку натисніть \nна👉 /refuse.".format(
                message.from_user
            ),
            reply_markup=nav.markupregistr_zka,
        )
        await RegUserZka.user_id_zka.set()

    elif message.text == "🎫Пошук за прізвищем та ім’ям ug":
        await message.answer(
            "{0.first_name} набирати можна з малої букви, а апостроф в тексті "
            "заміняємо на пробіл.\n\n<b>Попередження</b>❗, якщо буде введено "
            "тільки прізвище або ім’я, то Вам видасть всі засідання призначені на "
            "дане прізвище або ім’я."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /no.".format(message.from_user),
            reply_markup=nav.markuppasug,
        )
        await GetWordUg.surname_ug.set()

    elif message.text == "🔖Пошук за номером справи ug":
        await message.answer(
            "{0.first_name} набираємо⌨ згідно зразків "
            "304/555/20 або 555/20 і відправляємо📥."
            "\n\nЩоб скасувати пошук натисніть \nна👉 /no.".format(message.from_user),
            reply_markup=nav.markuppasug,
        )
        await GetCaseUg.case_ug.set()

    elif message.text == "📩Push сповіщення ug":
        await message.answer(
            "{0.first_name} в цьому розділі можна скористатися сервісом *<b>Push"
            " сповіщення</b>*.\nСуть сервісу проста, Ви отримаєте📩 сповіщення про дату, час "
            "судового засідання.\n\nЩоб підписатися✍🏻 на сервіс Вам потрібно набрати⌨ "
            "*<b>так</b>* і відправити📥 та слідувати👉 подальшим інструкціям."
            "\n\nЩоб скасувати підписку натисніть \nна👉 /refuseg.".format(
                message.from_user
            ),
            reply_markup=nav.markupregistr_ug,
        )
        await RegUserUg.user_id_ug.set()

    elif message.text == "🗓️Пошук за датою ug":
        await message.answer(
            "{0.first_name} щоб розпочати пошук виберіть дату та слідуйте👉 подальшим інструкціям."
            " Щоб скасувати пошук натисніть на👉 /no.".format(message.from_user),
            reply_markup=await SimpleCalendar2().start_calendar(),
        )

        await GetCalendarUg.den.set()


@dp.message_handler(state="*", commands=["stop", "стоп"])
@dp.message_handler(Text(equals="stop", ignore_case=True), state="*")
async def stop_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK!👌", reply_markup=nav.markupsearch)


@dp.message_handler(state="*", commands=["pass", "пропустити"])
@dp.message_handler(Text(equals="pass", ignore_case=True), state="*")
async def pass_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK!👌", reply_markup=nav.markupsearch_zka)


@dp.message_handler(state="*", commands=["no", "пропустити."])
@dp.message_handler(Text(equals="no", ignore_case=True), state="*")
async def pass_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK!👌", reply_markup=nav.markupsearch_ug)


# пошук дати засідання
@dp.message_handler(state=GetCase.case, content_types=types.ContentTypes.TEXT)
async def case_handler(message: types.Message, state: FSMContext):
    with open("data/data_pr.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

    flag = True
    for i in data1:
        if message.text in i["number"]:
            news1 = (
                f"Суддя: {i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news1,
                reply_markup=nav.markupsearch,
            )

            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введений номер справи або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати Наш вебпортал.",
            reply_markup=nav.markuphome,
        )


# пошук дати засыдання за словом
@dp.message_handler(state=GetWord.surname, content_types=types.ContentTypes.TEXT)
async def word_handler(message: types.Message, state: FSMContext):
    with open("data/data_pr.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        stemObj = UkrainianStemmer(message.text.replace("'", " "))

    flag = True
    for i in data1:
        if stemObj.stem_word() in i["involved"].lower().replace('"', " ").replace(
            "'", " "
        ):
            news2 = (
                f"Суддя: {i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news2,
                reply_markup=nav.markupsearch,
            )
            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введене слово або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати Наш вебпортал.",
            reply_markup=nav.markuphome,
        )


# пошук дати за датою каленрдаря та прізвищем судді
@dp.callback_query_handler(simple_cal_callback.filter(), state=GetCalendar.den)
async def process_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        den = date.strftime("%d.%m.%Y")
        await state.update_data({"den": den})

        await callback_query.message.answer(
            "Виберіть одне з форм судочинства. Щоб скасувати пошук натисніть на👉 /stop.",
            reply_markup=nav.inline_butforma,
        )
        await GetCalendar.forma.set()

@dp.callback_query_handler(text=["today"], state=GetCalendar.den)
async def calendar_handler(callback_query: types.CallbackQuery, state: FSMContext):
   if callback_query.data == "today":
       await callback_query.message.delete_reply_markup()

       today = date.today()
       den = today.strftime("%d.%m.%Y")
       await state.update_data({"den": den})

   await callback_query.message.answer(
           "Виберіть одне з форм судочинства. Щоб скасувати пошук натисніть на👉 /stop.",
           reply_markup=nav.inline_butforma,
       )
   await GetCalendar.forma.set()


@dp.callback_query_handler(text=["адмін", "цивіл", "крим", "всі"], state=GetCalendar.forma)
async def calendar_handler(callback_query: types.CallbackQuery, state: FSMContext):
    global b
    await callback_query.answer()
    if callback_query.data == "адмін":
        b = "Адміністративні правопорушення"
    elif callback_query.data == "цивіл":
        b = "Цивільне судочинство"
    elif callback_query.data == "крим":
        b = "Кримінальне судочинство"
    elif callback_query.data == "всі":
        b = ""

    forma = b
    await state.update_data({"forma": forma})
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(
        "Виберіть одне з прізвищ. Щоб скасувати пошук натисніть на👉 /stop.",
        reply_markup=nav.inline_butj,
    )
    await GetCalendar.judge.set()


@dp.callback_query_handler(
    text=["гевці", "чепурнов", "ганько", "all"], state=GetCalendar.judge
)
async def calendar_handler(callback_query: types.CallbackQuery, state: FSMContext):
    with open("data/data_pr.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        data = await state.get_data()
        den = data.get("den")
        forma = data.get("forma")

        await callback_query.answer()
        if callback_query.data == "гевці":
            a = "Гевці В.М."
        elif callback_query.data == "чепурнов":
            a = "Чепурнов В.О."
        elif callback_query.data == "ганько":
            a = "Ганько І.І."
        elif callback_query.data == "all":
            a = ""
        await callback_query.message.delete_reply_markup()

        flag = True

        for i in data1:
            if den in i["date"] and a in i["judge"] and forma in i["forma"]:
                news3 = (
                    f"Суддя: {i['judge']}\n"
                    f"Номер справи: {i['number']}\n"
                    f"Дата/Час: <b>{i['date']}</b> год.\n"
                    f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                    f"Суть позову:\n<b>{i['description']}</b>\n"
                    f"{i['forma']}"
                )

                await state.finish()
                await callback_query.message.answer(
                    news3,
                    reply_markup=nav.markupsearch,
                )
                flag = False

        if flag:
            await state.finish()
            await callback_query.message.answer(
                "Якщо інформація не з'явилася, можливо неправильно введені дані або справа "
                "ще не призначена до розгляду.\nВи також можете відвідати Наш вебпортал.",
                reply_markup=nav.markuphome,
            )


@dp.message_handler(state="*", commands=["cancel", "відмова"])
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK👌", reply_markup=nav.mainMenu)


# реєстрація на message push
@dp.message_handler(state=RegUser.user_id, content_types=types.ContentTypes.TEXT)
async def regUser_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["user_id"] = message.from_user.id

    await message.answer(
        "{0.first_name} наберіть⌨ прізвище та ім'я або номер справи і відправте📥."
        "\n\n<b>Попередження</b>❗ \nПрізвище та ім'я набирати можна з малої букви, а"
        " апостроф в тексті "
        "заміняється на пробіл.\n\nЩодо номера справи набираємо⌨ відповідно до зразків "
        "304/555/20 або 555/20.\nІнформацію вказуйте правильно💯."
        "\n\nПісля сповіщення <b>підписка видалиться</b>🗑."
        "\n\nЩоб скасувати підписку натисніть \nна👉 /cancel.".format(message.from_user),
        reply_markup=nav.markupregistr,
    )
    await RegUser.name.set()


@dp.message_handler(state=RegUser.name, content_types=types.ContentTypes.TEXT)
async def regUser2_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        stemObj = UkrainianStemmer(message.text)

        data["name"] = stemObj.stem_word()

    await registering.sql_add_command(state)

    await state.finish()
    await message.answer(
        "{0.first_name} Ви підписалися👍, очікуйте на сповіщення.".format(
            message.from_user
        ),
        reply_markup=nav.mainMenu,
    )


@dp.message_handler(state=GetCaseZka.case_zka, content_types=types.ContentTypes.TEXT)
async def caseZka_handler(message: types.Message, state: FSMContext):
    with open("data/data_zka.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

    flag = True
    for i in data1:
        if message.text in i["number"]:
            news1 = (
                f"Склад суду:\n{i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news1,
                reply_markup=nav.markupsearch_zka,
            )
            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введений номер справи або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати вебпортал"
            " Закарпатського апеляційного суду.",
            reply_markup=nav.markup_zka,
        )


@dp.message_handler(state=GetWordZka.surname_zka, content_types=types.ContentTypes.TEXT)
async def wordZka_handler(message: types.Message, state: FSMContext):
    with open("data/data_zka.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        stemObj = UkrainianStemmer(message.text.replace("'", " "))

    flag = True
    for i in data1:
        if stemObj.stem_word() in i["involved"].lower().replace('"', " ").replace(
            "'", " "
        ):
            news1 = (
                f"Склад суду:\n{i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news1,
                reply_markup=nav.markupsearch_zka,
            )
            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введене слово або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати вебпортал"
            " Закарпатського апеляційного суду.",
            reply_markup=nav.markup_zka,
        )


@dp.message_handler(state=RegUserZka, commands=["refuse", "відмовляюся"])
@dp.message_handler(Text(equals="refuse", ignore_case=True), state=RegUserZka)
async def regUserZka_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK👌", reply_markup=nav.markupsearch_zka)


@dp.message_handler(state=RegUserZka.user_id_zka, content_types=types.ContentTypes.TEXT)
async def regUserZka1_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["user_id"] = message.from_user.id

    await message.answer(
        "{0.first_name} наберіть⌨ прізвище та ім'я або номер справи і відправте📥."
        "\n\n<b>Попередження</b>❗ \nПрізвище та ім'я набирати можна з малої букви, а "
        "апостроф в тексті "
        "заміняється на пробіл.\n\nЩодо номера справи набираємо⌨ відповідно до зразків "
        "304/555/20 або 555/20.\nІнформацію вказуйте правильно💯."
        "\n\nПісля сповіщення <b>підписка видалиться</b>🗑."
        "\n\nЩоб скасувати підписку натисніть \nна👉 /refuse.".format(message.from_user),
        reply_markup=nav.markupregistr_zka,
    )
    await RegUserZka.name_zka.set()


@dp.message_handler(state=RegUserZka.name_zka, content_types=types.ContentTypes.TEXT)
async def regUserZka2_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        stemObj = UkrainianStemmer(message.text)

        data["name"] = stemObj.stem_word()

    await registering.sql_add_command_zka(state)

    await state.finish()
    await message.answer(
        "{0.first_name} Ви підписалися👍, очікуйте на сповіщення.".format(
            message.from_user
        ),
        reply_markup=nav.mainMenu,
    )


@dp.message_handler(state=GetCaseUg.case_ug, content_types=types.ContentTypes.TEXT)
async def caseUg_handler(message: types.Message, state: FSMContext):
    with open("data/data_ug.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

    flag = True
    for i in data1:
        if message.text in i["number"]:
            news1 = (
                f"Суддя: {i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news1,
                reply_markup=nav.markupsearch_ug,
            )
            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введений номер справи або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати вебпортал"
            " Ужгородського міськрайонного суду.",
            reply_markup=nav.markup_ug,
        )


@dp.message_handler(state=GetWordUg.surname_ug, content_types=types.ContentTypes.TEXT)
async def wordUg_handler(message: types.Message, state: FSMContext):
    with open("data/data_ug.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        stemObj = UkrainianStemmer(message.text.replace("'", " "))

    flag = True
    for i in data1:
        if stemObj.stem_word() in i["involved"].lower().replace('"', " ").replace(
            "'", " "
        ):
            news1 = (
                f"Суддя: {i['judge']}\n"
                f"Номер справи: {i['number']}\n"
                f"Дата/Час: <b>{i['date']}</b> год.\n"
                f"Сторони по справі:\n<b>{i['involved']}</b>\n"
                f"Суть позову:\n<b>{i['description']}</b>"
            )
            await state.finish()
            await message.answer(
                news1,
                reply_markup=nav.markupsearch_ug,
            )
            flag = False

    if flag:
        await state.finish()
        await message.answer(
            "Якщо нічого не з'явилося, можливо неправильно введене слово або справа "
            "ще не призначена до розгляду.\nВи також можете відвідати вебпортал"
            " Ужгородського міськрайонного суду.",
            reply_markup=nav.markup_ug,
        )


@dp.message_handler(state="*", commands=["refuseg", "відмовляюся."])
@dp.message_handler(Text(equals="refuseg", ignore_case=True), state="*")
async def regUserZka_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("OK👌", reply_markup=nav.markupsearch_ug)


@dp.message_handler(state=RegUserUg.user_id_ug, content_types=types.ContentTypes.TEXT)
async def regUserUg_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["user_id"] = message.from_user.id

    await message.answer(
        "{0.first_name} наберіть⌨ прізвище та ім'я або номер справи і відправте📥."
        "\n\n<b>Попередження</b>❗ \nПрізвище та ім'я набирати можна з малої букви, а "
        "апостроф в тексті "
        "заміняється на пробіл.\n\nЩодо номера справи набираємо⌨ відповідно до зразків "
        "304/555/20 або 555/20.\nІнформацію вказуйте правильно💯."
        "\n\nПісля сповіщення <b>підписка видалиться</b>🗑."
        "\n\nЩоб скасувати підписку натисніть \nна👉 /refuseg.".format(
            message.from_user
        ),
        reply_markup=nav.markupregistr_ug,
    )
    await RegUserUg.name_ug.set()


@dp.message_handler(state=RegUserUg.name_ug, content_types=types.ContentTypes.TEXT)
async def regUserUg_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        stemObj = UkrainianStemmer(message.text)

        data["name"] = stemObj.stem_word()

    await registering.sql_add_command_ug(state)

    await state.finish()
    await message.answer(
        "{0.first_name} Ви підписалися👍, очікуйте на сповіщення.".format(
            message.from_user
        ),
        reply_markup=nav.markupsearch_ug,
    )

@dp.callback_query_handler(simple_cal_callback2.filter(), state=GetCalendarUg.den)
async def process_calendar_ug(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar2().process_selection(callback_query, callback_data)
    if selected:
        den = date.strftime("%d.%m.%Y")
        await state.update_data({"den": den})

        await callback_query.message.answer(
            "Пропишіть одне з прізвищ. Щоб скасувати пошук натисніть на👉 /no.",
           reply_markup=nav.inline_butforma2,
        )
        await GetCalendarUg.forma.set()

@dp.callback_query_handler(text=["today2"], state=GetCalendarUg.den)
async def calendar_handler(callback_query: types.CallbackQuery, state: FSMContext):
   if callback_query.data == "today2":
       await callback_query.message.delete_reply_markup()

       today = date.today()
       den = today.strftime("%d.%m.%Y")
       await state.update_data({"den": den})

       await callback_query.message.answer(
           "Виберіть одне з форм судочинства. Щоб скасувати пошук натисніть на👉 /no.",
           reply_markup=nav.inline_butforma2,
       )
       await GetCalendarUg.forma.set()


@dp.callback_query_handler(text=["адмін2", "цивіл2", "крим2", "всі2"], state=GetCalendarUg.forma)
async def calendar_handler2(callback_query: types.CallbackQuery, state: FSMContext):
    global c
    await callback_query.answer()
    if callback_query.data == "адмін2":
        c = "Адміністративні правопорушення"
    elif callback_query.data == "цивіл2":
        c = "Цивільне судочинство"
    elif callback_query.data == "крим2":
        c = "Кримінальне судочинство"
    elif callback_query.data == "всі2":
        c = ""

    forma = c
    await state.update_data({"forma": forma})
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(
            "Виберіть одне з прізвищ. Щоб скасувати пошук натисніть на👉 /no.",
            reply_markup=nav.inline_butjua,
        )
    await GetCalendarUg.judge.set()


@dp.callback_query_handler(
    text=["дергачова", "дегтяренко", "деметрадзе",
        "данко", "логойда", "лемак", "голяна", "придачук",
        "сарай", "малюк", "бедьо","бенца",
          "фазикош", "шумило", "шепетко","іванов",
        "зарева", "крегул", "хамник","all"], state=GetCalendarUg.judge
)
async def calendar_handler(callback_query: types.CallbackQuery, state: FSMContext):
    with open("data/data_ug.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        data1 = json.loads(file_content)

        data = await state.get_data()
        den = data.get("den")
        forma = data.get("forma")

        await callback_query.answer()
        if callback_query.data == "дергачова":
            j = "Дергачова Н.В."
        elif callback_query.data == "дегтяренко":
            j = "Дегтяренко К.С."
        elif callback_query.data == "деметрадзе":
            j = "Деметрадзе Т.Р."
        elif callback_query.data == "данко":
            j = "Данко В.Й."
        elif callback_query.data == "логойда":
            j = "Логойда І.В."
        elif callback_query.data == "лемак":
            j = "Лемак О.В."
        elif callback_query.data == "голяна":
            j = "Голяна О.В."
        elif callback_query.data == "придачук":
            j = "Придачук О.А."
        elif callback_query.data == "сарай":
            j = "Сарай А.І."
        elif callback_query.data == "малюк":
            j = "Малюк В.М."
        elif callback_query.data == "бедьо":
            j = "Бедьо В.І."
        elif callback_query.data == "бенца":
            j = "Бенца К.К."
        elif callback_query.data == "фазикош":
            j = "Фазикош О.В."
        elif callback_query.data == "шумило":
            j = "Шумило Н.Б."
        elif callback_query.data == "шепетко":
            j = "Шепетко І.О."
        elif callback_query.data == "іванов":
            j = "Іванов А.П."
        elif callback_query.data == "зарева":
            j = "Зарева Н.І."
        elif callback_query.data == "крегул":
            j = "Крегул М.М."
        elif callback_query.data == "хамник":
            j = "Хамник М.М."
        elif callback_query.data == "all":
            j = ""
        await callback_query.message.delete_reply_markup()

        flag = True

        for i in data1:
            if den in i["date"] and forma in i["forma"] and j in i["judge"]:
                news3 = (
                    f"Суддя : {i['judge']}\n"
                    f"Номер справи : {i['number']}\n"
                    f"Дата/Час : <b>{i['date']}</b> год.\n"
                    f"Сторони по справі :\n<b>{i['involved']}</b>\n"
                    f"Суть : <b>{i['description']}</b>\n"
                    f"{i['forma']}"
                )

                await state.finish()
                await callback_query.message.answer(
                    news3,
                    reply_markup=nav.markupsearch_ug,
                )
                flag = False

        if flag:
            await state.finish()
            await callback_query.message.answer(
                "Якщо нічого не з'явилося, можливо неправильно введене слово або справа "
                "ще не призначена до розгляду.\nВи також можете відвідати вебпортал"
                " Ужгородського міськрайонного суду.",
                reply_markup=nav.markup_ug,)


@dp.callback_query_handler(text="menusearch")
async def callback_btn(callback_query: types.CallbackQuery):
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    await callback_query.message.answer(
        "В даному розділі можна подивитися дату засідання нажавши🕹 "
        "на ниже вказані кнопки👇:"
        "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи - набираємо 304/555/20 і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 🗓️Пошук за датою - вибираємо дату і прізвище судді",
        reply_markup=nav.markupsearch,
    )
    await callback_query.answer("Розділ 📅Дата засідання")


@dp.callback_query_handler(text="menuzka")
async def callback_btn2(callback_query: types.CallbackQuery):
    await bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    await callback_query.message.answer(
        "В даному розділі, нажавши🕹 на ниже вказані кнопки👇,"
        " можна подивитися дату засідання Закарпатського апеляційного суду"
        " та підписатися на отриманя📩 сповіщення про дату, час "
        "судового засідання:"
        "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І. і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи⌨ - набираємо 304/555/20 і "
        "відправляємо📥 "
        "\n\n📍 Натискаємо📲 на 📩Push сповіщення - сервіс на отримання сповіщення"
        " дати засідання.",
        reply_markup=nav.markupsearch_zka,
    )
    await callback_query.answer("Розділ ⚖️Апеляційний суд")


@dp.callback_query_handler(text="menuug")
async def callback_btn3(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,message_id=callback_query.message.message_id,)
    await callback_query.message.answer(
        "{0.first_name} в даному розділі, нажавши🕹 на ниже вказані кнопки👇,"
        " можна подивитися дату засідання Ужгородського міськрайонного суду"
        " та підписатися на отриманя📩 сповіщення про дату, час "
        "судового засідання:"
        "\n\n📍 Натискаємо📲 на 🎫Пошук за прізвищем та ім’ям - набираємо П.І. і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 🔖Пошук за номером справи⌨ - набираємо 304/555/20 і відправляємо📥"
        "\n\n📍 Натискаємо📲 на 📩Push сповіщення - сервіс на отримання сповіщення"
        " дати засідання.\n\nЩоб озвучити текст введіть команду /голос або /voice.".format(
            callback_query.message.from_user
        ),
        reply_markup=nav.markupsearch_ug,
    )
    await callback_query.answer("Розділ ⚖Ужгородського міськрайонного суду")


@dp.message_handler(state=GetVoice.voiceT, content_types=types.ContentTypes.TEXT)
async def voice_handler(message: types.Message, state: FSMContext):
    text = message.text
    tts = gTTS(text=text, lang="uk", tld="com.ua")
    tts.save(f"data/{message.from_user.first_name}.mp3")
    await state.finish()
    with open(f"data/{message.from_user.first_name}.mp3", "rb") as speech:
        await bot.send_audio(
            message.from_user.id,
            speech,
            title="Озвучений текст",
            reply_markup=nav.mainMenu,
        )


@dp.callback_query_handler(
    text=["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"]
)
async def callback_btn3(callback_query: types.CallbackQuery):
    if callback_query.data == "v0":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer("Головне меню", reply_markup=nav.mainMenu)
    elif callback_query.data == "v1":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/vxn_-h8BVnc", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v2":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/ultbtXfQJvE", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v3":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/kBlQHQLqx68", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v4":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/Hw1HshMi6hQ", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v5":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/94yAoQngPKI", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v6":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/9Jl-YflKoXM", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v7":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/GetzQq-09qU", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v8":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/g20JeR9GMKY", reply_markup=nav.inline_button
        )
    elif callback_query.data == "v9":
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
        )
        await callback_query.message.answer(
            text="https://youtu.be/5K32OzR7eMU", reply_markup=nav.inline_button
        )
    await callback_query.answer()


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except:
        pass
