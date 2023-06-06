import telebot
import requests
from bs4 import BeautifulSoup
import random

bot = telebot.TeleBot('6230693672:AAEV3dBdzKXjKHSgUPggl2IGqwucRb_Jk-k')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Нажми кнопку для получения случайной машины.")
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    button = telebot.types.KeyboardButton('/get_car')
    markup.add(button)
    bot.send_message(message.chat.id, "Нажми кнопку '/get_car' для получения машины.", reply_markup=markup)

@bot.message_handler(commands=['get_car'])
def get_car(message):
    url = 'https://www.mashina.kg/'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        cars = soup.find_all('div', class_='listing-item')

        if cars:
            random_car = random.choice(cars)

            title = random_car.find('a', class_='listing-name').text.strip()

            price = random_car.find('div', class_='listing-price').text.strip()

            image_url = random_car.find('img', class_='listing-image').get('src')

            bot.send_message(message.chat.id, f"Марка и модель: {title}\nЦена: {price}")
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.send_message(message.chat.id, "На сайте нет доступных машин")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении данных с сайта")


bot.polling()
