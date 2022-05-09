from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

btnMain = KeyboardButton("🔙Назат в меню")
# головне меню і кнопки до бота
btnDate = KeyboardButton("📅Дата засідання")
btnName = KeyboardButton("📩Push сповіщення")
btnDistribution = KeyboardButton("⚖️Апеляційний суд")
btnnudity = KeyboardButton("📢Оголошення про виклик")
btnContacts = KeyboardButton("☎️Контактні данні")
btnStatements = KeyboardButton("📝Заяви")
btnelectroniccourt = KeyboardButton("📃Електронний Суд")
btnevideo = KeyboardButton("Відео інструкція")

mainMenu = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(btnDate, btnName)
    .add(btnStatements, btnContacts)
    .add(btnDistribution, btnnudity)
    .add(btnelectroniccourt, btnevideo)
)

# конопки силка на  Геолокация
markupgeo = InlineKeyboardMarkup(row_width=1)
btngeo = InlineKeyboardButton(
    text="Переміститися на Google Карту", url="https://goo.gl/maps/sNThx2MEs5VCuy2z9"
)
markupgeo.insert(btngeo)

markupgeoa = InlineKeyboardMarkup(row_width=1)
btngeo1 = InlineKeyboardButton(
    text="Переміститися на Apple Карту",
    url="https://maps.apple.com/place?address=48.735389,22.476694&q",
)
markupgeoa.insert(btngeo1)

markuvideo = InlineKeyboardMarkup(row_width=1)
btnvideo1 = InlineKeyboardButton(
    text="Перегляд відео огляду", url="https://youtu.be/4sZwHyHm5HQ"
)
markuvideo.insert(btnvideo1)


# конопки на  Заяви
markupexample = InlineKeyboardMarkup(row_width=1)
btnexamples = InlineKeyboardButton(
    text="Про визнання прав в порядку спадкування",
    url="https://telegra.ph/Pro-viznannya-prav-v-poryadku-spadkuvannya-11-19",
)
btnexamples1 = InlineKeyboardButton(
    text="Про притягнення мене до відповід.КУпАП",
    url="https://telegra.ph/Zrazok-zayavi-pro-prityagnennya-mene-do-v%D1%96dpov%D1%96dalnost%D1%96-za-st-KUpAP-11-19",
)
btnexamples2 = InlineKeyboardButton(
    text="Про розірвання шлюбу та стяг. аліментів",
    url="https://telegra.ph/Zrazok-zayavi-pro-roz%D1%96rvannya-shlyubu-ta-styagnennya-al%D1%96ment%D1%96v-11-19",
)
btnexamples3 = InlineKeyboardButton(
    text="Про видачу виконавчого листа",
    url="https://telegra.ph/Zrazok-zayavi-na-vidachuvikonavchogo-lista-u-civ%D1%96ln%D1%96j-sprav%D1%96-11-19",
)
btnexamples4 = InlineKeyboardButton(
    text="Про видачу копії вироку суду",
    url="https://telegra.ph/Zrazok-zayavi-vidati-kop%D1%96yu-viroku-sudu-11-19",
)
btnexamples5 = InlineKeyboardButton(
    text="Про дозвід на побачення",
    url="https://telegra.ph/Zrazok-zayavi-pro-dozv%D1%96l-na-pobachennya-11-19",
)
btnexamples6 = InlineKeyboardButton(
    text="Про отримання повістки SMS-повідомлення",
    url="https://telegra.ph/Zayavka-pro-otrimannya"
    "-sudovoi-pov%D1%96stki-v-elektronn%D1%96j-form%D1%96-za-dopomogoyu-SMS-pov%D1%96domlennya-11-19",
)
btnfeedback = InlineKeyboardButton(
    text="Електронна форма звернення громадян",
    url="https://pr.zk.court.gov.ua/sud0708/feedback/",
)
btnforma = InlineKeyboardButton(
    text="ЗАПИТ на отримання публічної інформації",
    url="https://pr.zk.court.gov.ua/sud0708/forma/",
)
markupexample.insert(btnexamples)
markupexample.insert(btnexamples1)
markupexample.insert(btnexamples2)
markupexample.insert(btnexamples3)
markupexample.insert(btnexamples4)
markupexample.insert(btnexamples5)
markupexample.insert(btnexamples6)
markupexample.insert(btnfeedback)
markupexample.insert(btnforma)


# конопки на Оголошення про виклик
markupnews = InlineKeyboardMarkup(row_width=1)
btnnuditynews = InlineKeyboardButton(
    text="Переміститися в Оголошення",
    url="https://pr.zk.court.gov.ua/sud0708/gromadyanam//",
)
markupnews.insert(btnnuditynews)


markuphome = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text="Розклад засідань",
        url="https://pr.zk.court.gov.ua/sud0708/gromadyanam/csz/",
    ),
    InlineKeyboardButton("🔙Назат", callback_data="menusearch"),
)


markup_zka = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text="Розклад засідань",
        url="https://zka.court.gov.ua/sud4806/gromadyanam/csz/",
    ),
    InlineKeyboardButton("🔙Назат", callback_data="menuzka"),
)


markup_ug = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text="Розклад засідань",
        url="https://ug.zk.court.gov.ua/sud0712/gromadyanam/csz/",
    ),
    InlineKeyboardButton("🔙Назат", callback_data="menuug"),
)


# розділ Контаки
markup16 = InlineKeyboardMarkup(row_width=1)
btnnuditynews3 = InlineKeyboardButton(
    text="Загрузити з Апп Стор",
    url="https://apps.apple.com/ua/app/%D1%94%D1%81%D1%83%D0%B4/id1578245779?l=uk",
)
btnnuditynews4 = InlineKeyboardButton(
    text="Загрузити з Гугл Плей",
    url="https://play.google.com/store/apps/details?id=com.floor12apps.ecourt&gl=UA",
)
markup16.insert(btnnuditynews4)
markup16.insert(btnnuditynews3)


butmobileapplication = KeyboardButton("📲Завантажити офіційний мобільний додаток єСуд")
markupmobileapp = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(butmobileapplication).add(btnMain)
)


# кнопки пошуку в бз по номеру та по ымены
but_searchname = KeyboardButton("🎫Пошук за прізвищем та ім’ям")
but_casenumber = KeyboardButton("🔖Пошук за номером справи")
but_waiting_date_db = KeyboardButton("🗓️Пошук за датою")
markupsearch = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .row(but_searchname, but_casenumber)
    .row(but_waiting_date_db)
    .add(btnMain)
)


# реєстрація в базі данних
but_cancel = KeyboardButton("/відмова")
markupregistr = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    but_cancel
)


but_stop = KeyboardButton("/стоп")
markupstop = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    but_stop
)


but_pass = KeyboardButton("/пропустити")
markuppass = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    but_pass
)


but_list = KeyboardButton("📑Список заяв")
markuplist1 = ReplyKeyboardMarkup(resize_keyboard=True).row(but_list).add(btnMain)


but_geoss = KeyboardButton("🗺Карти проїзду")
markupkartu = ReplyKeyboardMarkup(resize_keyboard=True).row(but_geoss).add(btnMain)


but_searchname_zka = KeyboardButton("🎫Пошук за прізвищем та ім’ям zka")
but_casenumber_zka = KeyboardButton("🔖Пошук за номером справи zka")
btnName_zka = KeyboardButton("📩Push сповіщення zka")
markupsearch_zka = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(but_searchname_zka, but_casenumber_zka)
    .row(btnName_zka)
    .add(btnMain)
)


but_cancel_zka = KeyboardButton("/відмовляюся")
markupregistr_zka = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(but_cancel_zka)


mainbutton = InlineKeyboardButton("🔙Назат", callback_data="v0")
button1 = InlineKeyboardButton("Push сповіщення", callback_data="v1")
button2 = InlineKeyboardButton("Зникли кнопки", callback_data="v2")
button3 = InlineKeyboardButton("Текст з гіперпосиланням", callback_data="v3")
button4 = InlineKeyboardButton("Пошук за прізвищем", callback_data="v4")
button5 = InlineKeyboardButton("Озвучка тексту", callback_data="v5")
button6 = InlineKeyboardButton("Відключити плеєр", callback_data="v6")
button7 = InlineKeyboardButton("Одиночне відтворення плеєра", callback_data="v7")
button8 = InlineKeyboardButton("Скопіювати текстове повідомлення", callback_data="v8")
button9 = InlineKeyboardButton("Поширити файл", callback_data="v9")
inline_button = (
    InlineKeyboardMarkup()
    .add(button1, button2)
    .add(button3)
    .add(button4, button5)
    .add(button6, button9)
    .add(button7)
    .add(button8)
    .add(mainbutton)
)


butj1 = InlineKeyboardButton("Гевці В.М.", callback_data="гевці")
butj2 = InlineKeyboardButton("Чепурнов В.О.", callback_data="чепурнов")
butj3 = InlineKeyboardButton("Ганько І.І.", callback_data="ганько")
butj4 = InlineKeyboardButton("Вибрати всіх", callback_data="all")
inline_butj = InlineKeyboardMarkup().add(butj3).add(butj2).add(butj1).add(butj4)


butforma1 = InlineKeyboardButton(
    "Адміністративні правопорушення", callback_data="адмін"
)
butforma2 = InlineKeyboardButton("Цивільне судочинство", callback_data="цивіл")
butforma3 = InlineKeyboardButton("Кримінальне судочинство", callback_data="крим")
butforma4 = InlineKeyboardButton("Вибрати всі", callback_data="всі")
inline_butforma = (
    InlineKeyboardMarkup().add(butforma1).add(butforma2).add(butforma3).add(butforma4)
)

butforma1 = InlineKeyboardButton(
    "Адміністративні правопорушення", callback_data="адмін2"
)
butforma2 = InlineKeyboardButton("Цивільне судочинство", callback_data="цивіл2")
butforma3 = InlineKeyboardButton("Кримінальне судочинство", callback_data="крим2")
butforma4 = InlineKeyboardButton("Вибрати всі", callback_data="всі2")
inline_butforma2 = (
    InlineKeyboardMarkup().add(butforma1).add(butforma2).add(butforma3).add(butforma4)
)

but_searchname_ug = KeyboardButton("🎫Пошук за прізвищем та ім’ям ug")
but_casenumber_ug = KeyboardButton("🔖Пошук за номером справи ug")
but_waiting_ug = KeyboardButton("🗓️Пошук за датою ug")
btnName_ug = KeyboardButton("📩Push сповіщення ug")
markupsearch_ug = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(but_searchname_ug, but_casenumber_ug)
    .row(but_waiting_ug, btnName_ug)
    .add(btnMain)
)

but_cancel_ug = KeyboardButton("/відмовляюся.")
markupregistr_ug = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(but_cancel_ug)


but_passug = KeyboardButton("/пропустити.")
markuppasug = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    but_passug
)

butj1 = InlineKeyboardButton("Дергачова Н.В.", callback_data="дергачова")
butj2 = InlineKeyboardButton("Дегтяренко К.С.", callback_data="дегтяренко")
butj3 = InlineKeyboardButton("Деметрадзе Т.Р.", callback_data="деметрадзе")
butj4 = InlineKeyboardButton("Данко В.Й.", callback_data="данко")
butj5 = InlineKeyboardButton("Логойда І.В.", callback_data="логойда")
butj6 = InlineKeyboardButton("Лемак О.В.", callback_data="лемак")
butj7 = InlineKeyboardButton("Голяна О.В.", callback_data="голяна")
butj8 = InlineKeyboardButton("Придачук О.А.", callback_data="придачук")
butj9 = InlineKeyboardButton("Сарай А.І.", callback_data="сарай")
butj10 = InlineKeyboardButton("Малюк В.М.", callback_data="малюк")
butj11 = InlineKeyboardButton("Бедьо В.І.", callback_data="бедьо")
butj12 = InlineKeyboardButton("Бенца К.К.", callback_data="бенца")
butj13 = InlineKeyboardButton("Фазикош О.В.", callback_data="фазикош")
butj14 = InlineKeyboardButton("Шумило Н.Б.", callback_data="шумило")
butj15 = InlineKeyboardButton("Шепетко І.О.", callback_data="шепетко")
butj16 = InlineKeyboardButton("Іванов А.П.", callback_data="іванов")
butj17 = InlineKeyboardButton("Зарева Н.І.", callback_data="зарева")
butj18 = InlineKeyboardButton("Крегул М.М.", callback_data="крегул")
butj19 = InlineKeyboardButton("Хамник М.М.", callback_data="хамник")
butj20 = InlineKeyboardButton("Вибрати всіх", callback_data="all")
inline_butjua = InlineKeyboardMarkup().add(butj1,butj2).add(butj4,butj5,butj6).add(butj7,butj19,butj9)\
    .add(butj10,butj11,butj12).add(butj13,butj14,butj15).add(butj16,butj17,butj18).add(butj8,butj3).add(butj20)
