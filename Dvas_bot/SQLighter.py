import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def add_new_row(self):
        with self.connection:
            return self.cursor.execute('INSERT INTO music (id, number, title)')

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def add_new_song(self, file_id, file_name, wrongs):
        with self.connection:
            return self.cursor.execute('INSERT INTO music (file_id, right_answer, wrong_answers) VALUES(?, ?, ?)',
                                       (file_id, file_name, wrongs))

    def increment_stat(self, user_id, incr):
        with self.connection:
            try:
                return self.cursor.execute('INSERT INTO statistics (chat_user_id, user_stat) VALUES(?, ?)',
                                           (user_id, incr))
            except:
                stat = self.cursor.execute("SELECT user_stat FROM statistics WHERE chat_user_id = ?",
                                           user_id)
                self.cursor.execute("UPDATE statistics SET user_stat = ? WHERE chat_user_id = ? VALUES(?, ?)",
                                    (incr+stat, user_id))

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
