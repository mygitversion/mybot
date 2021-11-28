'''
Задание 1-ой недели курса:  начальная версия Telegram бота
----------------------------------------------------------
Код создан пошагово по видеолекциям Михаила Корнеева 
(я пока не стал убирать строки с "print()", так как в дальнейшем код будет дополнительно модифицироваться и
усложняться, насколько я понял)
'''
import logging
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)  

def greet_user(update, context):
    print("Вызван /start") 
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text) 

def planet_where(update, context):
    user_text = update.message.text
    print('user text', user_text)
    user_text_list = user_text.strip().split() 
    print('user text list', user_text_list)
    bool0 = len(user_text_list) == 2
    bool1 = user_text_list[0] == '/planet'
    planet_name = user_text_list[1].lower().capitalize()
    bool2 = planet_name in ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    print('bool0 and bool1 and bool2:', bool0 and bool1 and bool2)
    if bool0 and bool1 and bool2:
        ephem_planet = getattr(ephem, planet_name)()
        ephem_planet.compute('2021/11/29 07:30:12')
        msge = ephem.constellation(ephem_planet)
    else:
        msge = "The planet name doesn't exist"
    print(msge)
    update.message.reply_text(msge)

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, planet_where))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    # Командуем боту начать ходить в Telegram за сообщениями
    logging.info("Бот стартовал")   # to do: добавить дату и время в логи
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

if __name__ == "__main__":
    main()

