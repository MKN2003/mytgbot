import telebot
import buttons as bt
import database as db
from geopy.geocoders import Nominatim

bot = telebot.TeleBot("7074864531:AAEyfbkKzGfbViiK7p9gKQoI5_Bc3-rlCh0")
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/123.0.0.0 Safari/537.36")

# db.add_product(pr_name="Капсула", pr_price=20000.00, pr_des="18.9L", pr_photo="https://en.hydrolife.uz/d/gallon.jpg")
# db.add_product(pr_name="Боклажка", pr_price=10000.00, pr_des="10L", pr_photo="https://orzon.uz/upload/iblock/3a0/3a09472d9f06ee46cdbe18dbc2ba572e.jpg")


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


@bot.callback_query_handler(lambda call: call.data in ["cart", "back"])
def for_call(call):
    user_id = call.message.chat.id

    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Отправьте геолокацию или выберите адрес", reply_markup=bt.location_bt())

        bot.register_next_step_handler(call.message, get_location)
    elif call.data == "cart":
        pass
    else:
        pass


bot.infinity_polling()
