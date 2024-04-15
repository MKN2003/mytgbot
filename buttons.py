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


def exact_product(current_amount=1, plus_minus=""):
    kb = types.InlineKeyboardMarkup(row_width=3)

    back = types.InlineKeyboardButton(text="⬅️Назад", callback_data="main_menu")
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="to_cart")

    amount = types.InlineKeyboardButton(text=f"{current_amount}", callback_data="none")
    plus = types.InlineKeyboardButton(text="+", callback_data="plus")
    minus = types.InlineKeyboardButton(text="-", callback_data="minus")

    if plus_minus == "plus":
        new_amount = current_amount + 1
        amount = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")
    elif plus_minus == "minus":
        if current_amount > 1:
            new_amount = current_amount - 1
            amount = types.InlineKeyboardButton(text=f"{new_amount}", callback_data="none")

    kb.add(plus, amount, minus)
    kb.row(back)
    kb.row(cart)

    return kb


def get_user_cart_kb(cart):
    kb = types.InlineKeyboardMarkup(row_width=1)

    back = types.InlineKeyboardButton(text="⬅️Назад", callback_data="main_menu")
    order = types.InlineKeyboardButton(text="Оформить заказа", callback_data="order")
    clear = types.InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")

    product = [types.InlineKeyboardButton(text=f"❌ {i[1]}", callback_data=f"{i[1]}") for i in cart]

    kb.add(clear, order, back)
    kb.add(*product)

    return kb


