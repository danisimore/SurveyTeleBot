from keyboards.inline_keyboard import ServeyKeyboardGenerator


def callback_data_handler(text, buttons, callback, callback_data, bot):
    """
    :param text: The text that will above the inline keyboard
    :param buttons: The buttons that will be offered to the user
    :param callback: The Callback object formed based on the user's last click on the inline button
    :param callback_data: The callback data that will be transmitted when the user clicks the inline button
    :param bot: Bot object
    :return:
    """

    keyboard_generator = ServeyKeyboardGenerator()

    bot.send_message(
        callback.json["message"]["chat"]["id"],
        text=text,
        reply_markup=keyboard_generator.gen_inline_markup(
            buttons=buttons, callback_data=callback_data
        ),
    )
