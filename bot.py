import os

import dotenv
import telebot

from telebot.types import CallbackQuery, Message

from keyboards.inline_keyboard import ServeyKeyboardGenerator

from handlers.callback_data_handler import callback_data_handler

from services.write_data import write_json
from services.delete_user_results_data import delete_data
from services.load_survey_users_data import load_data


dotenv.load_dotenv(".env", override=True)

API_TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(API_TOKEN)


survey_users_data = {}

# try:
#     with open("data/survey_users_data.json", encoding="utf-8") as data_file:
#         survey_users_data = json.load(data_file)
# except FileNotFoundError:
#     print("LOGS | Data file doesn't exist. Dont worry! This is not a problem.")
#     survey_users_data = {}


@bot.message_handler(content_types=["text"])
def test_f(message: Message):
    keyboard_generator = ServeyKeyboardGenerator()
    if message.text == "/start":
        start_command_handler(message)
    elif message.text == "Пройти опрос снова":
        delete_data(message.chat.username)
        bot.send_message(
            chat_id=message.chat.id,
            text="Хорошо, можете приступать.",
            reply_markup=keyboard_generator.drop_reply_markup(),
        )
        start_command_handler(message)


@bot.message_handler(commands=["start"])
def start_command_handler(message: Message) -> None:
    global survey_users_data

    keyboard_generator = ServeyKeyboardGenerator()
    survey_users_data = load_data()

    if message.chat.username in survey_users_data:
        bot.send_message(
            chat_id=message.chat.id,
            text="Кажется ты уже проходил опрос...",
        )
        return

    buttons = ["Да", "Нет"]
    callback_data = ["cb_rf_citizen", "cb_not_rf_citizen"]

    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Ты являешься гражданином РФ?",
        reply_markup=keyboard_generator.gen_inline_markup(
            buttons=buttons,
            callback_data=callback_data,
        ),
    )
    survey_users_data[message.chat.username] = {}


@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback: CallbackQuery) -> None:
    keyboard_generator = ServeyKeyboardGenerator()

    buttons = ["Да", "Нет"]

    username = callback.from_user.username

    if "dead_end" in survey_users_data[username]:
        return

    # Если гражданин РФ, узнаем о том, живет ли Москве.
    if callback.data == "cb_rf_citizen":
        survey_users_data[username]["Ветка"] = "Гражданин РФ"
        callback_data_handler(
            text="Отлично! Являешься ли ты жителем Москвы?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_live_in_moscow", "cb_doesnt_live_in_moscow"],
            bot=bot,
        )

    # Независимо от того живет ли гражданин в Москве, узнаем студент ли он.
    elif (
        callback.data == "cb_live_in_moscow"
        or callback.data == "cb_doesnt_live_in_moscow"
    ):
        if callback.data == "cb_live_in_moscow":
            survey_users_data[username]["Житель Москвы?"] = True
        else:
            survey_users_data[username]["Житель Москвы?"] = False

        callback_data_handler(
            text="Вы студент?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_student", "cb_not_student"],
            bot=bot,
        )

    # Если не студент, то узнаем о его желании учиться в Москве.
    elif callback.data == "cb_not_student":
        survey_users_data[username]["Студент?"] = False

        callback_data_handler(
            text="Хотели бы учиться в Москве?",
            buttons=buttons,
            callback=callback,
            callback_data=[
                "cb_wanna_study_in_moscow",
                "cb_doesnt_wanna_study_in_moscow",
            ],
            bot=bot,
        )

    # Если не гражданин РФ, то узнаем о желании быть гражданином РФ.
    elif callback.data == "cb_not_rf_citizen":
        survey_users_data[username]["Ветка"] = "Не гражданин РФ"

        callback_data_handler(
            text="Хотели бы вы стать гражданином РФ?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_wanna_live_in_russia", "cb_doesnt_wanna_live_in_russia"],
            bot=bot,
        )

    # Независимо от того хочет ли быть гражданином РФ, узнаем о желании учиться в Москве.
    elif (
        callback.data == "cb_wanna_live_in_russia"
        or callback.data == "cb_doesnt_wanna_live_in_russia"
    ):
        if callback.data == "cb_wanna_live_in_russia":
            survey_users_data[username]["Хочет ли стать гражданином РФ"] = True
        else:
            survey_users_data[username]["Хочет ли стать гражданином РФ"] = False

        callback_data_handler(
            text="Переехав в Россию, вы бы хотели получить образование в одном и ВУЗов Москвы?",
            buttons=buttons,
            callback=callback,
            callback_data=[
                "cb_wanna_study_in_moscow",
                "cb_doesnt_wanna_study_in_moscow",
            ],
            bot=bot,
        )

    # Завершаем опрос в этих точках.
    elif (
        callback.data == "cb_student"
        or callback.data == "cb_wanna_study_in_moscow"
        or callback.data == "cb_doesnt_wanna_study_in_moscow"
    ):
        if callback.data == "cb_doesnt_wanna_live_in_russia":
            survey_users_data[username]["Хочет ли стать гражданином РФ"] = False
        elif callback.data == "cb_student":
            survey_users_data[username]["Студент?"] = True
            survey_users_data[username]["Хотел бы учиться в Москве?"] = None
        elif callback.data == "cb_wanna_study_in_moscow":
            survey_users_data[username]["Хотел бы учиться в Москве?"] = True
        else:
            survey_users_data[username]["Хотел бы учиться в Москве?"] = False

        # Нужно, чтобы handler больше не обрабатывал нажатие кнопок после прохождения опроса
        survey_users_data[username]["dead_end"] = True

        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Спасибо за участие в опросе!",
            reply_markup=keyboard_generator.gen_reply_markup(
                buttons=["Пройти опрос снова"],
            ),
        )

        write_json(user_data=survey_users_data, username=username)


bot.infinity_polling()
