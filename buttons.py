from telebot import types


def phone_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone = types.KeyboardButton("Поделиться контактами", request_contact=True)
    kb.add(phone)
    return kb


def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    location = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(location)

    return kb


def language_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    ru = types.KeyboardButton("Русский")
    eng = types.KeyboardButton("Узбекский")

    kb.add(ru, eng)

    return kb


def product_menu(actual_products):
    kb = types.InlineKeyboardMarkup(row_width=2)

    back = types.InlineKeyboardButton(text="⬅️Назад", callback_data="back")
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    products = [types.InlineKeyboardButton(text=i[1], callback_data=i[0]) for i in actual_products]

    kb.row(*products)
    kb.row(cart)
    kb.row(back)

    return kb