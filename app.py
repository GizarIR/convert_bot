import telebot
from  telebot import types
from extensions import ConvertException, CryptoConvert
from config import TOKEN, keys

# простое создание кнопок
# conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
# buttons = []
# for val in keys.keys():
#     buttons.append(types.KeyboardButton(val.capitalize()))
# conv_markup.add(*buttons)

# динамическое создание клавиатуры
def create_markup(quote = None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != quote:
            buttons.append(types.KeyboardButton(val.capitalize()))
    markup.add(*buttons)
    return markup


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Бот имеет 2 режима работы. Первый - Краткий: Для начала работы бота введите команду в формате: ' \
'<имя валюты> <имя валюты, в которую надо перевести> <количество первой валюты>. ' \
'Второй - Диалог. Для старта данного режима наберите: /convert ' \
'Чтобы узнать доступные валюты введите команду:  /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join([text, key])
    bot.reply_to(message, text)

# реализация диалога с ботом
@bot.message_handler(commands=['convert'])
def answer_quote(message: telebot.types.Message):
    text = "Выберите валюту, из которой хотите конвертировать"
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, quote_handler)

def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().lower()
    text = "Выберите валюту, в которую Вы хотите конвертировать"
    bot.send_message(message.chat.id, text, reply_markup=create_markup('quote'))
    bot.register_next_step_handler(message, base_handler, quote)

def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip().lower()
    text = "Введите сумму конвертации"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)

def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip().lower()
    try:
        total_base = CryptoConvert.get_price(quote, base, amount)
    except ConvertException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации. \n{e}')
    else:
        text = f'{amount} {quote}  это  {total_base} {base}'
        bot.send_message(message.chat.id, text)


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
