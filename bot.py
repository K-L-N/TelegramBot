import telebot
import pyowm
import json
import logging

logging.basicConfig(
    format="[%(asctime)s](%(module)s)%(levelname)s: %(message)s",
    level=logging.INFO
)
with open('constants.json') as file:
    constants = json.load(file)
    logging.info("Json file with constants loaded")
bot = telebot.TeleBot(constants["bot_token"])
last_weather = False


def get_weather(city):
    global constants
    try:
        weather = pyowm.OWM(constants["owm_token"]).weather_at_place(
            city).get_weather()
        return ("In " + city + " weather is " + str(weather.get_status()) +
                ", the temperature is " +
                str(weather.get_temperature("celsius")["temp"]) + " сelsius.")
    except pyowm.exceptions.not_found_error.NotFoundError as error:
        raise error


@bot.message_handler(commands=['help'])
def handle_help(msg):
    logging.info("Get \"help\" command from chat: {}".format(msg.chat.id))
    bot.send_message(msg.chat.id, constants["help_msg"])
    logging.info("Send help message to chat: {}".format(msg.chat.id))


@bot.message_handler(commands=['weather'])
def handle_weather(msg):
    global last_weather
    logging.info("Get \"weather\" command from chat: {}".format(msg.chat.id))
    bot.send_message(msg.chat.id, constants["weather_msg"])
    logging.info("Send weather message to chat: {}".format(msg.chat.id))
    last_weather = True


@bot.message_handler(content_types=['text'])
def handle_text(msg):
    global last_weather
    logging.info("Get message from chat: {}".format(msg.chat.id))
    if last_weather:
        while True:
            try:
                weather = get_weather(msg.text)
                bot.send_message(msg.chat.id, weather)
                logging.info(
                    "Send message with weather in city to chat: {}".format(
                        msg.chat.id)
                )
                break
            except pyowm.exceptions.not_found_error.NotFoundError:
                bot.send_message(msg.chat.id, constants["bad_city_msg"])
                logging.warning(
                    "Get bad name of city from chat: {}".format(msg.chat.id)
                )
        last_weather = False
    else:
        bot.send_message(msg.chat.id, constants["std_msg"])
        logging.info("Send standart message to chat: {}".format(msg.chat.id))


bot.polling(none_stop=True, interval=0)
