import telebot
from telebot import types

from config import TOKEN, INSTRUCTIONS_PATH
from extensions import *


bot = telebot.TeleBot(TOKEN)

instructions_text = open(INSTRUCTIONS_PATH, 'r', encoding='utf-8').read()


@bot.message_handler(commands=['start', 'help'])
def start_help_command(message):
    bot.send_message(message.from_user.id, instructions_text)


@bot.message_handler(commands=['values'])
def values_list_command(message):
    text = f'Валюты:\n\n' \
           f'[{list(VALUES.keys())[0]}] {VALUES["EUR"][0]}\n' \
           f'[{list(VALUES.keys())[1]}] {VALUES["USD"][3]}\n' \
           f'[{list(VALUES.keys())[2]}] {VALUES["RUB"][3]}'
    bot.send_message(message.from_user.id, text)


@bot.message_handler(content_types=['text'])
def convert_message(message):
    words = message.text.split(' ')
    try:
        if len(words) != 3:
            raise APIException
    except APIException:
        bot.send_message(message.from_user.id, f'❗ Аргумента должно быть 3')
        return 0

    try:
        base = [key for key, value in VALUES.items() if words[0].upper() in list(map(lambda x: x.upper(), value))][0]
    except IndexError:
        bot.send_message(message.from_user.id, f'❗ Валюты с названием {words[0]} не существует')
        return 0

    try:
        quote = [key for key, value in VALUES.items() if words[1].upper() in list(map(lambda x: x.upper(), value))][0]
    except IndexError:
        bot.send_message(message.from_user.id, f'❗ Валюты с названием {words[1]} не существует')
        return 0

    try:
        amount = int(words[2])
    except ValueError:
        bot.send_message(message.from_user.id, f'❗ Вы ввели не число в качестве количества')
        return 0

    result = ValuesManager.get_price(base, quote, amount)
    text = f'Результат конвертирования {base} в {quote}: {result}'
    bot.send_message(message.from_user.id, text)


if __name__ == '__main__':
    bot.polling()
