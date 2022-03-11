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

from DataBase import DataBase

# from forms import LoginForm
from bot_async import send_message

DEBUG = True

app = Quart(__name__)

conn = sq.connect("site.db")
conn.row_factory = sq.Row
dbase = DataBase(conn)


@app.route("/", methods=["POST", "GET"])
async def contact():
    if request.method == "POST":
        form = await request.form
        await send_message(form["message"])
        t = time()
        for x in range(20):
            await dbase.add_message_a("Quart", form["message"])
        await send_message(time() - t)

    return await render_template('contact_for_app2.html',
                                 title="Обратная связь")


if __name__ == "__main__":
    app.run(host="127.0.0.3", debug=True)
