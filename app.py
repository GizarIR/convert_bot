import telebot

TOKEN ='5468058144:AAEKHdTA40eeou88cMCsMblvB4b2pdiz21w'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Hello {message.chat.username}")


bot.polling()
