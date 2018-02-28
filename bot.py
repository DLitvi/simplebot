import logging
import settings
import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram import Sticker


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
def start_bot(bot, update):
	mytext = ('Привет, {} \n!'
			 'Я учебный бот. Но могу тебе помочь. Вот список того, что я умею:\n'
			 'Команда /planet для того, чтобы узнать, в каком созвездии сегодня находится планета.'
			 'Ввдеди данную команду, далее пробел, а затем название плнаеты \n'
			 'Команда /wordcount посчитает количество слов.'
			 'Ввдеди данную команду, пробел, затем в двойных кавычках напиши предложение\n'
			 'Также я умею считать. Для этого введи математическое выражение, поставь равно (например 2+3=), и я скажу тебе ответ.\n'
			 'Я пойму, если ты напишешь мне словами. Только каждое число должно быть от 0 до 10. (Например один и один плюс три). \n'
			 'А еще я скажу тебе, когда следующее полнолуние.'
			 'Для этого напиши "Когда ближайшее полнолуние после " (без ковычек) и укажи дату в формате YYYY.MM.DD'.format(update.message.chat.first_name))
	logging.info('Пользователь {} нажал /start'.format(update.message.chat.username))
	update.message.reply_text(mytext)


def chat(bot, update):
	text = update.message.text
	if text.endswith('='):
		text = calculator(text[:-1])

	elif text.lower().startswith('сколько будет '):
		text = dictionary_calculator(text[14:])

	elif text.lower().startswith('когда ближайшее полнолуние после '):
		text = text.replace('?', '')
		text = full_moon(text[-10:])

	update.message.reply_text(text)
	#sticker = Sticker(file_id='CAADAQADNAIAAiJHOgfE0KNHT2UJIwI', width=100, height=100)
	#update.message.reply_sticker(sticker=sticker)


def ask_planet(bot, update):
	text = update.message.text[8:]
	date = datetime.datetime.now()
	date = date.strftime('%Y/%m/%d')
	print(text)
	text = text.capitalize()
	print(text, date)
	planets_dict = {'Mercury':ephem.Mercury(date), 'Venus':ephem.Venus(date), 
					 'Mars':ephem.Mars(date), 
					'Jupiter':ephem.Jupiter(date), 'Saturn':ephem. Saturn(date),
					'Uranus':ephem.Uranus(date), 'Neptune':ephem.Neptune(date)}
	#'Earth':ephem.Earth(date),
	planet = planets_dict[text]
	text_bot = ephem.constellation(planet)
	update.message.reply_text('{} сегодня находится в созвездии {}'.format(text, ','.join(text_bot)))


def wordcount(bot, update):
	text = update.message.text[11:]
	if text.startswith('"') and text.endswith('"'):
		text = text.replace('"', '')
		text = text.split()

	update.message.reply_text('В вашем сообщении {} слов'.format(len(text)))


def calculator (text):
	try:
		text = text.lower().replace(' ', '')
		parts = text.split('+')

		for plus in range(len(parts)):
			if '-' in parts[plus]:
				parts[plus] = parts[plus].split('-')
			
		for plus in range(len(parts)):
			parts[plus] = precalculator(parts[plus])
	
		result = sum(parts)

	except ValueError:
		result = ('Ты ввел странные символы!')

	except ZeroDivisionError:
		result = ('Ты на ноль делишь. Так нельзя')

	return result


def precalculator(part):
	if type(part) is str:

		if '*' in part:
			result = 1
			for subpart in part.split('*'):
				result *= precalculator(subpart)
			return result

		elif '/' in part:
			parts = list(map(precalculator, part.split('/')))
			result = parts[0]
			for subpart in parts[1:]:
				result /= subpart
			return result

		else:
			return float(part)

	elif type(part) is list:

		for element in range(len(part)):
			part[element] = precalculator(part[element]) 

		return part[0] - sum(part[1:])

	return part


def keyboard(bot, update):
	print('1')
	custom_keyboard = [['top-left', 'top-right'], 
					   ['bottom-left', 'bottom-right']]
	print('2')
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	print('3')
	update.message.reply_text(m.chat_id, 'Кто ты?',
                     reply_markup=keyboard)
	print('4')


def dictionary_calculator(text):
	text = text.lower()
	if text.endswith('?'):
		text = text.replace('?', '')

	text = text.split()
	transformation = {'и':'.', 'один':'1', 'два':'2', 'три':'3',
					'четыре':'4', 'пять':'5', 'шесть':'6',
					'семь':'7', 'восемь':'8', 'девять':'9',
					'десять':'10', 'ноль':'0', 'плюс':'+',
					'минус':'-', 'умножить':'*','разделить':'/'}
	math_expression = ''
	for word in text:
		if word in transformation:
			math_expression +=transformation[word]
	return calculator(math_expression)
	
	print(math_expression)


def full_moon(text):
	text = text.replace('.', '/') 
	text = text.replace('-', '/')
	print(text)
	date = ephem.next_full_moon(text)
	print(ephem.next_full_moon(text))
	return str(date)
	print(date)


def main():
	update = Updater(settings.TELEGRAM_API_KEY)

	update.dispatcher.add_handler(CommandHandler("start", start_bot))
	update.dispatcher.add_handler(CommandHandler("keyboard", keyboard))
	#update.dispatcher.add_handler(MessageHandler(Filters.sticker, chat))
	update.dispatcher.add_handler(MessageHandler(Filters.text, chat))
	update.dispatcher.add_handler(CommandHandler('planet', ask_planet))
	update.dispatcher.add_handler(CommandHandler('wordcount', wordcount))


	update.start_polling()
	update.idle()


if __name__ == "__main__":
	logging.info('Bot started')
	main()