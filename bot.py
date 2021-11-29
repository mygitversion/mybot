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

logging.basicConfig(filename='bot.log', \
                    format = '%(asctime)s %(levelname)s %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p',  \
                    level=logging.INFO)  

def greet_user(update, context):
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    user_text = update.message.text 
    update.message.reply_text(user_text) 

def planet_where(update, context):
    user_text = update.message.text
    user_text_list = user_text.strip().split() 
        
    if len(user_text_list) == 0 or user_text_list[0] != '/planet':
        return
    
    msge = "is wrong planet name"
    if len(user_text_list) == 1:
        update.message.reply_text('no name ' + msge)
        return
    
    planet_name = user_text_list[1].lower().capitalize()
    planet_name_valid = planet_name in ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    if planet_name_valid:
        ephem_planet = getattr(ephem, planet_name)()
        ephem_planet.compute('2021/12/01 07:30:12')
        msge = ephem.constellation(ephem_planet)
    else:
        msge = planet_name + ' ' + msge
    
    update.message.reply_text(msge)

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, planet_where))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    # Командуем боту начать ходить в Telegram за сообщениями
    logging.info("Бот стартовал")  
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

if __name__ == "__main__":
    main()

