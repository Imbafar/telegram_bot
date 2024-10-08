import logging
import os
import requests
# import psutil
from datetime import date
# import matplotlib.pyplot as plt

from dotenv import load_dotenv
from telegram import (
    Bot,
    ReplyKeyboardMarkup,
)
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
URL_CAT = "https://api.thecatapi.com/v1/images/search"
URL_DOG = "https://api.thedogapi.com/v1/images/search"
CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
DAYS = 3


def get_date(person):
    year, month, day = [int(x) for x in (os.getenv(person).split(","))]
    return date(year, month, day)


DATE_DORA = get_date("DATE_DORA")
DATE_ALFIR = get_date("DATE_ALFIR")
DATE_KATE = get_date("DATE_KATE")
DATE_ALICE = get_date("DATE_ALICE")
DATE_KOSTA = get_date("DATE_KOSTA")


bot = Bot(token=TELEGRAM_TOKEN)

logging.basicConfig(
    filename="tg_bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - (line : %(lineno)d) - (filename :%(filename)s)",
    level=logging.INFO,
)


def get_new_image(url_animal):
    """Return image of animal."""
    try:
        response = requests.get(url_animal)
        response = response.json()
        random_animal = response[0].get("url")
        return random_animal
    except Exception as error:
        logging.error(f"Ошибка при запросе к API : {error}")


def new_cat(update, context):
    """Send image of cat."""
    chat = update.effective_chat
    try:
        context.bot.send_photo(chat.id, get_new_image(URL_CAT))
    except Exception as error:
        logging.error(f"Ошибка при запросе к API : {error}")
        message = "Что-то поломалось, сообщите разработчику"
        context.bot.send_message(chat.id, text=message)


def new_dog(update, context):
    """Send image of dog."""
    chat = update.effective_chat
    try:
        context.bot.send_photo(chat.id, get_new_image(URL_DOG))
    except Exception as error:
        logging.error(f"Ошибка при запросе к API : {error}")
        message = "Что-то поломалось, сообщите разработчику"
        context.bot.send_message(chat.id, text=message)


def get_date(date_of_birth):
    """Return age in days and days till birthday."""
    date_today = date.today()
    days_person = date_today - date_of_birth

    next_bday_person = date_of_birth.replace(year=date_today.year)
    if next_bday_person < date_today:
        next_bday_person = next_bday_person.replace(year=date_today.year + 1)

    return days_person.days, (next_bday_person - date_today).days


def get_time(update, context):
    """Send deltatime between now and persons birthday."""
    days_dora, next_bday_dora = get_date(DATE_DORA)
    days_alfir, next_bday_alfir = get_date(DATE_ALFIR)
    days_kate, next_bday_kate = get_date(DATE_KATE)
    days_alice, next_bday_alice = get_date(DATE_ALICE)
    days_kosta, next_bday_kosta = get_date(DATE_KOSTA)

    chat = update.effective_chat
    message = f"Нашей Доре {days_dora} дней, ДР через {next_bday_dora} дн.\n"
    message += f"Нашему папе {days_alfir} дней, ДР через {next_bday_alfir} дн.\n"
    message += f"Нашей Кейт {days_kate} дней, ДР через {next_bday_kate} дн.\n"
    message += f"Нашему Косте {days_kosta} дней, ДР через {next_bday_kosta} дн.\n"
    message += f"Нашей Элис {days_alice} дней, ДР через {next_bday_alice} дн."
    context.bot.send_message(chat.id, text=message)


def say_hi(update, context):
    """Send some text as a reply."""
    chat = update.effective_chat
    message = "Привет, я БОТ Альфира!\n"
    message += "Поддерживаемые команды:\n"
    message += "/start - инициализация(не объязательно)\n"
    message += "/new_cat или /new_dog - фото котика/собачки\n"
    message += "/get_time - отчет до ДР\n"
    # message += '/get_weather - погода в Заречном, можно указать "/get_weather x" где x - ваш город\n'
    message += "/get_dollar - курс доллара\n"
    # message += "/get_temperature - температура сервера\n"
    context.bot.send_message(chat_id=chat.id, text=message)


# def get_weather(update, context):
#     """Send weather in Zarechnyy."""
#     chat = update.effective_chat
#     try:
#         if len(context.args) > 0:
#             CITY = context.args[0]
#         else:
#             CITY = "56.811,61.3254"
#     except Exception as error:
#         logging.error(f"Ошибка при запросе к основному API: {error}")
#         message = "Что-то поломалось, сообщите разработчику"
#         context.bot.send_message(chat.id, text=message)
#         return

#     WEATHER_API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={CITY}&days={DAYS}&lang=ru"

#     try:
#         message = "Погода! \n"
#         response = requests.get(WEATHER_API_URL)
#         # plot_temperature_graph(response, CITY)
#         data = response.json()
#         for day in range(DAYS):
#             data_day = data.get("forecast").get("forecastday")[day].get("day")
#             data_date = date.fromisoformat(
#                 data.get("forecast").get("forecastday")[day].get("date")
#             )
#             mintemp_c = data_day.get("mintemp_c")
#             maxtemp_c = data_day.get("maxtemp_c")
#             condition = data_day.get("condition").get("text")
#             avghumidity = data_day.get("avghumidity")
#             message += f"<b>{data_date.strftime('%d/%B/%Y')} </b>\n"
#             message += f"температура мин/макс {mintemp_c}/{maxtemp_c}\n"
#             message += f"влажность {avghumidity}\n"
#             message += f"{condition} \n"
#             message += "\n"
#         context.bot.send_message(chat.id, text=message, parse_mode="HTML")
#         with open("foo.png", "br") as f:
#             context.bot.send_photo(chat.id, f)
#     except Exception as error:
#         logging.error(f"Ошибка при запросе к основному API: {error}")
#         message = "Что-то поломалось, сообщите разработчику"
#         context.bot.send_message(chat.id, text=message)


# def plot_temperature_graph(response, city):
#     """Save img file ploted of weather temperature."""
#     plt.switch_backend("Agg")
#     weather_api_data = {}
#     data = response.json().get("forecast").get("forecastday")
#     for day in data:
#         data_day = day.get("hour")
#         for item in data_day:
#             time = item.get("time")
#             temperature = item.get("temp_c")
#             weather_api_data[time] = temperature

#     days = [datetime.strptime(x, "%Y-%m-%d %H:%M") for x in weather_api_data.keys()]
#     temperatures = [float(x) for x in weather_api_data.values()]

#     plt.figure(figsize=(10, 5))
#     plt.plot(days, temperatures, marker="o", linestyle="-", color="b", linewidth=3)
#     if city == "56.811,61.3254":
#         plt.title("Температура в Заречном")
#     else:
#         plt.title(f"Температура в {city}")
#     plt.xlabel("Дата")
#     plt.ylabel("Температура, °C")
#     plt.grid(True, which="both", linestyle="--", linewidth=0.5)
#     plt.savefig("foo.png")


def get_dollar(update, context):
    """Send dollar to ruble currency."""
    chat = update.effective_chat
    try:
        response = requests.get(CURRENCY_URL)
        usd = response.json().get("Valute").get("USD")
        usd_value = usd.get("Value")
        usd_previous = usd.get("Previous")
        message = "<b>Курс доллара</b>\n"
        message += f"Сегодня {usd_value} руб\n"
        message += f"Вчера {usd_previous} руб"
        context.bot.send_message(chat.id, text=message, parse_mode="HTML")
    except Exception as error:
        logging.error(f"Ошибка при запросе к основному API: {error}")
        message = "Что-то поломалось, сообщите разработчику"
        context.bot.send_message(chat.id, text=message)


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [
            ["/new_cat"],
            ["/new_dog"],
            ["/get_time"],
            # ["/get_weather"],
            ["/get_dollar"],
            # ["/get_temperature"],
        ],
        resize_keyboard=True,
    )

    context.bot.send_message(
        chat_id=chat.id, text=f"Привет, {name}! Держи пятюню!", reply_markup=button
    )


# def get_temperature(update, context):
#     """Send temperature of server."""
#     try:
#         temperature = psutil.sensors_temperatures()
#         acpitz = temperature.get("acpitz")[0][1], temperature.get("acpitz")[1][1]
#         nouveau = temperature.get("nouveau")[0][1]
#         coretemp = (
#             temperature.get("coretemp")[0][1],
#             temperature.get("coretemp")[1][1],
#             temperature.get("coretemp")[2][1],
#         )
#         message = "Температура компьютера \n"
#         message += f"acpitz: {acpitz}\n"
#         message += f"nouveau: {nouveau}\n"
#         message += f"coretemp: {coretemp}\n"
#         chat = update.effective_chat
#         context.bot.send_message(chat.id, text=message)
#     except Exception as error:
#         logging.error(f"Ошибка при запросе к API температуры: {error}")
#         message = "Что-то поломалось, сообщите разработчику"
#         chat = update.effective_chat
#         context.bot.send_message(chat.id, text=message)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("new_cat", new_cat))
    updater.dispatcher.add_handler(CommandHandler("new_dog", new_dog))
    updater.dispatcher.add_handler(CommandHandler("get_time", get_time))
    # updater.dispatcher.add_handler(CommandHandler("get_weather", get_weather))
    updater.dispatcher.add_handler(CommandHandler("get_dollar", get_dollar))
    # updater.dispatcher.add_handler(CommandHandler("get_temperature", get_temperature))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling(poll_interval=1)
    updater.idle()


if __name__ == "__main__":
    main()
