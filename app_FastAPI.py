from fastapi import FastAPI, Request, Form
import sqlite3 as sq
from DataBase import DataBase
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from bot_async import send_message
from time import time


templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

conn = sq.connect("site.db")
conn.row_factory = sq.Row
dbase = DataBase(conn)


@app.post("/")
async def contact(message: str = Form(...)):
    t = time()
    await send_message(message)
    await dbase.add_message_a("current_user.getEmail()", message)
    await send_message(time() - t)


@app.get("/", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse('contact_for_app2.html', {"request": request})


if __name__ == "__main__":
    uvicorn.run(app)
