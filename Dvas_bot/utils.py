import shelve
from random import shuffle
from telebot import types
from SQLighter import SQLighter
from config import SHELVE_NAME, DATABASE_NAME


def count_rows():
    """
    Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
    Потом из этого количества будем выбирать музыку.
    """
    db = SQLighter(DATABASE_NAME)
    rowsnum = db.count_rows()
    with shelve.open(SHELVE_NAME) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(SHELVE_NAME) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(SHELVE_NAME) as storage:
        # 0 - count of right answers in current session
        storage[str(chat_id)] = [estimated_answer, 0]


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(SHELVE_NAME) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(SHELVE_NAME) as storage:
        try:
            answer = storage[str(chat_id)][0]
            return answer
        except KeyError:
            return None


def increment_count_right_answer(user_id):
    """
    Обновляем статистику правильных ответов пользователя
    :param chat_id: id юзера
    """

    with shelve.open(SHELVE_NAME) as storage:
        try:
            incr = storage[str(user_id)][1]

        except KeyError:
            incr = 0

    # Сделать окончание игры по команде пользователя и не дёргать БД каждый раз
    db = SQLighter(DATABASE_NAME)
    db.increment_stat(user_id, incr)
    db.close()


def generate_markup(right_answer, wrong_answers):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильными
    all_answers = '{},{}'.format(right_answer, wrong_answers)

    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)

    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup
