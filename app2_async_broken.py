from quart import Quart, \
    render_template, \
    request, flash, \
    redirect, \
    url_for, \
    abort, \
    g, make_response

import sqlite3 as sq
from time import time

import aiohttp
# from asgiref.wsgi import WsgiToAsgi

from flask_login import LoginManager, \
    login_user, \
    login_required, \
    logout_user, \
    current_user

from werkzeug.security import generate_password_hash, check_password_hash

from my_user_login import UserLogin
from bot_async import send_message
import sqlite3 as sq

from forms import FlaskForm

from DataBase import DataBase

# from forms import LoginForm


DEBUG = True

app = Quart(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста авторизуйтесь"
login_manager.login_message_category = "success"

app.config["SECRET_KEY"] = '1JNFJNFNGHMNGHKMHGKYRVTAWEURKNTONIKBJUVHY'
app.config["DATABASE"] = "site.db"

# db2 = SQLAlchemy(app)


# class Users(db2.Model):
#     id = db2.Column(db2.Integer, primary_key=True)
#     email = db2.Column(db2.String(50), unique=True)
#     psw = db2.Column(db2.String(500), nullable=True)
#     date = db2.Column(db2.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"users {self.id}"
#
#
# class Profiles(db2.Model):
#     id = db2.Column(db2.Integer, primary_key=True)
#     name = db2.Column(db2.String(50), unique=True)
#     old = db2.Column(db2.Integer)
#     city = db2.Column(db2.String(100))
#
#     user_id = db2.Column(db2.Integer, db2.ForeignKey("users.id"))
#
#     def __repr__(self):
#         return f"profiles {self.id}"


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


@login_manager.user_loader
def load_user(user_id):
    print("user_loader")
    return UserLogin().fromDB(user_id, dbase)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("page_not_found.html", title="Not found"), 404


def connect_db():
    conn = sq.connect(app.config["DATABASE"], check_same_thread=False)
    conn.row_factory = sq.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource("my_first_sql.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Устанавливаем соединениее с БД через глобальную переменную g"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(exeption):
    """Закрываем соединениее с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/")
async def home():
    return await render_template('home.html',
                                 authors=dbase.get_authors(),
                                 title="Главная страница")


@app.route("/create", methods=["POST", "GET"])
@login_required
async def create():
    if request.method == "POST":
        file = request.files["file"]
        # print("file:")
        # print(file.__class__)
        if file:
            try:
                pic = file.read()
            except FileNotFoundError as e:
                await flash("Ошибка чтения файла", "error")
        else:
            await flash("Ошибка получения файла из формы", "error")
        if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
            res = dbase.add_post(request.form["name"],
                                 pic,
                                 request.form["wiki"],
                                 request.form["url"],
                                 request.form["post"],
                                 request.form["col1"],
                                 request.form["col2"],
                                 request.form["col3"])
            if not res:
                await flash("Ошибка добавления статьи", category="error")

            else:
                await flash("Статья добавлена успешно", category="success")
                return redirect(url_for("show_post", alias=request.form["url"]))
        else:
            await flash("Ошибка добавления статьи", category="error")

    return render_template('create.html',
                           authors=dbase.get_authors(),
                           title="Добаление статьи")


@app.route("/update/<alias>", methods=["POST", "GET"])
@login_required
def update(alias):
    post = dbase.get_post(alias)
    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                pic = file.read()
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            pic = None

        res = dbase.update_post(name=request.form["name"],
                                file=pic,
                                wiki=request.form["wiki"],
                                url=request.form["url"],
                                bio=request.form["post"],
                                col1=request.form["col1"],
                                col2=request.form["col2"],
                                col3=request.form["col3"],
                                alias=alias)
        if res:
            flash("Статья обновления успешно", category="success")
            return redirect(url_for("show_post", alias=res["url"]))

        else:
            flash("Ошибка обновления статьи", category="error")

    return render_template('update.html',
                           authors=dbase.get_authors(),
                           post=post,
                           title="Редактирование статьи")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form["name"]) > 4 and \
                len(request.form["email"]) > 4 and \
                len(request.form["psw"]) > 4 and \
                (len(request.form["psw"]) == len(request.form["psw2"])):
            hash = generate_password_hash(request.form["psw"])
            res = dbase.add_user(request.form["name"], request.form["email"], hash)
            if res:
                flash("Вы успешно зарегистрировалсь", "success")
                return redirect(url_for("login"))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполены поля", "error")
    return render_template("register2.html",
                           title="Регистрация")


# @app.route("/registerAlchemy", methods=["POST", "GET"])
# def registerAlchemy():
#     if request.method == "POST":
#         try:
#             hash = generate_password_hash(request.form["psw"])
#             u = Users(email=request.form["email"], psw=hash)
#             db2.session.add(u)
#             db2.session.flush()
#             p = Profiles(name=request.form["name"],
#                          old=request.form["old"],
#                          city=request.form["city"],
#                          user_id=u.id)
#             db2.session.add(p)
#             db2.session.commit()
#             flash("Вы успешно зарегистрировалсь", "success")
#         except Exception as e:
#             db2.session.rollback()
#             print("*****************")
#             print(e)
#             flash("Ошибка при добавлении в БД", "error")
#
#     return render_template("registerAlchemy.html",
#                            title="Форма регистрации")


async def get_mess():
    return await aiohttp.web.Request


@app.route("/contact", methods=["POST", "GET"])
@login_required
async def contact():
    if request.method == "POST":
        # async with aiohttp.ClientSession() as session:
        #     url = "http://127.0.0.1:5000/contact"
        #     async with session.get(url, allow_redirects=True) as resp:
        #         data = await resp.read()
        #
        # print()
        t = time()
        form = FlaskForm()
        mes = form.message.data
        print(mes)
        tasks = []
        for x in range(20):
            # task = asyncio.create_task(dbase.add_message_a("mail", "my_message"))
            # await task
            await dbase.add_message_a("mail", "my_message")
        # await asyncio.gather(*tasks)
        ft = time() - t
        await send_message("async: " + str(ft))
        # print(get_flashed_messages())
    return await render_template('contact.html',
                                 title="Обратная связь")


@app.route("/login", methods=["POST", "GET"])
async def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = dbase.getUserByEmail(form.email.data)
    #     if user and check_password_hash(user["psw"], form.psw.data):
    #         userlogin = UserLogin().create(user)
    #         rm = form.remember.data
    #         login_user(userlogin, remember=rm)
    #         return redirect(request.args.get("next") or url_for("profile"))
    #
    #     else:
    #         flash("Неверная пара логин/пароль", "error")
    #         print("error")
    # return render_template("login2.html", title="Авторизация", menu=dbase.getMenu(), form=form)

    if request.method == "POST":
        user = dbase.get_user_by_mail(request.form["email"])
        if user and check_password_hash(user["psw"], request.form["psw"]):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get("remainme") else False
            login_user(userlogin, remember=rm)
            return redirect(url_for("profile2", alias=current_user.get_id()))

        else:
            await flash("Неверная пара логин/пароль", "error")

    return await render_template("login3.html",
                                 title="Авторизация")


@app.route("/profile")
@login_required
async def profile():
    if current_user.is_authenticated:
        return await redirect(url_for("profile2", alias=current_user.get_id()))
    else:
        return await redirect(url_for("login"))


@app.route(f"/profile/<alias>")
@login_required
async def profile2(alias):
    return await render_template("profile.html",
                                 title="Профиль",
                                 authors=dbase.get_authors())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for("login"))


@app.route("/showall")
@login_required
def showall():
    return render_template("showall.html",
                           posts=dbase.get_all_posts(),
                           authors=dbase.get_authors(),
                           title="Все статьи")


@app.route("/post/<alias>")
@login_required
def show_post(alias):
    post = dbase.get_post(alias)
    if not post:
        abort(404)

    return render_template("post.html",
                           post=post,
                           authors=dbase.get_authors())


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    if request.method == "POST":
        res = dbase.delete_post(request.form["url"])
        if not res:
            flash("Ошибка удаления статьи", category="error")
        else:
            flash("Статья удалена успешно", category="success")
    return render_template("delete_article.html",
                           authors=dbase.get_authors(),
                           posts=dbase.get_all_posts(),
                           title="Удаление статей")


@app.route("/avatar")
@login_required
def get_user_ava():
    img = current_user.get_avatar(app)
    if not img:
        return None

    h = make_response(img)
    h.headers["Content-Type"] = "image/jpg"
    return h


@app.route("/picture/<alias>")
@login_required
def get_picture(alias):
    img = dbase.get_pict(alias)
    if not img:
        print("error")
        return None

    response = make_response(img['file'])
    response.headers["Content-Type"] = "image/jpg"
    return response


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                    return redirect(url_for("profile2", alias=current_user.get_id()))
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for("profile2", alias=current_user.get_id()))


if __name__ == "__main__":
    # asyncio.run(serve(asgi_app, Config()))
    app.run(host="127.0.0.3", debug=True)
