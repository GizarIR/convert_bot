import telebot
from extensions import ConvertException, CryptoConvert
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы бота введите команду в формате: ' \
'<имя валюты> <имя валюты, в которую надо перевести> <количество первой валюты>. ' \
'Чтобы узнать доступные валюты введите команду:  /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join([text, key])
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertException('Количество введенных параметров не совпадает с требуемым - 3 параметра')

        quote, base, amount = values

        total_base = CryptoConvert.get_price(quote.lower(), base.lower(), amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {quote}  это  {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
