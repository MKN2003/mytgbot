import telebot
import buttons as bt
import database as db
from geopy.geocoders import Nominatim

bot = telebot.TeleBot("7074864531:AAEyfbkKzGfbViiK7p9gKQoI5_Bc3-rlCh0")
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/123.0.0.0 Safari/537.36")

#db.add_product(pr_name="Капсула", pr_price=20000.00, pr_des="18.9L", pr_photo="https://en.hydrolife.uz/d/gallon.jpg")
#db.add_product(pr_name="Боклажка", pr_price=10000.00, pr_des="10L", pr_photo="https://orzon.uz/upload/iblock/3a0/3a09472d9f06ee46cdbe18dbc2ba572e.jpg")

users = {}
user_products = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    user_name = message.from_user.first_name
    checker = db.check_user(user_id)

    if checker == False:
        bot.send_message(user_id, f"Assalomu alaykum {user_name}. Men Hydrolife yetkazib berish xizmati botiman!\n"
                                  f"Привет {user_name}! Я бот службы доставки Hydrolife!")
        bot.send_message(user_id, "Muloqot tilini tanlang\n"
                                  "Выберите язык\n", reply_markup=bt.language_bt())
        bot.register_next_step_handler(message, register)
    elif checker == True:
        actual_products = db.get_pr_id()
        bot.send_message(user_id, "Выберите один из продуктов", reply_markup=bt.product_menu(actual_products))


def register(message):
    user_id = message.from_user.id
    if message.text == "Русский":
        bot.send_message(user_id,"Пройдите короткую регистрацию\n"
                                 "Напишите свое имя")
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Узбекский":
        pass


def get_name(message):
    user_id = message.from_user.id
    name = message.text

    bot.send_message(user_id, "Поделитесь контактнами данными", reply_markup=bt.phone_bt())
    bot.register_next_step_handler(message, get_phone_number, name)

    print(message.text)


def get_phone_number(message, name):
    user_id = message.from_user.id

    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, "Поделитесь геолокацией", reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, phone_number)
    else:
        bot.send_message(user_id, "Отправьте свои контакты через конпку")
        bot.register_next_step_handler(message, get_phone_number, name)


def get_location(message, name, phone_number):
    user_id = message.from_user.id

    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        address = geolocator.reverse((latitude, longitude))

        actual_products = db.get_pr_id()

        bot.send_message(user_id, f"Ваш адрес: {address}\n"
                                  "Регистрация завершена\n\n"
                                  f"Добро пожаловать {name}")
        bot.send_message(user_id, "Выберите один из продуктов", reply_markup=bt.product_menu(actual_products))

        db.register_user(user_id=user_id, user_name=name, phone_number=phone_number)
    else:
        bot.send_message(user_id, "Отправьте кнопкой")
        bot.register_next_step_handler(message, get_location)


@bot.callback_query_handler(lambda call: call.data in ["cart", "back", "plus", "minus", "none",
                                                       "main_menu", "to_cart", "clear_cart", "order"])
def for_call(call):
    user_id = call.message.chat.id

    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Отправьте геолокацию или выберите адрес", reply_markup=bt.location_bt())

        bot.register_next_step_handler(call.message, get_location)
    elif call.data == "cart":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        user_id = call.message.chat.id

        user_cart =db.get_user_cart(user_id)

        full_text = (f"Ваша корзина\n\n")
        total_amount = 0

        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\nОбщая сумма:{total_amount}"

        cart = db.get_cart_id_name(user_id)
        pr_name = []

        for i in cart:
            pr_name.append(i[1])
        user_products[user_id] = pr_name

        bot.send_message(user_id, full_text, reply_markup=bt.get_user_cart_kb(cart))
    elif call.data == "to_cart":
        user_id = call.message.chat.id
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"],
                       users[user_id]["pr_count"], users[user_id]["pr_price"])
        users.pop(user_id)

        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, "Продук добавлен в корзину")
    elif call.data == "clear_cart":
        db.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваша корзина очищена")

        actual_products = db.get_pr_id()
        bot.send_message(user_id, "Выберите один из продуктов", reply_markup=bt.product_menu(actual_products))
    elif call.data == "main_menu":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)

        actual_products = db.get_pr_id()
        bot.send_message(user_id, "Выберите один из продуктов", reply_markup=bt.product_menu(actual_products))

    elif call.data == "plus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1

        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product(current_amount, plus_minus="plus"))
    elif call.data == "minus":
        current_amount = users[user_id]["pr_count"]

        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                          reply_markup=bt.exact_product(current_amount, plus_minus="minus"))
        else:
            pass
    elif call.data == "order":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Новый заказа от пользователя {user_id}\n"

        total_amount = 0

        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\nИтоговая сумма: {total_amount}"

        bot.send_message(-4133559500, full_text)
        bot.send_message(user_id, "Ваш заказ оформлен")

        db.delete_user_cart(user_id)
        user_products.pop(user_id)

    elif call.data == "none":
        pass
    else:
        pass

@bot.callback_query_handler(lambda call: call.message.chat.id in user_products.keys() and call.data in user_products.get(call.message.chat.id))
def call_for_delete(call):
    user_id = call.message.chat.id
    db.delete_exact_pr_from_cart(user_id, call.data)

    user_products[user_id].remove(str(call.data))
    user_cart = db.get_user_cart(user_id)

    full_text = (f"Ваша корзина\n\n")
    total_amount = 0

    for i in user_cart:
        full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
        total_amount += i[2]
    full_text += f"\nОбщая сумма:{total_amount}"
    cart = db.get_cart_id_name(user_id)

    bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=full_text, reply_markup=bt.get_user_cart_kb(cart))


@bot.callback_query_handler(lambda call: int(call.data) in db.get_all_id())
def for_products(call):
    user_id = call.message.chat.id
    product = db.get_product(int(call.data))

    users[user_id] = {"pr_id": call.data, "pr_name": product[0], "pr_count": 1, "pr_price": product[1]}
    bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                                                      f"Описание: {product[2]}\n"
                                                      f"Цена: {product[1]}\n"
                                                      f"Выберите количество: ", reply_markup=bt.exact_product())


bot.infinity_polling()
