import telebot
import pyowm
import constants

bot = telebot.TeleBot(constants.token)
bot.send_message(422243813, "123")
last_weather = False


def get_weather(city):
    try:
        weather = pyowm.OWM("608b9e48a283cfb2c1fe98c0b67c73ba").weather_at_place(
            city).get_weather()
        return ("In " + city + " weather is " + str(weather.get_status()) +
                ", the temperature is " +
                str(weather.get_temperature("celsius")["temp"]) + " сelsius.")
    except pyowm.exceptions.not_found_error.NotFoundError as error:
        raise error


@bot.message_handler(commands=['help'])
def handle_help(msg):
    bot.send_message(msg.chat.id, constants.help_msg)


@bot.message_handler(commands=['weather'])
def handle_weather(msg):
    global last_weather
    bot.send_message(msg.chat.id, constants.weather_msg)
    last_weather = True


@bot.message_handler(content_types=['text'])
def handle_text(msg):
    global last_weather
    if last_weather:
        while True:
            try:
                weather = get_weather(msg.text)
                bot.send_message(msg.chat.id, weather)
                break
            except:
                bot.send_message(msg.chat.id, constants.bad_city_msg)
        last_weather = False
    else:
        bot.send_message(msg.chat.id, constants.std_msg)


bot.polling(none_stop=True, interval=0)
