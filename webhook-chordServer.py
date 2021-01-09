import telepot
import urllib3
from datetime import datetime

from pytz import timezone
from flask import Flask, request

# כדי שיהיה אפשר לגשת מהשרת לטלגרם צריך להשתמש בפרוקסי מובנה
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# מגדיר את הרובוט עפ הטוקן הייחודי שלו ומזדהה מול טלגרם.
bot = telepot.Bot('1223729088:AAHmZyVGZd6hDDjYYfvhuSqk3yWpqk4S57U')

# מבקש מהטלגרם לשלוח את כל העדכונים בתור POST לכתובת הזו.
# יש את הטוקן בסיום (למרות שאפשר לשים כל מספר, או לא לשים כלום) כי זה אתר ציבורי, משמע כל מי שיהיה לו את הלינק הזה יוכל לגשת לרובוט, אז אנחנו שמים כתובת שאף אחד לא יכול לנחש.
bot.setWebhook("https://elikopeleg.pythonanywhere.com/1223729088:AAHmZyVGZd6hDDjYYfvhuSqk3yWpqk4S57U",
               max_connections=100)

# מגדירים משימת Flask חדשה שטטפל בעדכונים
app = Flask(__name__)


# מגדירים למה המשימה תענה: פניות לכתובת הספציפית הזו
@app.route('/1223729088:AAHmZyVGZd6hDDjYYfvhuSqk3yWpqk4S57U', methods=["POST"])
def main_handler():

    # משנה את הקידוד. העדכון מתקבל בקידוד JSON. מחליף את הקידוד להיות dict של python
    # המבנה של ה-update הוא כזה:
    # ה-update מתחלק ל2 חלקים. ID של ה-update וההודעה עצמה.
    # בתוך ההודעה יש את הקטגוריות:
    # ה-message_id שומר את ה-ID של ההודעה.
    # ה-from שומר את הנתונים של המשתמש.
    # ה-chat - שומר את הנתונים של המשתמש ושל הצ'אט (יש כפילויות עם "from" כשמדובר במשתמש פרטי ולא קבוצה).
    # ה-date שומר את הרגע של קבלת (או שליחת) ההודעה.

    update = request.get_json()

    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, "message\n\n\n")
    if "message" in update:
        bot.sendMessage(chat_id, "message\n\n\n" + str(update["message"]["text"]))
        message_handler(update["message"])

    return "OK"


def message_handler(message):
    if message["text"] == "/start":
        start(message)

    chat_id = message["chat"]["id"]
    bot.sendMessage(chat_id, str(datetime.now(timezone("Israel")))[:-13])

    return
