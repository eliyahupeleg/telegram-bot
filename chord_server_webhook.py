import telepot
import urllib3

from flask import Flask, request

# טוקן זיהוי ייחודי לבוט. משמש גם כדי לאבטח את הנתוני כניסה (כמו סיסמא).
BOT_TOKEN = "923788458:AAEU7AkkMCCfemmRRn4uxIjgxhdTn7FIUuM"

# תקייית השורש של הפרוייקט, עם הקבצים הבסיסיים.
ROOT_PATH = "/home/elikopeleg/"

# נתיב לקובץ טקסט ששומר את ה-ID של כל הצ'אטים עם המשתמשים. משמש כדי לשלוח להם הודעה (לדעת מי משתמש) וכדי לספור כמה משתמשים יש.
USERS_PATH = f'{ROOT_PATH}/users.txt'

# מעתיק את רשימת המשתמשים מהקובץ, כדי לבדוק אם מדובר במשתמש חדש.
# !!! צריך למצוא דרך יעילה כדי למנוע re-reading של הנתונים בכל הרצה.
with open(USERS_PATH, 'r') as f:
    USERS = f.read().split('\n')

# כדי שיהיה אפשר לגשת מהשרת לטלגרם צריך להשתמש בפרוקסי מובנה.
# הכתובת של הפרוקסי.
proxy_url = "http://proxy.server:3128"

# מגדיר את הפרוקסי לרובוט.
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# מגדיר את הרובוט עפ הטוקן הייחודי שלו ומזדהה מול טלגרם.
bot = telepot.Bot(BOT_TOKEN)

# מבקש מטלגרם לשלוח את כל העדכונים בתור POST לכתובת הזו.
# הכתובת מורכבת מכתובת הבסיס, פלוס הטוקן. בצורה כזו רק מי שיש לו את הטוקן יכול לגשת לאתר (אי אפשר "לגנוב" את הבוט).
bot.setWebhook(f"https://elikopeleg.pythonanywhere.com/{BOT_TOKEN}")

# מגדירים משימת Flask חדשה שטטפל בעדכונים.
app = Flask(__name__)


# פונקציות לקיצור דרך, וסידור טקסט.
def get_chat_id(update):
    return int(update['message']['chat']['id'])


def get_from_id(update):
    return update['message']['from']['id']


def get_message_text(update):
    return update['message']['text']


# אחרי שהרשימה מתעדכנת ונוסף משתמש, צריך לעדכן את הקובץ שנשמר בצורה סטאטית ולא תלוי בתוכנה.
def write_users():
    # פותח את קובץ המשתמשים לכתיבה.
    with open(USERS_PATH, 'w+') as out:
        # כותבים את כל המשתמשים עם "\n" בין אחד לשני.
        out.write('\n'.join(USERS))
        out.close()


# הפונקציה שמטפלת בהודעות "START/", ומגיבה להן.
# יש 2 אופציות לפקודת START.
# או משתמש חדש (ואז צריך לרשום אותו ולשלוח הודעת ברוך הבא)
# או משתמש שהגיע מהקבוצה, וה START שלו מכיל HASH להודעה המדוייקת שהוא ביקש, ואז צריך לשלוח לו את השיר.
def start_handler(update):
    # רשימה שמכילה את כל ה ID של המשתמשים.
    # משמשת לבדיקה אם מדובר ביוזר רשום או שצריך להוסיף אותו.
    global USERS
    USERS.remove(str(get_from_id(update)))

    # הודעות בקרה - מתכנת
    chat_id = get_chat_id(update)
    bot.sendMessage(chat_id, "start\n" + str(get_from_id(update)))
    bot.sendMessage(chat_id, "users\n" + str(get_from_id(update) in USERS))

    # אם מדובר במשתמש חדש, צריך להוסיף אותו לרשימה ולשמור לקובץ.
    if get_from_id(update) not in USERS:
        # מוסיף את המשתמש לרשימה.
        USERS.append(get_from_id(update))

        # כותב את השינויים לקובץ שלא משתנה אם התוכנה תיפול.
        write_users()

        # מעדכן את מתכנת הבוט במספר המשתמשים.
        bot.sendMessage(386848836, len(USERS))

        # מדובר במשתמש חדש. שולח הודעת "ברוך הבא" מסודרת עם הוראות שימוש.
        bot.sendMessage(chat_id,
                        '''היי, ברוכים הבאים לרובוט האקורדים של 🎶‏ISRACHORD🎶.\n
שילחו שם מלא או חלקי של שיר *או* אמן, וקבלו את האקורדים. כן, כזה פשוט.\n
שלחו שם של אקורד (למשל A#m) כדי לקבל איצבוע לגיטרה.\n
לדיווח: @ADtmr\n
הערוץ שלנו: @tab4us ''')
        return


# הפונקציה שמטפלת בהודעות טקסט, ומגיבה להן.
def message_handler(update):
    pass


# מגדירים למה המשימה תענה: פניות מסוג POST לכתובת הספציפית הזו.
@app.route(f'/{BOT_TOKEN}', methods=["POST"])
def main_handler():
    # המבנה של ה-update הוא כזה:
    # ה-update מתחלק ל2 חלקים. ID של ה-update וההודעה עצמה.
    # בתוך ההודעה יש את הקטגוריות:
    # ה-message_id שומר את ה-ID של ההודעה.
    # ה-from שומר את הנתונים של המשתמש.
    # ה text שומר את תוכן ההודעה.
    # ה-chat - שומר את הנתונים של המשתמש ושל הצ'אט (יש כפילויות עם "from" כשמדובר במשתמש פרטי ולא קבוצה).
    # ה-date שומר את הרגע של קבלת (או שליחת) ההודעה.

    # משנה את הקידוד. העדכון מתקבל בקידוד JSON. מחליף את הקידוד להיות dict של python
    update = request.get_json()

    chat_id = get_chat_id(update)
    bot.sendMessage(chat_id, "message\n" + get_message_text(update))

    # אם אין טקסט בהודעה, מתעלמים ממנה. חסרת משמעות עבור הבוט.
    if "message" not in update:
        bot.sendMessage(chat_id, "no message")
        return "OK"

    # אם זו הודעת "/start" היא לא דורשת תגובה עניינית לטקסט, אלא תחילת עבודה.
    if get_message_text(update) == "/start":
        # שולח את הנתונים (update) לפונקציה שמטפלת  ב START ומסיים את הפעולה.
        start_handler(update)
        #return "OK"

    # אם יש טקסט והוא לא START , צריך לחפש את השיר המתאים וכד' - שולח את הנתונים (update) לפונקציה שמטפלת בהודעות.
    # message_handler(update)

    # שורות בקרה לוודא שהבוט פעיל - הוא מגיב לכל הודעה בהודעה חוזרת כלשהי.
    bot.sendMessage(chat_id, "message\n" + get_message_text(update))
    return "OK"
