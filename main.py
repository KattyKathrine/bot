import telebot
from config import TOKEN, currancies
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):

    text = "Чтобы начать работу с ботом, введите запрос в следующием формате:\n\
<имя валюты> <в какую валюту перевести> <количество>\nУвидеть список доступных валют:\n\
/values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def start_message(message):
    text = "Доступные валюты:\n"
    text += "\n".join(currancies.keys())
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def text_message(message):

    try:
        if len(message.text.split(' ')) != 3:
            raise APIException("Количество значений не равно трем.")
    except APIException as err:
        bot.reply_to(message, str(err))
    else:

        quote, base, amount = message.text.split(' ')
        quote = quote.capitalize()
        base = base.capitalize()
        if Converter.check_input(message, bot, quote, base, amount):
            result = Converter.get_price(quote, base, amount)
            text = f'Цена {amount} {quote} в {base} - {result}'
            bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
