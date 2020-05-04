import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler, DefaultHandler
from StatsParser import StatsParser
from NewsParser import NewsParser
from PlacesParser import PlacesParse
import user
import qr
import schedule

TOKEN = "001.3868058082.2881881038:752386192"

bot = Bot(token=TOKEN)

def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat,
                      text="Что вам необходимо?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Статистика", "callbackData": "stats", "style": "attention"},
                          {"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"},
                          {"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"},
                          {"text": "Новоти", "callbackData": "news", "style": "primary"}
                      ]])))
    UserID = event.data['from']['userId']
    message = event.text
    if message == '/start' and user.check_branch(UserID) == []:
        user.add(UserID)
        bot.send_text(chat_id=event.from_chat,
                      text="Что вам необходимо?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Статистика", "callbackData": "stats", "style": "attention"},
                          {"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"},
                          {"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"},
                          {"text": "Новоти", "callbackData": "news", "style": "primary"}
                      ]])))

def buttons_answer_cb(bot, event):
    #print(event)
    UserID = event.data['from']['userId']
    answer = event.data['callbackData']
    #branch = user.check_branch(UserID)
    print(user.check_branch(UserID))  
    if answer == "stats":
        print('stats')
        bot.send_text(chat_id=UserID,
                    text="Статистика на сегодняшний день:")
        parser = StatsParser()
        data = parser.get_data(event.data['from']['userId'])
        print(data)
        for d in data:
            message = f"""{d['title']}
        Заболевших: {d['sick']} (+ {d['sick_incr']})
        Умерших: {d['died']} (+ {d['died_incr']})
        Выздоровевших {d['healed']} (+ {d['healed_incr']})"""
            bot.send_text(chat_id=UserID,
            text=message)
        user.change_branch(UserID, 'choose')
    if answer == 'news':
        print('Aj')
        p = NewsParser()
        data = p.mailruParser()
        for news in data:
            message = f"""От Mail.ru
            {news['title']}
            {news['url']}"""
            bot.send_text(chat_id=event.data['from']['userId'],
            text=message)
    if answer == 'pharmacy':
        p = PlacesParse()
        data = p.getPharmacy(UserID)
        for pharmacy in data:
            bot.send_text(chat_id=event.data['from']['userId'],
            text=pharmacy['name'])
            bot.send_text(chat_id=event.data['from']['userId'],
            text=pharmacy['url'])
    if answer == 'shops':
        p = PlacesParse()
        data = p.getShop(UserID)
        for shop in data:
            bot.send_text(chat_id=event.data['from']['userId'],
            text=shop['name'])
            bot.send_text(chat_id=event.data['from']['userId'],
            text=shop['url'])
    if answer == "da":
        print('u')
        user.change_branch(UserID, 'main')
        bot.send_text(chat_id=UserID,
                text="Вы подписались на уведомления")
    if answer == "net":
        print('a')
        user.change_branch(UserID, 'main')
    if user.check_branch(UserID) == 'main':
        bot.send_text(chat_id=event.data['from']['userId'],
                    text="Что вам необходимо?",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Статистика", "callbackData": "stats", "style": "attention"},
                        {"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"},
                        {"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"},
                        {"text": "Новоcти", "callbackData": "news", "style": "primary"}
                    ]])))       
    if user.check_branch(UserID) == 'choose':
        bot.send_text(chat_id=UserID,
                    text="Хотите подписаться на ежедненвые уведомления?",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Да", "callbackData": "da", "style": "attention"},
                        {"text": "Нет", "callbackData": "net", "style": "primary"},
                    ]])))
    
bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()