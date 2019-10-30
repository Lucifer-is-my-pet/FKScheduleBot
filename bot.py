# -*- coding: utf-8 -*-
from datetime import date
import telebot
import re
import os

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

TODAY = date.today()  # date(2020, 1, 28)
battle_kind = "wtf"  # fb

QUEST_SCHEDULE = {
    "визитка": [date(2020, 1, 18), date(2020, 1, 19)],
    "тексты нерейтинг": [date(2020, 1, 25), date(2020, 1, 26)],
    # "драбблы нерейтинг": [date(2020, 1, 26), date(2020, 1, 27)],
    # "мини нерейтинг": [date(TODAY.year, 1, 26), date(TODAY.year, 1, 27)],
    "визуал нерейтинг": [date(2020, 1, 31), date(2020, 2, 1)],
    # "миди нерейтинг": [date(TODAY.year, 1, 26), date(TODAY.year, 1, 27)],
    "челлендж": [date(2020, 2, 7), date(2020, 2, 8)],
    # "бб": [date(TODAY.year, 8, 26), date(TODAY.year, 8, 27)],
    "тексты рейтинг": [date(2020, 2, 15), date(2020, 2, 16)],
    # "драбблы рейтинг": [date(2020, 2, 16), date(2020, 2, 17)],
    # "мини рейтинг": [date(TODAY.year, 2, 16), date(TODAY.year, 2, 17)],
    "визуал рейтинг": [date(2020, 2, 21), date(2020, 2, 22)],
    # "миди рейтинг": [date(TODAY.year, 2, 16), date(TODAY.year, 2, 17)],
    "спецквест": [date(2020, 2, 27), date(2020, 2, 28)]}

VOTE_SCHEDULE = [
    {"name": "визитка", "beginning": date(2020, 1, 20), "end": date(2020, 2, 2),
     "out": "визитку"},
    {"name": "тексты нерейтинг", "beginning": date(2020, 1, 27), "end": date(2020, 2, 9),
     "out": "нерейтинговые тексты", "rating": False},
    # {"name": "драбблы нерейтинг", "beginning": date(2020, 1, 28), "end": date(2020, 2, 10),
    #  "out": "нерейтинговые драбблы", "rating": False},
    # {"name": "мини нерейтинг", "beginning": date(TODAY.year, 8, 2), "end": date(TODAY.year, 8, 23),
    # "out": "нерейтинговые мини", "rating": False},
    {"name": "визуал нерейтинг", "beginning": date(2020, 2, 2), "end": date(2020, 2, 15),
     "out": "нерейтинговый визуал", "rating": False},
    # {"name": "миди нерейтинг", "beginning": date(TODAY.year, 8, 12), "end": date(TODAY.year, 9, 2),
    # "out": "нерейтинговые миди", "rating": False},
    {"name": "челлендж", "beginning": date(2020, 2, 9), "end": date(2020, 2, 22), "out": "челлендж"},
    # {"name": "бб", "beginning": date(TODAY.year, 8, 28), "end": date(TODAY.year, 10, 19), "out": "ББ"},
    {"name": "тексты рейтинг", "beginning": date(2020, 2, 17), "end": date(2020, 3, 2),
     "out": "нерейтинговые тексты", "rating": True},
    # {"name": "драбблы рейтинг", "beginning": date(2020, 9, 8), "end": date(2020, 9, 29),
    #  "out": "рейтинговые драбблы", "rating": True},
    # {"name": "мини рейтинг", "beginning": date(TODAY.year, 9, 13), "end": date(TODAY.year, 10, 4),
    # "out": "рейтинговые мини", "rating": True},
    {"name": "визуал рейтинг", "beginning": date(2020, 2, 23), "end": date(2020, 3, 7),
     "out": "рейтинговый визуал", "rating": True},
    # {"name": "миди рейтинг", "beginning": date(TODAY.year, 9, 23), "end": date(TODAY.year, 10, 14),
    # "out": "рейтинговые миди", "rating": True},
    {"name": "спецквест", "beginning": date(2020, 2, 29), "end": date(2020, 3, 13), "out": "спецквест"}]


def is_not_in_quest_list(word):
    if word not in QUEST_SCHEDULE.keys():
        return True
    return False


def quest_feature(quest_name, feature):
    return list(filter(lambda quest: quest["name"] == quest_name, VOTE_SCHEDULE))[0][feature]


def quest_date(sought_quest, *args):
    print(sought_quest, args)
    if args[0]:
        sought_quest = sought_quest + " " + args[0]

    quest_first_date = QUEST_SCHEDULE[sought_quest.lower()][0]
    quest_second_date = QUEST_SCHEDULE[sought_quest.lower()][1]
    quest_days_left = (quest_first_date - TODAY).days

    if quest_days_left > 0:
        return sought_quest.capitalize() + ": " + quest_first_date.strftime("%d.%m") + "-" + quest_second_date.strftime(
            "%d.%m") + ", осталось дней до выкладки: {}".format(quest_days_left)
    else:
        return sought_quest.capitalize() + ": " + quest_first_date.strftime("%d.%m")


def vote_date(sought_quest: str, *args):
    # if sought_quest.find("чел") + 1:
    #     sought_quest = "челлендж"

    # quests = set(map(lambda quest: quest["name"], VOTE_SCHEDULE))
    # if sought_quest not in quests:
    #     bot.say("Таких квестов не знаю")
    #     return

    # rating = None
    # if args:
    #     if args[0] not in ["рейтинг", "нерейтинг"]:
    #         bot.say("Квест либо рейтинговый, либо нерейтинговый, третьего не дано")
    #         return
    #     else:
    #         rating = True if args[0] == "рейтинг" else False

    # фильтруем список голосования
    # if rating is None:  # оставляем квесты без разделения на рейтинг и нерейтинг
    #     vote_schedule_filtered = list(filter(lambda quest: "rating" not in quest.keys(), VOTE_SCHEDULE))
    # elif rating:  # оставляем рейтинговые
    #     vote_schedule_filtered = list(filter(lambda quest: "rating" in quest.keys() and quest["rating"], VOTE_SCHEDULE))
    # else:  # оставляем нерейтинговые
    #     vote_schedule_filtered = list(
    #         filter(lambda quest: "rating" in quest.keys() and not quest["rating"], VOTE_SCHEDULE))

    # quests = set(map(lambda quest: quest["name"], vote_schedule_filtered))
    # if sought_quest not in quests:
    #     bot.say("У этого квеста нет разделения на рейтинг и нерейтинг")
    #     return

    for quest in VOTE_SCHEDULE:  # vote_schedule_filtered
        if sought_quest == quest["name"]:  # название искомого квеста встретилось в списке
            if quest["beginning"] > TODAY:  # если дата начала голосования позже сегодня
                return "Голосование за {} ещё не началось".format(quest["out"])
            elif quest["end"] < TODAY:  # если дата окончания голосования раньше сегодня
                return "Голосование за {} уже закончилось".format(quest["out"])
            else:
                return "Голосование за {} закончится ".format(quest["out"]) + quest["end"].strftime("%d.%m")


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
# bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = """*Основные команды:*
/quest узнать, когда выкладка конкретного квеста (кнопочки)
/vote узнать, сколько до конца голосования за конкретный квест (кнопочки)
/pic получить картинку с расписанием

Можно обратиться к боту в строке из любого чата и указать название квеста:
`@FKScheduleBot драбблы рейтинг`
`@FKScheduleBot голосование спецквест`"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
    # bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['pic'])
def schedule(message):
    # photo = open('187 (1).png', 'rb')
    bot.send_message(message.chat.id, 'http://funkyimg.com/i/2MdrS.png')
    # bot.send_photo(message.chat.id, photo)


# кнопки
@bot.message_handler(commands=["quest"])
def quest(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text="Рейтинг", callback_data="рейтинг"),
        telebot.types.InlineKeyboardButton(text="Нерейтинг", callback_data="нерейтинг"),
        telebot.types.InlineKeyboardButton(text="Другое", callback_data="другое"))
    bot.send_message(message.chat.id, "Рейтинговый квест или нет?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'квест')
def callback_button_quest(call):
    if call.message:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text="Рейтинг", callback_data="рейтинг"),
            telebot.types.InlineKeyboardButton(text="Нерейтинг", callback_data="нерейтинг"),
            telebot.types.InlineKeyboardButton(text="Другое", callback_data="другое"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Рейтинговый квест или нет?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'квест гол')
def callback_button_vote(call):
    if call.message:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text="Рейтинг", callback_data="рейтинг гол"),
            telebot.types.InlineKeyboardButton(text="Нерейтинг", callback_data="нерейтинг гол"),
            telebot.types.InlineKeyboardButton(text="Другое", callback_data="другое гол"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Голосование за рейтинговый квест или нет?", reply_markup=keyboard)


# кнопки
@bot.message_handler(commands=["vote"])
def vote(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text="Рейтинг", callback_data="рейтинг гол"),
        telebot.types.InlineKeyboardButton(text="Нерейтинг", callback_data="нерейтинг гол"),
        telebot.types.InlineKeyboardButton(text="Другое", callback_data="другое гол"))
    bot.send_message(message.chat.id, "Голосование за рейтинговый квест или нет?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] in ['рейтинг', 'нерейтинг'])
def callback_button_rating_quests(call):
    # Если сообщение из чата с ботом
    if call.message:
        is_vote = ""
        if call.data.find("гол") + 1:
            is_vote = " гол"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text=" « ", callback_data="квест" + is_vote),
            telebot.types.InlineKeyboardButton(text="Тексты", callback_data="тексты"))
            # telebot.types.InlineKeyboardButton(text="Драбблы", callback_data="драбблы " + call.data),
            # telebot.types.InlineKeyboardButton(text="Мини", callback_data="мини " + call.data))
        keyboard.row(
            telebot.types.InlineKeyboardButton(text="Визуал", callback_data="визуал " + call.data))
            # telebot.types.InlineKeyboardButton(text="Миди", callback_data="миди " + call.data))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выбери квест", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'другое')
def callback_button_other_quests(call):
    if call.message:
        is_vote = ""
        if call.data.find("гол") + 1:
            is_vote = " гол"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(text=" « ", callback_data="квест" + is_vote),
            telebot.types.InlineKeyboardButton(text="Визитка", callback_data="визитка" + is_vote),
            telebot.types.InlineKeyboardButton(text="Челлендж", callback_data="челлендж" + is_vote))
        keyboard.row(
            telebot.types.InlineKeyboardButton(text="ББ", callback_data="бб" + is_vote),
            telebot.types.InlineKeyboardButton(text="Спецквест", callback_data="спецквест" + is_vote))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выбери квест", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] in ['тексты', 'драбблы', 'мини', 'визуал', 'миди'])
def callback_button_texts_and_visual_response(call):
    if call.message:
        if call.data.find("гол") + 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=vote_date(call.data[:-4]))
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=quest_date(call.data))


@bot.callback_query_handler(func=lambda call: call.data.split()[0] in ['визитка', 'челлендж', 'бб', 'спецквест'])
def callback_button_other_response(call):
    if call.message:
        if call.data.find("гол") + 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=vote_date(call.data[:-4]))
        else:  # если нет "гол"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=quest_date(call.data))


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query_text(query):
    pattern = re.compile(r'^([а-яА-Я]+)[ ]*([а-яА-Я]*)[ ]*([а-яА-Я]*)$', re.MULTILINE)

    try:
        matches = pattern.match(query.query)  # на случай если ввели херню
    except AttributeError as ex:
        return

    query_array = list(map(lambda query_word: query_word.lower(), query.query.split()))
    rating = ""

    if len(query_array) == 3:
        if query_array[0] == "голосование":
            sought_quest, rating = query_array[1], query_array[2]
    if len(query_array) == 2:
        if query_array[0] == "голосование":
            sought_quest = query_array[1]
        else:
            sought_quest, rating = query_array[0], query_array[1]
    else:
        sought_quest = query_array[0]

    if sought_quest.find("чел") + 1:
        sought_quest = "челлендж"

    quests = set(QUEST_SCHEDULE.keys())  # map(lambda quest: quest["name"], QUEST_SCHEDULE)
    if rating:
        if sought_quest + " " + rating not in quests:
            print("Таких квестов не знаю: " + sought_quest + " " + rating)
            return
    else:
        if sought_quest not in quests:
            print("Таких квестов не знаю: " + sought_quest)
            return

    if "голосование" in query_array:
        title = "Голосование"
        result_dates = vote_date(sought_quest, rating)
    else:
        title = "Квест"
        result_dates = quest_date(sought_quest, rating)

    result = telebot.types.InlineQueryResultArticle(
        id='1', title=title,
        input_message_content=telebot.types.InputTextMessageContent(  # то, что пойдёт в чат
            message_text=result_dates,
            parse_mode='HTML'),
        description=result_dates
        # что будет во всплывающем поле над строкой
    )
    bot.answer_inline_query(query.id, [result])


# try:
bot.polling(none_stop=True, timeout=123)
# except ProxyError:
#     telebot.apihelper.proxy = {'https':''}
#     bot.polling()
