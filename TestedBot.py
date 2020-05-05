import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, StartCommandHandler, DefaultHandler
from StatsParser import StatsParser
from NewsParser import NewsParser
from PlacesParser import PlacesParse
import user
import qr
import schedule
from dataset import ViewMoscow as dataset
from books import books

TOKEN = "001.3868058082.2881881038:752386192"

bot = Bot(token=TOKEN)

def message_cb(bot, event):
    print ('massege')
    UserID = event.data['from']['userId']
    message = event.text
    if message == '/start' and user.check_branch(UserID) == 404:
        bot.send_text(chat_id=event.from_chat,
                    text="Для некоторых функций мне нужно знать в каком городе вы находитесь. Для этого пожалуйста пришлите свое местоположение. Ничего кроме города я о вас не узнаю)",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Хорошо", "callbackData": "geo_ok", "style": "attention"},
                        {"text": "Не хочу!", "callbackData": "geo_neok", "style": "primary"},
                    ]])))
    elif message.split('=')[0] == 'https://www.google.com/maps/search/?api':
        if user.check_branch(UserID) == 404:
            user.add(UserID)
            user.change_branch(UserID, 'main')
        qr.record_City(message,UserID)
        bot.send_text(chat_id=UserID,
                    text="Готово! Теперь вы можете пользоваться всеми моими функциями.")
        bot.send_text(chat_id=event.data['from']['userId'],
                        text="Главное меню",
                        inline_keyboard_markup="{}".format(json.dumps([[
                            {"text": "Статистика", "callbackData": "stats", "style": "attention"}],
                            [{"text": "Новоcти COVID", "callbackData": "news", "style": "attention"}],
                            [{"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"}],
                            [{"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"}],
                            [{"text": "QR код", "callbackData": "QR"}],
                            [{"text": "Экскурсия", "callbackData": "exc"}],
                            [{"text": "Сказки для детей", "callbackData": "books"}
                        ]])))
    else:
        bot.send_text(chat_id=UserID,
                text="Клавиатура воть")
        if user.check_branch(UserID) != 404:
            bot.send_text(chat_id=event.data['from']['userId'],
                        text="Главное меню",
                        inline_keyboard_markup="{}".format(json.dumps([[
                            {"text": "Статистика", "callbackData": "stats", "style": "attention"}],
                            [{"text": "Новоcти COVID", "callbackData": "news", "style": "attention"}],
                            [{"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"}],
                            [{"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"}],
                            [{"text": "QR код", "callbackData": "QR"}],
                            [{"text": "Экскурсия", "callbackData": "exc"}],
                            [{"text": "Сказки для детей", "callbackData": "books"}
                        ]])))

def buttons_answer_cb(bot, event):
    UserID = event.data['from']['userId']
    answer = event.data['callbackData']
    print('User:',UserID)
    if answer == 'books':
        user.change_branch(UserID, 'book')
    if answer == 'QR':
        if qr.check_City(UserID) == 404:
            user.change_branch(UserID,'geolocation')
            bot.send_text(chat_id=UserID,
                    text="Для этой функции мне нужно знать ваш город, для этого пожалуйста отправьте свое местоположение",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Хорошо", "callbackData": "geo_ok", "style": "attention"},
                        {"text": "Не хочу!", "callbackData": "geo_neok", "style": "primary"},
                    ]])))
            
        else:
            bot.send_text(chat_id=UserID,
                    text="Сайт, на котором вы можете получить QR код для выхода на улицу")
            bot.send_text(chat_id=UserID,
                    text=qr.recive_qr(UserID))
    if answer == "geo_ok":
        bot.send_text(chat_id=UserID,
                    text="Жду ваше расположение",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Отмена", "callbackData": "F", "style": "attention"},
                    ]])))
    if answer == "geo_neok":
        user.change_branch(UserID, 'main')
        if user.check_branch(UserID) == 404:
            user.add(UserID)
    if answer == "F":
        user.change_branch(UserID, 'main')
        bot.send_text(chat_id=UserID,
                    text="Отменяюсь")
        if user.check_branch(UserID) == 404:
            user.add(UserID)
    if answer == "stats":
        bot.send_text(chat_id=UserID,
                    text="Статистика на сегодняшний день:")
        parser = StatsParser()
        data = parser.get_data(event.data['from']['userId'])
        for d in data:
            message = f"""{d['title']}
        Заболевших: {d['sick']} (+ {d['sick_incr']})
        Умерших: {d['died']} (+ {d['died_incr']})
        Выздоровевших {d['healed']} (+ {d['healed_incr']})"""
            bot.send_text(chat_id=UserID,
            text=message)
        user.change_branch(UserID, 'choose')
    if answer == 'news':
        p = NewsParser()
        data = p.mailruParser()
        for news in data:
            message = f"""От Mail.ru
            {news['title']}
            {news['url']}"""
            bot.send_text(chat_id=event.data['from']['userId'],
            text=message)
    if answer == 'pharmacy':
        if qr.check_City(UserID) == 404:
            user.change_branch(UserID,'geolocation')
            bot.send_text(chat_id=UserID,
                    text="Для этой функции мне нужно знать ваш город, для этого пожалуйста отправьте свое местоположение",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Хорошо", "callbackData": "geo_ok", "style": "attention"},
                        {"text": "Не хочу!", "callbackData": "geo_neok", "style": "primary"},
                    ]])))
        else:
            print ('pharmacy')
            p = PlacesParse()
            data = p.getPharmacy(UserID)
            for pharmacy in data:
                bot.send_text(chat_id=event.data['from']['userId'],
                text=pharmacy['name'])
                bot.send_text(chat_id=event.data['from']['userId'],
                text=pharmacy['url'])
            user.change_branch(UserID,'main')
    if answer == 'shops':
        if qr.check_City(UserID) == 404:
            user.change_branch(UserID,'geolocation')
            bot.send_text(chat_id=UserID,
                    text="Для этой функции мне нужно знать ваш город, для этого пожалуйста отправьте свое местоположение",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Хорошо", "callbackData": "geo_ok", "style": "attention"},
                        {"text": "Не хочу!", "callbackData": "geo_neok", "style": "primary"},
                    ]])))
        else:
            print('shops')
            p = PlacesParse()
            data = p.getShop(UserID)
            for shop in data:
                bot.send_text(chat_id=event.data['from']['userId'],
                text=shop['name'])
                bot.send_text(chat_id=event.data['from']['userId'],
                text=shop['url'])
            user.change_branch(UserID,'main')
    if answer == "da":
        print('u')
        user.change_branch(UserID, 'main')
        bot.send_text(chat_id=UserID,
                text="Вы подписались на уведомления")
    if answer == "net":
        user.change_branch(UserID, 'main')
    if user.check_branch(UserID) == 'main':
        bot.send_text(chat_id=event.data['from']['userId'],
                        text="Главное меню",
                        inline_keyboard_markup="{}".format(json.dumps([[
                            {"text": "Статистика", "callbackData": "stats", "style": "attention"}],
                            [{"text": "Новоcти COVID", "callbackData": "news", "style": "attention"}],
                            [{"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"}],
                            [{"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"}],
                            [{"text": "QR код", "callbackData": "QR"}],
                            [{"text": "Экскурсия", "callbackData": "exc"}],
                            [{"text": "Сказки для детей", "callbackData": "books"}
                        ]])))       
    if user.check_branch(UserID) == 'choose':
        bot.send_text(chat_id=UserID,
                    text="Хотите подписаться на ежедневные уведомления?",
                    inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Да", "callbackData": "da", "style": "attention"},
                        {"text": "Нет", "callbackData": "net", "style": "primary"},
                    ]])))
    if answer == 'exc':
        bot.send_text(chat_id=event.data['from']['userId'],
                       text='Мы предлагаем вам небольшую экскурсию по достопримичательностям Москвы! Надеемся вы узнаете для себя что-нибудь новое и интересное, а так же хорошо проведете время :)',
                       inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Начнем же!", "callbackData": "moscow_view_1", "style": "primary"},
                    ]])))
        user.change_branch(UserID, 'excursion')
    if user.check_branch(UserID) == 'excursion':
        if event.data['callbackData'] == "moscow_view_1":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[0]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[0]['info'])
            bot.send_text(chat_id=event.data['from']['userId'], text=f"""{dataset[0]['q']}
            1. {dataset[0]['a2']}
            2. {dataset[0]['a3']}
            3. {dataset[0]['a1']}""",
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": "moscow_view_2ff", "style": "primary"},
                        {"text": "2", "callbackData": "moscow_view_2f", "style": "primary"},
                        {"text": "3", "callbackData": "moscow_view_2t", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_2t" or event.data['callbackData'] == "moscow_view_2f" or event.data['callbackData'] == "moscow_view_2ff":
            if event.data['callbackData'] == "moscow_view_2f" or event.data['callbackData'] == "moscow_view_2ff":
                bot.send_text(chat_id=event.data['from']['userId'], text=dataset[0]['ra'])
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text="Правильно!")
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[1]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[1]['info'],
                    inline_keyboard_markup="{}".format(json.dumps([[
                            {"text": "Далее", "callbackData": "moscow_view_3", "style": "primary"}
                        ]])))
        if event.data['callbackData'] == "moscow_view_3":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[2]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[2]['info'],
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Далее", "callbackData": "moscow_view_4", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_4":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[3]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[3]['info'])
            bot.send_text(chat_id=event.data['from']['userId'], text=f"""{dataset[3]['q']}
            1. {dataset[3]['a2']}
            2. {dataset[3]['a1']}
            3. {dataset[3]['a3']}""",
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": "moscow_view_5f", "style": "primary"},
                        {"text": "2", "callbackData": "moscow_view_5t", "style": "primary"},
                        {"text": "3", "callbackData": "moscow_view_5ff", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_5f" or event.data['callbackData'] == "moscow_view_5t" or event.data['callbackData'] == "moscow_view_5ff":
            if event.data['callbackData'] == "moscow_view_5f" or event.data['callbackData'] == "moscow_view_5ff": 
                bot.send_text(chat_id=event.data['from']['userId'], text=dataset[3]['ra'])
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text="Правильно!")
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[4]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[4]['info'],
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Далее", "callbackData": "moscow_view_6", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_6":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[5]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[5]['info'],
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Далее", "callbackData": "moscow_view_7", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_7":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[6]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[6]['info'])
            bot.send_text(chat_id=event.data['from']['userId'], text=f"""{dataset[6]['q']}
            1. {dataset[6]['a2']}
            2. {dataset[6]['a1']}
            3. {dataset[6]['a3']}""",
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": "moscow_view_8t", "style": "primary"},
                        {"text": "2", "callbackData": "moscow_view_8f", "style": "primary"},
                        {"text": "3", "callbackData": "moscow_view_8ff", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_8f" or event.data['callbackData'] == "moscow_view_8t" or event.data['callbackData'] == "moscow_view_8ff":
            if event.data['callbackData'] == "moscow_view_8f" or event.data['callbackData'] == "moscow_view_8ff":
                bot.send_text(chat_id=event.data['from']['userId'], text=dataset[6]['ra'])
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text="Правильно!")
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[7]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[7]['info'],
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Далее", "callbackData": "moscow_view_9", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_9":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[8]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[8]['info'],
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Далее", "callbackData": "moscow_view_10", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_10":
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[9]['url'])
            bot.send_text(chat_id=event.data['from']['userId'], text=dataset[9]['info'])
            bot.send_text(chat_id=event.data['from']['userId'], text=f"""{dataset[9]['q']}
            1. {dataset[9]['a3']}
            2. {dataset[9]['a1']}
            3. {dataset[9]['a2']}""",
                inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": "moscow_view_11f", "style": "primary"},
                        {"text": "2", "callbackData": "moscow_view_11ff", "style": "primary"},
                        {"text": "3", "callbackData": "moscow_view_11t", "style": "primary"}
                    ]])))
        if event.data['callbackData'] == "moscow_view_11f" or event.data['callbackData'] == "moscow_view_11t" or event.data['callbackData'] == "moscow_view_11ff":
            if event.data['callbackData'] == "moscow_view_11f" or event.data['callbackData'] == "moscow_view_11ff":
                bot.send_text(chat_id=event.data['from']['userId'], text=dataset[9]['ra'])
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text="Правильно!")
            bot.send_text(chat_id=event.data['from']['userId'], text="Спасибо за внимание!",
                        inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "Конец экскурсии!", "callbackData": "end", "style": "primary"}
                    ]])))
            user.change_branch(UserID,'main')
    if user.check_branch(UserID) == 'book':
        if event.data['callbackData'] == "1" or event.data['callbackData'] == "2" or event.data['callbackData'] == "3" or event.data['callbackData'] == "4" or event.data['callbackData'] == "5":
            num = int(event.data['callbackData']) - 1
            bot.send_text(chat_id=event.data['from']['userId'], text=books[num]['title'])
            with open(books[num]['audio'], 'rb') as f:
                bot.send_text(chat_id=event.data['from']['userId'], text="Пожалуйста, подождите...")
                bot.send_file(file=f, chat_id=event.data['from']['userId'])
            print('audio')
            with open(books[num]['text'], 'rb') as f:
                bot.send_file(file=f, chat_id=event.data['from']['userId'])
            print('text')
            bot.send_text(chat_id=event.data['from']['userId'],
                        text="Главное меню",
                        inline_keyboard_markup="{}".format(json.dumps([[
                            {"text": "Статистика", "callbackData": "stats", "style": "attention"}],
                            [{"text": "Новоcти COVID", "callbackData": "news", "style": "attention"}],
                            [{"text": "Ближайшие магазины", "callbackData": "shops", "style": "primary"}],
                            [{"text": "Ближайшие аптеки", "callbackData": "pharmacy", "style": "primary"}],
                            [{"text": "QR код", "callbackData": "QR"}],
                            [{"text": "Экскурсия", "callbackData": "exc"}],
                            [{"text": "Сказки для детей", "callbackData": "books"}
                        ]])))
            user.change_branch(UserID,'main')
        if event.data['callbackData'] == "books":
            bot.send_text(chat_id=event.data['from']['userId'], 
            text=f"""Какую книгу хотите получить?
            1. {books[0]['title']}
            2. {books[1]['title']}
            3. {books[2]['title']}
            4. {books[3]['title']}
            5. {books[4]['title']}""",
            inline_keyboard_markup="{}".format(json.dumps([[
                        {"text": "1", "callbackData": "1", "style": "attention"},
                        {"text": "2", "callbackData": "2", "style": "attention"},
                        {"text": "3", "callbackData": "3", "style": "attention"},
                        {"text": "4", "callbackData": "4", "style": "attention"},
                        {"text": "5", "callbackData": "5", "style": "primary"}
                    ]])))   
    
bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()