import telebot
import config
import os
import time
import random

from SQLighter import *
import utils

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    dirlist = os.listdir('music/')
    db_worker = SQLighter(config.DATABASE_NAME)
    for file in dirlist:
        if file.split('.')[-1] == 'ogg':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.from_user.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.from_user.id, msg.voice.file_id, reply_to_message_id=msg.message_id)

            # ПРоблема: варианты ответа всегда одни и те же для соответствуюих заданий
            f_idx = dirlist.index(file)
            wrong_answers_list = random.sample(dirlist[:f_idx] + dirlist[f_idx+1:], 3)
            wrong_answers_str = ''
            for i in range(len(wrong_answers_list)):
                wrong_answers_str = wrong_answers_str + wrong_answers_list[i][:-5] + ','

            db_worker.add_new_song(msg.voice.file_id, file, wrong_answers_str)
        time.sleep(1)
    db_worker.close()


@bot.message_handler(commands=['game'])
def game(message):
    db_worker = SQLighter(config.DATABASE_NAME)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))

    markup = utils.generate_markup(row[2], row[3])
    bot.send_voice(message.from_user.id, row[1], reply_markup=markup)
    utils.set_user_game(message.from_user.id, row[2])

    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.from_user.id)
    if not answer:
        bot.send_message(message.from_user.id, 'Чтобы поиграть введите "/game"')
    else:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()

        if message.text == answer:
            bot.send_message(message.from_user.id, 'Верно!')
            utils.increment_count_right_answer(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, 'Неверно')
        reply_markup = keyboard_hider
        utils.finish_user_game(message.from_user.id)


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)