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
