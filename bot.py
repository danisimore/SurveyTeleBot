import os

import dotenv
import telebot

from telebot.types import CallbackQuery, Message

from keyboards.inline_keyboard import ServeyInlineMarkupGen

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
    keyboard_generator = ServeyInlineMarkupGen()

    buttons = ["Да", "Нет"]

    # Если гражданин РФ, узнаем о том, живет ли Москве.
    if callback.data == "cb_rf_citizen":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Отлично! Являешься ли ты жителем Москвы?",
            reply_markup=keyboard_generator.gen_keyboard(
                buttons=buttons,
                callback_data=["cb_live_in_moscow", "cb_doesnt_live_in_moscow"]
            )
        )
    # Независимо от того живет ли гражданин в Москве, узнаем студент ли он.
    elif callback.data == "cb_live_in_moscow" or callback.data == "cb_doesnt_live_in_moscow":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Вы студент?",
            reply_markup=keyboard_generator.gen_keyboard(
                buttons=buttons,
                callback_data=["cb_student", "cb_not_student"],
            )
        )
    # Если не студент, то узнаем о его желании учиться в Москве.
    elif callback.data == "cb_not_student":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Хотели бы учиться в Москве?",
            reply_markup=keyboard_generator.gen_keyboard(
                buttons=buttons,
                callback_data=["cb_wanna_study_in_moscow", "cb_doesnt_wanna_study_in_moscow"],
            )
        )

    # Если не гражданин РФ, то узнаем о желании быть гражданином РФ.
    elif callback.data == "cb_not_rf_citizen":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Хотели бы вы стать гражданином РФ?",
            reply_markup=keyboard_generator.gen_keyboard(
                buttons=buttons,
                callback_data=["cb_wanna_live_in_russia", "cb_doesnt_wanna_live_in_russia"]
            )
        )

    # Если хочет быть гражданином РФ, то узнаем о желании учиться в Москве.
    elif callback.data == "cb_wanna_live_in_russia":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Переехав в Россию, вы бы хотели получить образование в одном и ВУЗов Москвы?",
            reply_markup=keyboard_generator.gen_keyboard(
                buttons=buttons,
                callback_data=["cb_wanna_study_in_moscow", "cb_doesnt_wanna_study_in_moscow"]
            )
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
