import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler
from StatsParser import StatsParser
from NewsParser import NewsParser
#from PlacesParser import PlacesParse
import user
import qr

TOKEN = "001.3868058082.2881881038:752386192"

bot = Bot(token=TOKEN)

def start(bot, event):
    bot.send_text(chat_id=event.data['queryId'],
                  text="Приветствую!")
    user.add(event.data['from']['userId'])

def game(bot, chat_id):
    global GAME_STARTED
    GAME_STARTED = True
    bot.send_text(chat_id=chat_id,
                  text="Game started")
    bot.send_text(chat_id=chat_id,
                  text="https://sun9-58.userapi.com/c855536/v855536860/22c4e2/MPqGe47q1qg.jpg")

def buttons_answer_cb(bot, event):
    if event.data['callbackData'] == "stats":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Статистика на сегодняшний день:",
            show_alert=True
        )
        parser = StatsParser()
        data = parser.get_data(event.data['from']['userId'])
        for d in data:
            message = f"""{d['title']}
        Заболевших: {d['sick']} (+ {d['sick_incr']})
        Умерших: {d['died']} (+ {d['died_incr']})
        Выздоровевших {d['healed']} (+ {d['healed_incr']})"""
            bot.send_text(chat_id=event.data['from']['userId'],
            text=message)
    elif event.data['callbackData'] == "shop":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="....",
            show_alert=False
        )
    elif event.data['callbackData'] == 'news':
        p = NewsParser()
        data = p.mailruParser()
        for news in data:
            message = f"""От Mail.ru
            {news['title']}
            {news['url']}"""
            bot.send_text(chat_id=event.data['from']['userId'],
            text=message)
    bot.send_text(chat_id=event.data['from']['userId'],
                      text="Что вам необходимо?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Статистика", "callbackData": "stats", "style": "attention"},
                          {"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"},
                          {"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"},
                          {"text": "Новоти", "callbackData": "news", "style": "primary"}
                      ]])))

with open('answers.json', 'r', encoding="utf-8") as f:
    templates = json.load(f)


def message_cb(bot, event):
    if event.text == "menu":
        bot.send_text(chat_id=event.from_chat,
                      text="Что вам необходимо?",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Статистика", "callbackData": "stats", "style": "attention"},
                          {"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"},
                          {"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"},
                          {"text": "Новоти", "callbackData": "news", "style": "primary"}
                      ]])))
    else:
        ques = ''
        for mes in templates['answer']:
            for ans in mes['plate']:
                if ans == event.text:
                    ques = mes['model']
                    bot.send_text(chat_id=event.from_chat,
                                  text=ques)
        if ques == "":
            bot.send_text(chat_id=event.from_chat,
                          text="Ошибка!Я не понимаю, что вы хотете",
                          inline_keyboard_markup="{}".format(json.dumps([[
                              {"text": "Статистика", "callbackData": "call_back_id_2", "style": "attention"},
                              {"text": "Помощь", "callbackData": "call_back_id_3", "style": "primary"}]])
                          ))

'''def geobord(bot, event):
    if data['callbackData'].split('=')[0] == 'https://www.google.com/maps/search/?api':
        qr.record_City(data['callbackData'],event.data['from']['userId'])
    elif data['callbackData'] == "cancell":
        return 0
    bot.send_text(chat_id=event.from_chat,
                      text="Пожалуйста отправьте вашу геолокацию для определения города, в котором вы находитесь. Это необходимо для большинства функций",
                      inline_keyboard_markup="{}".format(json.dumps([[
                          {"text": "Отмена", "callbackData": "cancell", "style": "attention"},
                      ]])))

def geocheck (bot, event):
    if qr.check_City(UserID) == 0:
        return ('ok')
    else:
        bot.dispatcher.add_handler(MessageHandler(callback=geobord))'''

bot.dispatcher.add_handler(StartCommandHandler(callback=start))
bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()
