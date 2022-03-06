import math
import sqlite3 as sq
import time
import datetime


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        try:
            self.__cur.execute("""SELECT * FROM mainmenu""")
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_post(self, name, file, wiki, url, bio, col1, col2, col3):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (name, file, wiki, url, bio, col1, col2, col3, tm))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    async def add_message_a(self, mail, message):
        try:
            t = str(datetime.datetime.now())
            self.__cur.execute("INSERT INTO messages VALUES (?, ?, ?)",
                               (mail, message, t))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def add_message(self, mail, message):
        try:
            t = str(datetime.datetime.now())
            self.__cur.execute("INSERT INTO messages VALUES (?, ?, ?)",
                               (mail, message, t))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def get_post(self, alias):
        try:
            self.__cur.execute(f"SELECT * FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False, False

    def get_pict(self, alias):
        try:
            self.__cur.execute(f"SELECT file FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False, False

    def get_all_posts(self):
        try:
            self.__cur.execute(f"SELECT id, name, bio, url FROM posts ORDER BY time DESC ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sq.Error as e:
            print("Ошибка получения статьи из БД " + str(e))
        return []

    def get_authors(self):
        try:
            self.__cur.execute(f"SELECT name, url FROM posts ORDER BY name DESC ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sq.Error as e:
            print("getAuthors: Ошибка получения статьи из БД " + str(e))
        return []

    def delete_post(self, url):
        try:
            print(url)
            self.__cur.execute(f"DELETE FROM posts WHERE url LIKE '{url}'")
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False

        return True

    def add_user(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким email уже сущесвует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sq.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_user_by_mail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sq.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def update_user_avatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sq.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def update_post(self, name, file, wiki, url, bio, col1, col2, col3, alias):
        try:
            tm = math.floor(time.time())
            if file:
                self.__cur.execute(f"""UPDATE posts SET file = ? WHERE url = ?""", (file, alias))
            self.__cur.execute(f"""UPDATE posts SET name = '{name}', wiki = '{wiki}', url = '{url}', bio = '{bio}', col1 = '{col1}', col2 = '{col2}', col3 = '{col3}' WHERE url LIKE '{alias}'""")
            self.__db.commit()
            self.__cur.execute(f"""SELECT * FROM posts WHERE url = '{url}' LIMIT 1""")
            res = self.__cur.fetchone()
        except sq.Error as e:
            print("updatePost: Ошибка обновления статьи в БД " + str(e))
            return False
        return res
