from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    def get_avatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for("static", filename="images/default.png"), "rb") as f:
                    print(url_for("static", filename="images/default.png"))
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user["avatar"]

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit(".", 1)[1]
        if ext == "png" or ext == "PNG" or ext == "jpg" or ext == "JPG":
            return True
        return False
