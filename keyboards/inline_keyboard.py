from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class ServeyInlineMarkupGen:
    def __init__(self) -> None:
        """Инициализируем объекты клавиатуры в кнопки в виде атрибутов класса"""
        markup = InlineKeyboardMarkup()
        markup.row_width = 4

        self.markup = markup
        self.keyboard_button = InlineKeyboardButton

    def gen_keyboard(self, buttons: list, callback_data: list) -> InlineKeyboardMarkup:
        """Функция добавляет кнопки к клавиатуре на основе переданных аргументов"""
        for button, cb_data in zip(buttons, callback_data):
            self.markup.add(self.keyboard_button(text=button, callback_data=cb_data))

        return self.markup
