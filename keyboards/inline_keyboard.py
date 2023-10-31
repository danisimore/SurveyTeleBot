from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)


class ServeyKeyboardGenerator:
    def __init__(self) -> None:
        """Инициализируем объекты клавиатуры в кнопки в виде атрибутов класса"""
        inline_markup = InlineKeyboardMarkup()
        inline_markup.row_width = 4

        self.inline_markup = inline_markup
        self.inline_markup_button = InlineKeyboardButton

        self.reply_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.reply_markup_button = KeyboardButton

    def gen_inline_markup(
        self, buttons: list, callback_data: list
    ) -> InlineKeyboardMarkup:
        """Функция добавляет кнопки к клавиатуре на основе переданных аргументов"""
        for button, cb_data in zip(buttons, callback_data):
            self.inline_markup.add(
                self.inline_markup_button(text=button, callback_data=cb_data)
            )

        return self.inline_markup

    def gen_reply_markup(self, buttons: list):
        for button in buttons:
            self.reply_markup.add(self.reply_markup_button(text=button))

        return self.reply_markup

    @staticmethod
    def drop_reply_markup():
        return ReplyKeyboardRemove()
