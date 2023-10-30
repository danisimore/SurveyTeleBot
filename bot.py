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
    callback_data = ["cb_cis_citizen", "cb_not_cis_citizen"]

    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Ты являешься гражданином СНГ?",
        reply_markup=keyboard_generator.gen_keyboard(buttons=buttons, callback_data=callback_data)
    )


@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback: CallbackQuery) -> None:
    keyboard_generator = ServeyInlineMarkupGen()

    buttons = ["Да", "Нет"]
    is_live_in_moscow_callback_data = ["cb_live_in_moscow", "cb_doesnt_live_in_moscow"]
    wanna_live_in_russia = ["cb_wanna_live_in_russia", "cb_doesnt_wanna_live_in_russia"]

    # Если гражданин СНГ
    if callback.data == "cb_cis_citizen":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Отлично! Являешься ли ты жителем Москвы?",
            reply_markup=keyboard_generator.gen_keyboard(buttons=buttons, callback_data=is_live_in_moscow_callback_data)
        )
    # Если не гражданин СНГ
    elif callback.data == "cb_not_cis_citizen":
        bot.send_message(
            callback.json["message"]["chat"]["id"],
            text="Хотели бы вы стать гражданином РФ?",
            reply_markup=keyboard_generator.gen_keyboard(buttons=buttons, callback_data=wanna_live_in_russia)
        )


bot.infinity_polling()
