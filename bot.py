import telebot
import buttons as bt
import database as db
from geopy.geocoders import Nominatim

bot = telebot.TeleBot("7074864531:AAEyfbkKzGfbViiK7p9gKQoI5_Bc3-rlCh0")
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/123.0.0.0 Safari/537.36")


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Здраствуйте!\n"
                              "Пройдите короткую регистрацию\n\n"
                              "Введите своё имя:")
    print(message.text)
    bot.register_next_step_handler(message, get_name)


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
        bot.send_message(user_id, f"Ваш адрес: {address}\n"
                                  "Регистрация завершена\n"
                                  f"Добро пожаловать {name}")
        db.register_user(user_id=user_id, user_name=name, phone_number=phone_number)
        print(address)
        print(message.location)
    else:
        bot.send_message(user_id, "Отправьте кнопкой")
        bot.register_next_step_handler(message, get_location)


bot.infinity_polling()
