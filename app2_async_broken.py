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
from bot_async import send_message

DEBUG = True

app = Quart(__name__)

conn = sq.connect("site.db")
conn.row_factory = sq.Row
dbase = DataBase(conn)


@app.route("/contact", methods=["POST", "GET"])
async def contact():
    if request.method == "POST":
        form = await request.form
        t = time()
        for x in range(20):
            await send_message(form["message"])
            await dbase.add_message_a('current_user.getEmail()', form["message"])
        await send_message(time() - t)

    return await render_template('contact.html',
                                 title="Обратная связь")


if __name__ == "__main__":
    # asyncio.run(serve(asgi_app, Config()))
    app.run(host="127.0.0.3", debug=True)
