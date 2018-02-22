import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import Sticker


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start_bot(bot, update):
	mytext = 'Привет, {}'.format(update.message.chat.first_name)
	update.message.reply_text(mytext)


def chat(bot, update):
	text = update.message.text
	update.message.reply_text(text)
	sticker = Sticker(file_id='CAADAQADNAIAAiJHOgfE0KNHT2UJIwI', width=100, height=100)
	update.message.reply_sticker(sticker=sticker)


def main():
	update = Updater(settings.TELEGRAM_API_KEY)

	update.dispatcher.add_handler(CommandHandler("start", start_bot))
	update.dispatcher.add_handler(MessageHandler(Filters.sticker, chat))
	update.dispatcher.add_handler(MessageHandler(Filters.text, chat))


	update.start_polling()
	update.idle()


if __name__ == "__main__":
	logging.info('Bot started')
	main()