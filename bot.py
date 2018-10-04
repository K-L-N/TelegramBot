from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
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
bot = Bot(token=constants["bot_token"])
dp = Dispatcher(bot)
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


@dp.message_handler(commands=['help'])
async def handle_help(msg: types.Message):
    logging.info("Get \"help\" command from user: {}".format(msg.from_user.id))
    await bot.send_message(msg.from_user.id, constants["help_msg"])
    logging.info("Send help message to user: {}".format(msg.from_user.id))


@dp.message_handler(commands=['weather'])
async def handle_weather(msg: types.Message):
    global last_weather
    logging.info(
        "Get \"weather\" command from user: {}".format(msg.from_user.id))
    await bot.send_message(msg.from_user.id, constants["weather_msg"])
    logging.info("Send weather message to user: {}".format(msg.from_user.id))
    last_weather = True


@dp.message_handler()
async def handle_text(msg: types.Message):
    global last_weather
    logging.info("Get message from user: {}".format(msg.from_user.id))
    if last_weather:
        try:
            weather = get_weather(msg.text)
            await bot.send_message(msg.from_user.id, weather)
            logging.info(
                "Send message with weather in city to user: {}".format(
                    msg.from_user.id)
            )
            last_weather = False
        except pyowm.exceptions.not_found_error.NotFoundError:
            await bot.send_message(msg.from_user.id, constants["bad_city_msg"])
            logging.warning(
                "Get bad name of city from user: {}".format(
                    msg.from_user.id)
            )
    else:
        await bot.send_message(msg.from_user.id, constants["std_msg"])
        logging.info(
            "Send standart message to user: {}".format(msg.from_user.id))


if __name__ == '__main__':
    executor.start_polling(dp)
