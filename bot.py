import os

import dotenv
import telebot

from telebot.types import CallbackQuery, Message

from keyboards.inline_keyboard import ServeyInlineMarkupGen

from handlers.callback_data_handler import callback_data_handler


dotenv.load_dotenv(".env", override=True)

API_TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start_command_handler(message: Message) -> None:
    keyboard_generator = ServeyInlineMarkupGen()

    buttons = ["Да", "Нет"]
    callback_data = ["cb_rf_citizen", "cb_not_rf_citizen"]

    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Ты являешься гражданином РФ?",
        reply_markup=keyboard_generator.gen_keyboard(buttons=buttons, callback_data=callback_data)
    )


@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback: CallbackQuery) -> None:
    buttons = ["Да", "Нет"]

    # Если гражданин РФ, узнаем о том, живет ли Москве.
    if callback.data == "cb_rf_citizen":
        callback_data_handler(
            text="Отлично! Являешься ли ты жителем Москвы?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_live_in_moscow", "cb_doesnt_live_in_moscow"],
            bot=bot
        )

    # Независимо от того живет ли гражданин в Москве, узнаем студент ли он.
    elif callback.data == "cb_live_in_moscow" or callback.data == "cb_doesnt_live_in_moscow":
        callback_data_handler(
            text="Вы студент?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_student", "cb_not_student"],
            bot=bot
        )

    # Если не студент, то узнаем о его желании учиться в Москве.
    elif callback.data == "cb_not_student":
        callback_data_handler(
            text="Хотели бы учиться в Москве?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_wanna_study_in_moscow", "cb_doesnt_wanna_study_in_moscow"],
            bot=bot
        )

    # Если не гражданин РФ, то узнаем о желании быть гражданином РФ.
    elif callback.data == "cb_not_rf_citizen":
        callback_data_handler(
            text="Хотели бы вы стать гражданином РФ?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_wanna_live_in_russia", "cb_doesnt_wanna_live_in_russia"],
            bot=bot
        )

    # Если хочет быть гражданином РФ, то узнаем о желании учиться в Москве.
    elif callback.data == "cb_wanna_live_in_russia":
        callback_data_handler(
            text="Переехав в Россию, вы бы хотели получить образование в одном и ВУЗов Москвы?",
            buttons=buttons,
            callback=callback,
            callback_data=["cb_wanna_study_in_moscow", "cb_doesnt_wanna_study_in_moscow"],
            bot=bot
        )

    # Завершаем опрос в этих точках.
    elif (
            callback.data == "cb_doesnt_wanna_live_in_russia" or
            callback.data == "cb_student" or
            callback.data == "cb_dead_end" or
            callback.data == "cb_wanna_study_in_moscow" or
            callback.data == "cb_doesnt_wanna_study_in_moscow"
    ):
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Спасибо за участие в опросе!",
            )


bot.infinity_polling()
