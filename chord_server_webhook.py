import collections
import glob
import hashlib
import pickle
import re
import threading
import time
from random import randrange

import telepot
import urllib3
from flask import Flask, request
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telepot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

# טוקן זיהוי ייחודי לבוט. משמש גם כדי לאבטח את הנתוני כניסה (כמו סיסמא).
BOT_TOKEN = "999605455:AAFkVPs2jTncditDCzMdGCkatrOfodsVGxE"

# תקייית השורש של הפרוייקט, עם הקבצים הבסיסיים.
ROOT_PATH = "/home/elikopeleg/"

# נתיב לקובץ טקסט ששומר את ה-ID של כל הצ'אטים עם המשתמשים. משמש כדי לשלוח להם הודעה (לדעת מי משתמש) וכדי לספור כמה משתמשים יש.
USERS_PATH = f'{ROOT_PATH}/users.txt'

# נתיב לקבצי האקורדים שהועלו כבר לערוץ (בעיקרון כולם חוץ מאלו שעודכנו למחשב המקומי של המנהל ועוד לא הועלו לערוץ).
UPLOADED_PATH = ROOT_PATH + "/uploaded/"

# רשימת שמות הקבצים (השירים) שקיימים. נשמר פעם אחת מטעמי אופטימזציה. אחרי עדכון, הבוט מורץ מחדש ע"י סקריפט העדכון וכך מעדכן את רשימת הקבצים.
UPLOADED_LIST = glob.glob(f"{UPLOADED_PATH}/*")

# אורך הנתיב נשמר מטעמי אופטימזציה. מחושב רק פה במקום שוב ושוב. משמש כדי לחתוך נתיב לקובץ אקורדים ולקבל רק את השם של הקובץ.
LEN_UPLOADED_PATH = len(UPLOADED_PATH)

# כל האקורדים שיש להם תמונה.
CHORDS_LIBRARY = ["A", "A5", "A6", "A7", "A9", "A_Ab", "A_B", "A_Bb", "A_C#", "A_C", "A_D", "A_E", "A_Eb", "A_F#",
                  "A_F", "A_G", "Aadd9", "Aaug", "Ab", "Ab5", "Ab6", "Ab7", "Ab9", "Ab_A", "Ab_Bb", "Ab_C#", "Ab_C",
                  "Ab_Eb", "Ab_F#", "Ab_G", "Abadd9", "Abaug", "Abdim", "Abdim7", "Abm", "Abm7", "Abm7b5", "Abm9",
                  "Abmaj7", "Absus4", "Adim", "Adim7", "Am", "Am7", "Am7b5", "Am9", "Am_Ab", "Am_B", "Am_Bb", "Am_C",
                  "Am_D", "Am_E", "Am_Eb", "Am_F#", "Am_F", "Am_G", "Amaj7", "Ammaj7", "Asus4", "B", "B5_", "B6", "B7",
                  "B9_2", "B_A", "B_Ab", "Badd9", "Baug", "Bb", "Bb5", "Bb6", "Bb7", "Bb9", "Bb9_2", "Bb_A", "Bb_Ab",
                  "Bb_B", "Bb_Eb", "Bbadd9", "Bbaug", "Bbdim", "Bbdim7", "Bbm", "Bbm7", "Bbm7b5", "Bbm9", "Bbmaj7",
                  "Bbsus4", "Bdim", "Bdim7", "Bm", "Bm7", "Bm7b5", "Bm9", "Bm_A", "Bm_Ab", "Bm_Bb", "Bm_C#", "Bm_C",
                  "Bm_F#", "Bmaj7", "Bsus4", "C#", "C#5", "C#6", "C#7", "C#9_2", "C#add9", "C#aug", "C#dim", "C#dim7",
                  "C#m", "C#m7", "C#m7b5", "C#m9", "C#maj7", "C#mmaj7", "C#sus4", "C", "C5", "C6", "C7", "C9_2", "C_A",
                  "C_B", "C_Bb", "C_C#", "C_G", "Cadd9", "Caug", "Cdim", "Cdim7", "Cm", "Cm7", "Cm7b5", "Cm9", "Cmaj7",
                  "Csus4", "D", "D5", "D6", "D7", "D9", "D_A", "D_B", "D_Bb", "D_C#", "D_C", "D_F#", "Dadd9", "Daug",
                  "Ddim", "Ddim7", "Dm", "Dm7", "Dm7b5", "Dm9", "Dm_A", "Dm_B", "Dm_C", "Dmaj7", "Dsus4", "E", "E5",
                  "E6", "E7", "E9", "E_A", "E_Ab", "E_B", "E_Bb", "E_C#", "E_C", "E_D", "E_Eb", "E_F#", "E_F", "E_G",
                  "Eadd9", "Eaug", "Eb", "Eb5", "Eb6", "Eb7", "Eb9", "Eb9_2", "Ebadd9", "Ebaug", "Ebdim", "Ebdim7",
                  "Ebm", "Ebm7", "Ebm7b5", "Ebm9", "Ebmaj7", "Ebsus4", "Edim", "Edim7", "Em", "Em7", "Em7b5", "Em9",
                  "Em_A", "Em_Ab", "Em_B", "Em_Bb", "Em_C#", "Em_C", "Em_D", "Em_Eb", "Em_F#", "Em_F", "Em_G", "Emaj7",
                  "Esus4", "F#", "F#5", "F#6", "F#7", "F#9", "F#_Ab", "F#_B", "F#_Bb", "F#_C#", "F#_E", "F#_F", "F#_G",
                  "F#add9", "F#aug", "F#dim", "F#dim7", "F#m", "F#m7", "F#m7b5", "F#m9", "F#m_E", "F#m_F", "F#m_G",
                  "F#maj7", "F#sus4", "F", "F5", "F6", "F7", "F9_2", "F_A", "F_Bb", "F_C", "F_D", "F_E", "F_Eb", "F_F#",
                  "F_G", "Fadd9", "Faug", "Fdim", "Fdim7", "Fm", "Fm7", "Fm7b5", "Fm9", "Fm_Ab", "Fm_D", "Fm_E",
                  "Fm_Eb", "Fm_F#", "Fmaj7", "Fsus4", "G", "G5", "G6", "G7", "G9", "G_C", "G_D", "G_E", "G_F#", "G_F",
                  "Gadd9", "Gaug", "Gdim", "Gdim7", "Gm", "Gm7", "Gm7b5", "Gm9", "Gm_Ab", "Gm_D", "Gm_E", "Gm_F",
                  "Gmaj7", "Gsus4"]

# רשימה מיוחדת. כל האקורדים הבסיסיים, אבל קודם אלו עם # או b.
# נועד להמרות. אם הופכים את כל ה F להיות G ורק אז מחפשים F#, יהיה במקום F# G#.
# ברשימה הזו קודם F# מוחלף בA# ורק אז מחפשים F.
CHORDS = ["A#", "Ab", "A", "Bb", "B", "C#", "C", "Db", "D#", "D", "Eb", "E", "F#", "F", "Gb", "G#", "G"]

# משמש להמרת סולמות. האקורדים במרווחים של חצי בדיוק.
LEVELS = [["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
          ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]]

# השירים נשמרים בלי הפתיחה והסיום (שורות מיוחדות עם אמוג'ים וקישור לערוץ או לרובוט).
# כדי לחסוך פתיחה מחדש של הקובץ ששומר את נתוני הפתיחה והסיום (הם קבועים), הפתיחה והסיום של ההודעות נשמרים בקבועים.
fname = f"{ROOT_PATH}/message-intro.txt"
with open(fname, "r") as f:
    # שומר את הפתיחה הקבועה לתוך INTRO
    INTRO = f.read()

fname = f"{ROOT_PATH}/message-end.txt"
with open(fname, "r") as f:
    # בקובץ סיום יש קישור לערוץ של האקורדים. בגלל שהבוט הוא זה ששלח את ההודעה ולא הערוץ, הקישור בסוף משתנה לקישור לבוט ולא לערוץ.
    ENDING = f.read().replace("‏@Tab4us", "‏@Tab4usBot")

# מעתיק את רשימת המשתמשים מהקובץ, כדי לבדוק אם מדובר במשתמש חדש.
# !!! צריך למצוא דרך יעילה כדי למנוע re-reading של הנתונים בכל הרצה.
with open(USERS_PATH, 'r') as f:
    USERS = f.read().split('\n')

# נתיב הקובץ ששומר את הסטטיסטיקה. זהו קובץ ששומר "מילון". המילון מבטא: כמה פעמים חיפשו,על פי מה חיפשו.
STATISTICS_PATH = f'{ROOT_PATH}/statistics.pkl'

# קורא את הסטטיסטיקה לתוך המילון. אם הקובץ לא קיים או ריק, יוצר אותו.
try:

    # קורא את הנתונים מהקובץ לתוך statistics.
    with open(STATISTICS_PATH, 'rb') as fp:
        statistics = pickle.load(fp)

# אם האורך של הקובץ יהיה 0, תוחזר שגיאה EOFError.
# אם הקובץ לא קיים, תוחזר שגיאה FileNotFoundError.
# בכל מקרה, הפתרון הוא ליצור את הקובץ מחדש.
except (FileNotFoundError, EOFError) as e:

    # יוצר את הקובץ, ומכניס לתוכו מילון ריק.
    with open(STATISTICS_PATH, 'wb') as fp:

        # מכניס מילון ריק({}) לתוך הקובץ, כדי שלא יהיה עם אורך 0.
        pickle.dump({}, fp, protocol=pickle.HIGHEST_PROTOCOL)

        # יוצר את המילון של הסטטיסטיקה (משתנה מקומי statistics) ריק.
        statistics = collections.OrderedDict()

# דגל שבודק האם הקישור בקבוצה שומש. אם כן, הבוט ימחק את ההודעות.
# נבדק פעם ב5 דקות. אחרי 3 שעות יימחק בכל מקרה (למנוע עבודה מיותרת של הבוט)
flags = {}

# התוצאות חיפוש של ההודעה בקבוצה.
# לדוגמא - משתמש שלח בקבוצה "אקורדים לאייל גולן", בתוך ה-saved יישמרו התוצאות לחיפוש "אייל גולן", כך שהן יוצגו למשתמש מייד לאחר הלחיצה על הקישור לרובוט.
saved = {}

# המזהה הייחודי של ההודעות בקבוצה.
# המזהה של הודעת בקשת אקורדים ותגובת הבוט נשמר כדי למחוק את ההודעות אחרי שהקישור נלחץ (מונע הספמה ע"י הבוט).
to_delete = {}

# כדי שיהיה אפשר לגשת מהשרת לטלגרם צריך להשתמש בפרוקסי מובנה.
# הכתובת של הפרוקסי.
PROXY_URL = "http://proxy.server:3128"

# מגדיר את הפרוקסי לרובוט.
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=PROXY_URL, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=PROXY_URL, num_pools=1, maxsize=1, retries=False, timeout=30))

# מגדיר את הרובוט עפ הטוקן הייחודי שלו ומזדהה מול טלגרם.
bot = telepot.Bot(BOT_TOKEN)

# מבקש מטלגרם לשלוח את כל העדכונים בתור POST לכתובת הזו.
# הכתובת מורכבת מכתובת הבסיס, פלוס הטוקן. בצורה כזו רק מי שיש לו את הטוקן יכול לגשת לאתר (אי אפשר "לגנוב" את הבוט).
bot.setWebhook(f"https://elikopeleg.pythonanywhere.com/{BOT_TOKEN}")

# מגדירים משימת Flask חדשה שטטפל בעדכונים.
app = Flask(__name__)

# "מקלדת" עם אופציה אחת - שלח לי שיר אקראי.
random_keyboard = ReplyKeyboardMarkup(keyboard=[['שיר אקראי']], resize_keyboard=True, one_time_keyboard=True)


# מקלדת שנשלחת לאחר לחיצה על "+" במקלדת הקודמת. מראה את אופציות השינוי.
# השימוש בפונקציה נועד כדי להכניס את האינדקס של השיר (איפה הוא ממוקם בתוך uploaded_list - ובהמרה יהיה אפשר לשלוף אותו בקלות.
def keyboard_plus(index):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="+1", callback_data=f'+1|{index}'),
                                                  InlineKeyboardButton(text="+2", callback_data=f'+2|{index}'),
                                                  InlineKeyboardButton(text="+3", callback_data=f'+3|{index}')],
                                                 [InlineKeyboardButton(text="+0.5", callback_data=f'+0.5|{index}'),
                                                  InlineKeyboardButton(text="+1.5", callback_data=f'+1.5|{index}'),
                                                  InlineKeyboardButton(text="+2.5", callback_data=f'+2.5|{index}'),
                                                  InlineKeyboardButton(text="+3.5", callback_data=f'+3.5|{index}')]
                                                 ])


# מקלדת שנשלחת לאחר לחיצה על "-" במקלדת הקודמת. מראה את אופציות השינוי.
# השימוש בפונקציה נועד כדי להכניס את האינדקס של השיר (איפה הוא ממוקם בתוך uploaded_list - ובהמרה יהיה אפשר לשלוף אותו בקלות.
def keyboard_minus(index):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="-1", callback_data=f'-1|{index}'),
                                                  InlineKeyboardButton(text="-2", callback_data=f'-2|{index}'),
                                                  InlineKeyboardButton(text="-3", callback_data=f'-3|{index}')],
                                                 [InlineKeyboardButton(text="-0.5", callback_data=f'-0.5|{index}'),
                                                  InlineKeyboardButton(text="-1.5", callback_data=f'-1.5|{index}'),
                                                  InlineKeyboardButton(text="-2.5", callback_data=f'-2.5|{index}'),
                                                  InlineKeyboardButton(text="-3.5", callback_data=f'-3.5|{index}')]
                                                 ])


# מקלדת המרות האקורדים. מאפשרת להעלות או להוריד סולם.
# השימוש בפונקציה נועד כדי להכניס את האינדקס של השיר (איפה הוא ממוקם בתוך uploaded_list) - ובהמרה יהיה אפשר לשלוף אותו בקלות.
def default_keyboard(index, easy_key):
    # אם הסולם הקל לא שלילי, צריך להוסיף לפניו סימן של "+" כדי להתאים לפורמט.
    if float(easy_key) >= 0:
        easy_key = f"+{easy_key}"

    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="+", callback_data=f"+|{index}"),
                          InlineKeyboardButton(text="-", callback_data=f"-|{index}")],
                         [InlineKeyboardButton(text="גרסה קלה", callback_data=f"{easy_key}|{index}")]
                         ])


# הפונקציה בודקת אם השם של הזמר או השיר מורכב רק מאותיות גדולות.
# אם כן, צריך לדלג על פונקציית ה title.
def is_upper(i):
    # אם השם מורכב רק מאותיות גדולות, הוא מוחזר כמו שהוא.
    if i.isupper():
        return i
    # אם לא, מסדרים את השם עם title.
    else:
        return i.title()


# מקבל קישור מלא לקובץ בתקיית uploaded, ומסיר ממנו את הסיומת ".TXT" ואת הקידומת של "\home\elikoeleg" וכו'.
def replace_to_filename(i):
    return i[LEN_UPLOADED_PATH:-4]


# הפונקציה משמשת כדי להגדיר בעזרתה את רשימת האמנים.
# היא מקבלת נתיב מלא לקובץ, ומחזירה את שם האמן.
# השימוש בפונקציה נועד עבור map - חסכוני יותר מלולאת for.
def get_artist(name):
    return replace_to_filename(name).split(" - ")[0]


# שומר רשימה של כל האמנים.
# השימוש ב map נועד כדי לחסוך לולאת for (יעיל יותר).
ARTISTS_LIST = list(dict.fromkeys(list(map(get_artist, UPLOADED_LIST))))


# פונקציות לקיצור דרך, וסידור טקסט.
# מנסה לשלוף נתונים דרך message, אם לא מצליח מנסה דרך callback_query (מאפשר שימוש באותה פונקציה בשני המקרים).
def get_message_chat_id(update):
    return update['message']['chat']['id']


def get_message_id(update):
    try:
        return update['message']['message_id']
    except KeyError:
        return update['callback_query']['id']


def get_message_from_id(update):
    try:
        return update['message']['from']['id']
    except KeyError:
        return update['callback_query']['from']['id']


def get_message_text(update):
    try:
        return update['message']['text']
    except KeyError:
        return update['callback_query']['data']


# הפונקציה רצה ברקע, ובודקת מתי הלינק שנשלח בקבוצה נלחץ.
# כשהלינק נלחץ, מוחקת את ההודעות שהבוט שלח בקבוצה, ואת ההודעות להן הוא הגיב.
def delete(time_hash):
    # אם אחרי 3 שעות (180 דק', 36*300 שניות) הלינק עדיין לא נלחץ, מוחקים  את ההודעות בכל זאת.
    for i in range(36):
        # אם הלינק נלחץ, צא מהלולאה.
        if flags[time_hash]:
            break
        # אם הלינק לא נלחץ, חכה 5 דקות ובדוק שוב.
        time.sleep(300)

    # מוחק את 2 ההודעות מהקבוצה - הודעת הבקשה והודעת התגובה.
    # בתוך to_delete יש את הID של ההודעה.
    bot.deleteMessage(to_delete[time_hash])
    bot.deleteMessage(to_delete[time_hash] + 1)


# יוצר ערך HASH באורך מוגבל מהטקסט הנתון.
def h1(data):
    return hashlib.md5(data).hexdigest()[:9]


# הפונקציה שולחת הודעה אחת (message) לכל משתמשי הבוט.
# הפונקציה גם מסירה את כל המשתמשים שחסמו את הבוט \ לא פעילים מ USERS.
# הדרך היחידה (הידועה) לבדוק מי מהמהתמשים אכן פעיל היא לנסות לשלוח להם הודעה.
def msg(message):
    # עובר על כל המשתמשים.
    for USER in USERS:

        # אם המשתמש חסם את הבוט, הפעולה תחזיר שגיאה (משתמש לא קיים \ הבוט חסום וכד'
        try:
            # מנסה לשלוח את ההודעה למשתמש.
            bot.sendMessage(chat_id=USER, text=message)

        # אם יש שגיאה, המשתמש לא רלוונטי.
        except Exception:

            # מסירים את המשתמש מהרשימה.
            USERS.remove(USER)
    # בגלל שהרשימה השתנתה, צריך לעדכן את הקובץ.
    write_users()


# אחרי שהרשימה מתעדכנת ונוסף משתמש, צריך לעדכן את הקובץ שנשמר בצורה סטאטית ולא תלוי בתוכנה.
def write_users():
    # פותח את קובץ המשתמשים לכתיבה.
    with open(USERS_PATH, 'w+') as out:
        # כותבים את כל המשתמשים עם "\n" בין אחד לשני.
        out.write('\n'.join(USERS))
        out.close()


# שולח שיר אקראי למשתמש.
def send_random(update):
    # שולף שם של שיר בצורה אקראית.
    song_name = UPLOADED_LIST[randrange(len(UPLOADED_LIST))]

    # שולח את ההודעה בצורה מסודרת, כאילו זו תוצאת חיפוש יחידה.
    build_message([song_name], update)


# ממיר את השיר לסולם חדש
def new_key(index, key):
    # אם ממירים ב1.5, זה בעצם 3 חצאים ללמעלה.
    # ההמרה לפי חצאים כי יותר קל להשתמש ב2 מ0.5
    half_key = int(float(key) * 2)

    # פותח את הקובץ המקורי לקריאה.
    with open(UPLOADED_LIST[index], "r") as f:

        # קורא את השיר לתוך data.
        data = f.read()

        # אחד דיאזים אחד במולים
        for chord in CHORDS:

            if chord in LEVELS[0]:
                chord_index = LEVELS[0].index(chord)
                level = LEVELS[0]
            else:
                chord_index = LEVELS[1].index(chord)
                level = LEVELS[1]

            new_chord_index = half_key + chord_index
            len_level = len(level)

            if new_chord_index >= len_level:
                new_chord_index -= len_level

            if new_chord_index < 0:
                new_chord_index += len_level

            # מחליפים לאקורד הבא. מוסיפים | כדי לא להמיר את אותו אחד פעמיים.
            # //אם יש אקורד מ2 סוגים (לדוג' #G וגם G) האות תקבל שתי המרות - אחת גם מהאקורד המקורי, ולכן צריך רשימה מיוחדת - שבה האקורדים המיוחדים מופיעים לפני הרגילים, וכך F# מוחלפים לפני שהגענו ל F.
            data = re.sub("\[" + chord, '[|' + str(level[new_chord_index]), data)

        # אם השפה היא עברית, צריך להוסיף סימן מיוחד אחרי הכוכביות שימנע מהן להתהפך בכיוון.
        if data.split("\n")[5] == "HE":
            data = data.replace("#]", "#ᶥ")

        # מוחקים את כל הסוגריים שמסמנים אקורד מהטקסט.
        data = data.replace("[|", "").replace("[", "").replace("]", "")

        # מחלקים את הטקסט לשורות.
        data = data.split('\n')

        # מעתיק את הפתיחה הקבועה לעותק מקומי, כדי לשנות אותו בלי לפתוח מחדש את הצורך.
        intro = INTRO

        # מכניס את שם השיר למקום המתאים בפתיחה, מסיר תווים מיוחדים שלא קיימים בשם הקובץ.
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + f"   \n{data[0]}")
        # מכניס את שם הזמר למקום המתאים בפתיחה, מסיר תווים מיוחדים שלא קיימים בשם הקובץ.
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + f"   \n{data[1]}")

        # אם בשורה השלישית כתוב "המערכת" ולא "גולש"..
        if "המערכת" == data[2]:
            # מוסיפים לשיר סימון של גרסה רשמית.
            intro = intro.replace("version", "⭐️ גרסה רשמית ⭐")
        # אם בשורה השלישית כתוב "גולש" ולא "המערכת""..
        else:
            # מוחקים את המיקום של הגרסה רשמית.
            intro = intro.replace("version", "")

        # השורה הרביעית בשיר מכילה את המספר של הגרסה הקלה - כמה צריך להזיז כדי להגיע אליה.
        # לא מכניסים את זה לפתיחה כי למשתמש זה לא יעיל, אלא מעבירים לפונקציה והיא מכניסה את זה לנתונים של כפתור "גרסה קלה".
        easy_key = data[3]

        # בשורה החמישית בשיר כתוב איפה לשים קאפו. אם הקאפו בשריג 0..
        if "0" == data[4]:
            # מסירים את הסימון של הקאפו. לא צריך לרשום 0.
            intro = intro.replace("capo", "")
        # אם הקאפו בשריג אחר..
        else:
            # רושמים במיקום המתאים איפה לשים את הקאפו.
            intro = intro.replace("capo", f"קאפו בשריג {data[4]}")

        # המידע בתחילת השיר (שמות, קאפו, גרסה קלה וכד') לא נשלח, רק מ - data[5] ואילך.
        # ולכן מוסיפים ל- data[5] את כל הפתיח הרשמי, והשיר נשלח משם ואילך.
        data[5] = intro

        # מוסיפים את הסיומת הקבועה (אין בה משתנים בכלל).
        data.append(ENDING)

    # מנקים את סימני הבקרה
    return data[5:], easy_key


# הפונקציה שמטפלת בהודעות "START/", ומגיבה להן.
# יש 2 אופציות לפקודת START.
# או משתמש חדש (ואז צריך לרשום אותו ולשלוח הודעת ברוך הבא)
# או משתמש שהגיע מהקבוצה, וה START שלו מכיל HASH להודעה המדוייקת שהוא ביקש, ואז צריך לשלוח לו את השיר.
def start_handler(update):
    # רשימה שמכילה את כל ה ID של המשתמשים.
    # משמשת לבדיקה אם מדובר ביוזר רשום או שצריך להוסיף אותו.
    global USERS

    # הודעות בקרה - מתכנת
    chat_id = get_message_chat_id(update)
    bot.sendMessage(chat_id=chat_id, text="start\n" + str(get_message_from_id(update)))
    bot.sendMessage(chat_id=chat_id, text="users\n" + str(get_message_from_id(update) in USERS))

    # אם מדובר במשתמש חדש, צריך להוסיף אותו לרשימה ולשמור לקובץ.
    if get_message_from_id(update) not in USERS:
        # מוסיף את המשתמש לרשימה.
        USERS.append(get_message_from_id(update))

        # כותב את השינויים לקובץ שלא ישתנה אם התוכנה תיפול.
        write_users()

        # מעדכן את מתכנת הבוט במספר המשתמשים.
        bot.sendMessage(chat_id=386848836, text=len(USERS))

        # מדובר במשתמש חדש. שולח הודעת "ברוך הבא" מסודרת עם הוראות שימוש.
        bot.sendMessage(chat_id=chat_id, text=
        '''היי, ברוכים הבאים לרובוט האקורדים של 🎶‏ISRACHORD🎶.\n
שילחו שם מלא או חלקי של שיר *או* אמן, וקבלו את האקורדים. כן, כזה פשוט.\n
שלחו שם של אקורד (למשל A#m) כדי לקבל איצבוע לגיטרה.\n
לדיווח: @ADtmr\n
הערוץ שלנו: @tab4us ''')
        return


# הפונקציה מטפלת במקרים של START עם HASH - מישהו קיבל קישור לתוצאות מהרובוט בקבוצה, ועכשיו הוא מבקש את התוצאות בהודעה פרטית..
def start_hash_handler(update):
    # מחלץ את הID של המשתמש ואת ה HASH שנוצר אוטומטית (ע"פ הזמן בו נשלחה ההודעה).
    time_hash, chat_id = get_message_text(update).replace("/start ", "").split("andand")

    # משנה את הדגל של ה HASH ל TRUE - מדווח שהקישור נלחץ, וכך התוכנה יודעת למחוק אותו.
    flags[time_hash] = True

    # שולף את התוצאות (מוצא ע"פ ה HASH) ושומר אותן ל files כאילו שזה חיפוש שנעשה עכשיו בפרטי.
    files = saved[time_hash]

    # מפעיל את הפונקציה ששולחת את ההודעה עם התוצאות.
    build_message(files, update)


# הפונקציה מקבלת תוצאות חיפוש (רשימת שמות קבצים) ומחזירה הודעה מתאימה / שולחת את התוצאה (אם יש בודדת)
def build_message(files, update):
    # נשמר למנוע חיפוש חוזר:
    #
    # מספר התוצאות (כמות הקבצים ברשימה)
    len_files = len(files)
    # הטקסט של ההודעה המקורית.
    message = get_message_text(update)
    # הID של ה CHAT.
    chat_id = get_message_chat_id(update)

    # אם יש תוצאות אבל החיפוש נעשה בקבוצה ולא בצ'אט פרטי..
    if chat_id < 0 < len_files:

        # אם יש את המילה "אקורדים" בהודעה, מדובר בחיפוש ולא סתם הודעה שרצה עם תוצאות במקרה.
        if "אקורדים" in message:
            # יוצר HASH ע"י השעה המדוייקת שנועד לשמור ולזהות את המקרה הספציפי הזה.
            time_hash = h1(str(time.time()).encode())

            # שומר לתוך מילון את תוצאות, המפתח הוא ה HASH (כשהמשתמש יחזור, נוכל לשלוף את התוצאות באמצעות ה HASH בלבד).
            saved[time_hash] = files

            # יוצר מקלדת מיוחדת, שמובילה לתוך הבוט.
            # הקישור המיוחד מראה כפתור "התחל" גם למשתמשים שהתחילו כבר, ומזין ערך מיוחד ל start_hash_handler.
            replay_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    # ההודעה בקבוצה תהיה "אקורדים עבור ___", ועל הכתפור מתחת יהיה כתוב "לחץ פה".
                    text="לחץ פה",

                    # לחיצה תוביל לקישור - פותח את הבוט, יוצר התחלה חדשה עם ה time_hash המיוחד - וכך ה start_hash_handler יודע איזה קבצים להציג.
                    url=f"https://t.me/Tab4usBot?start={str(time_hash)}andand{str(chat_id)}"
                )
            ]])

            # מסדר את כל הטקסט כדי לרשום את השם של השיר בצורה מדוייקת בהודעה החוזרת.
            data = message.replace("?", "")
            data = data.replace("לשיר ", "ל")
            data = data[data.index(" ל") + 2:]

            # שולח את ההודעה עם המקלדת.
            bot.sendMessage(text=f'אקורדים ל "{data.replace("אקורדים ", "")}"', chat_id=chat_id,
                            reply_markup=replay_markup)

            # שומר לתוך רשימה מיוחדת איזו הודעה צריך למחוק ומאיפה.
            to_delete[time_hash] = [int(get_message_id(update))]

            # דגל שבודק אם ההודעה נמחקה.
            flags[time_hash] = False

            # יוצר לולאה שרצה ברקע ומוחקת את ההודעות בקבוצה אחרי שהמשתמש לחץ על הלינק (מונע הספמה)
            threading.Thread(target=delete, args=time_hash).start()
        return

    # אם אין תוצאות..
    if len_files == 0:

        # אם לא מדובר בקבוצה, שולחים הודעה אוטומטית שמדווחת על 0 תוצאות. בקבוצות לרוב ההודעות לא יהיו תוצאות, ולכן לא שולחים כלום.
        if chat_id > 0:
            # שולח למשתמש שלא נמצאו תוצאות.
            bot.sendMessage(chat_id=chat_id, text="פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!",
                            reply_markup=ReplyKeyboardRemove())
        return

    # אם יש כמה תוצאות (וזו לא קבוצה כי קבוצה שללנו למעלה)..
    if len_files > 1:

        # מכין מקלדת עם כל התוצאות.
        keyboard_values = sorted(list(map(replace_to_filename, files)))

        # הטקסט בהודעה הוא "בחר.."
        text = "בחר.."

        # אם יש מעל 100 תוצאות (וכפתור חזור אחד) מצמצמים ל100 תוצאות הראשונות - והמשתמש יצטרך לדייק את החיפוש שלו.
        if len(files) > 100:
            # חותכים את המקלדת ומשאירים רק את ה178 ערכים הראשונים.
            keyboard_values = keyboard_values[:100]

            # מדווחים למשתמש על עודף תוצאות.
            text = "החיפוש שלך כולל יותר מידי תוצאות, אז צמצמנו ל100 הראשונים.."

        # מוסיפים לתוצאות כפתור "חזור".
        keyboard_values.append("חזור")

        keyboard = ReplyKeyboardMarkup(keyboard=[[i] for i in keyboard_values], resize_keyboard=True,
                                       one_time_keyboard=True)

        print(type(keyboard))
        # שולחים למשתמש את ההודעה עם מקלדת התוצאות.
        bot.sendMessage(chat_id=chat_id, text=text, reply_markup=keyboard)
        return

    # אם מגיעים לפה, המשמעות היא שיר אחד בצ'אט פרטי.

    # מכניסים את הנתיב לשיר למשתנה fpath.
    fpath = files[0]

    # פותחים את הקובץ של השיר לקריאה.
    with open(fpath, "r") as song_file:

        # קוראים את כל הקובץ לתוך data.
        data = song_file.read()

        # אם השפה היא עברית, צריך להוסיף סימן מיוחד אחרי הכוכביות שימנע מהן להתהפך בכיוון.
        if data.split("\n")[5] == "HE":
            data = data.replace("#]", "#ᶥ")

        # מוחקים את כל הסוגריים שמסמנים אקורד מהטקסט.
        data = data.replace("[", "").replace("]", "")

        # מחלקים את הטקסט לשורות.
        data = data.split('\n')

        # מעתיק את הפתיחה הקבועה לעותק מקומי, כדי לשנות אותו בלי לפתוח מחדש את הצורך.
        intro = INTRO

        # מכניס את שם השיר למקום המתאים בפתיחה, מסיר תווים מיוחדים שלא קיימים בשם הקובץ.
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + f"   \n{data[0]}")
        # מכניס את שם הזמר למקום המתאים בפתיחה, מסיר תווים מיוחדים שלא קיימים בשם הקובץ.
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + f"   \n{data[1]}")

        # אם בשורה השלישית כתוב "המערכת" ולא "גולש"..
        if "המערכת" == data[2]:
            # מוסיפים לשיר סימון של גרסה רשמית.
            intro = intro.replace("version", "⭐️ גרסה רשמית ⭐")
        # אם בשורה השלישית כתוב "גולש" ולא "המערכת""..
        else:
            # מוחקים את המיקום של הגרסה רשמית.
            intro = intro.replace("version", "")

        # השורה הרביעית בשיר מכילה את המספר של הגרסה הקלה - כמה צריך להזיז כדי להגיע אליה.
        # לא מכניסים את זה לפתיחה כי למשתמש זה לא יעיל, אלא מעבירים לפונקציה והיא מכניסה את זה לנתונים של כפתור "גרסה קלה".
        easy_key = data[3]

        # בשורה החמישית בשיר כתוב איפה לשים קאפו. אם הקאפו בשריג 0..
        if "0" == data[4]:
            # מסירים את הסימון של הקאפו. לא צריך לרשום 0.
            intro = intro.replace("capo", "")
        # אם הקאפו בשריג אחר..
        else:
            # רושמים במיקום המתאים איפה לשים את הקאפו.
            intro = intro.replace("capo", f"קאפו בשריג {data[4]}")

        # המידע בתחילת השיר (שמות, קאפו, גרסה קלה וכד') לא נשלח, רק מ - data[5] ואילך.
        # ולכן מוסיפים ל- data[5] את כל הפתיח הרשמי, והשיר נשלח משם ואילך.
        data[5] = intro

        # מוסיפים את הסיומת הקבועה (אין בה משתנים בכלל).
        data.append(ENDING)

        # שולחים את השיר למשתמש בעזרת הפונקציה הייעודית.
        send_data(data[5:], update, True, False, None, easy_key, UPLOADED_LIST.index(fpath))


# הפונקציה שולחת את הודעה למשתמש בצורה מסודרת.
def send_data(data, update, is_song=False, is_converted=False, keyboard=None, easy_key=None, file_index=None):
    # יוצר את המקלדת כל פעם מחדש, כי הערך של "גרסה קלה" צריך להיות ב callback_data.
    if keyboard is None:
        # אם לא ביקשו מקלדת ספציפית, יוצר את המקלדת הרגילה עם הערכים של מספר השיר והגרסה קלה שלו.
        keyboard = default_keyboard(file_index, easy_key)

    # רשימה ריקה לתוכה תיכנס ההודעה, חתוכה לפי הגודל של הודעה מקסימלית ע"פ טלגרם (עד 4096 תווים להודעה).
    song = [""]

    # מונה - לכמה חלקים התחלקה ההודעה.
    counter = 0

    # עובר על השיר שורה שורה, מוסיף כל פעם את השורה עד שהגודל חורג, ואז פותח חלק שני.
    for line in data:

        # שומר את השורה הנוכחית יחד עם השורות שנשמרו כבר בחתיכה הנוכחית של song לתוך test כדי לבדוק אם אחרי ההוספה הגודל יחרוג.
        test = f"{song[counter]}%0A{line}{data[-1]}"

        # אם אחרי ההוספה הגודל חורג מ4096 בתים..
        if len(test) >= 4096:
            # מקדם את המונה ב1 כי מוסיפים חלק לשיר.
            counter += 1
            # פותח חתיכה חדשה ב song עבור המשך השיר.
            song.append("")

        # אחרי שנבדק לאיזו חתיכה צריכה להיכנס השורה הנוכחית, מוסיפים את השורה ל song[counter] (זו החתיכה המתאימה).
        if is_song:
            # אם מדובר בשיר, צריך להוסיף "אנטר" בין שורה לשורה.
            song[counter] += f"\n{line}"
        else:
            # אם לא מדובר בשיר, פשוט מוסיפים את השורה כמו שהיא.
            song[counter] += f"{line}"

    # עובר חתיכה חתיכה ושולח למשתמש.
    for part in song:
        # אם זו ההודעה האחרונה, מוסיף את המקלדת.
        if part == song[-1]:
            reply_markup = keyboard

        else:
            # אם זו לא ההודעה האחרונה, מסיר את המקלדת.
            reply_markup = ReplyKeyboardRemove()

        # ה -  ID של קבוצה תמיד יהיה במינוס.
        if get_message_chat_id(update) < 0:
            # אם זו הודעה בקבוצה, מסיר את המקלדת.
            reply_markup = ReplyKeyboardRemove()

        # שולח את ההודעה המסודרת למשתמש.
        bot.sendMessage(chat_id=get_message_chat_id(update), text=part.replace(u'\xa0', u' '),
                        reply_markup=reply_markup)

    # סמיילי יד מצביע על ההודעה הראשונה כדי לדפדף אליה בקלות.
    # אם מדובר בהמרה, צריך לרדת עוד הודעה אחת למטה (ההודעה שהומרה, הודעת האצבע שלה, ואז ההודעה שנשלחה עכשיו).
    bot.sendMessage(chat_id=get_message_chat_id(update), text=u'\u261d', reply_markup=ReplyKeyboardRemove(),
                    reply_to_message_id=get_message_id(update) + 1 + int(is_converted))


# הפונקציה מקבלת טקסט, ומחפשת שמות של שירים שמכילים את הטקסט המבוקש.
def search_songs(update):
    # ההודעה עצמה שהמשתמש שלח.
    data = get_message_text(update)

    # מגדירים פעם אחת כדי לחסוך שימוש חוזר בפונקציה.
    chat_id = get_message_chat_id(update)

    # אם מדובר בקבוצה, צריך להוריד חלקים מיותרים.
    # את "אקורדים" וכד' כבר הסרנו בפונקציה שקולטת את ההודעה.
    if chat_id < 0:

        # בסוף בקשת שיר הרבה פעמים שמים סימן שאלה מיותר.
        data = data.replace("?", "")

        # לפעמים בקבוצה כותבים "אקורדים לשיר..."
        # הופכים את זה ל "אקורדים ל...." כדי שהחיתוך בשורה הבאה יהיה מדוייק.
        data = data.replace("לשיר ", "ל")

        # חותכים את תחילת ההודעה (מיותר. לדוגמא "יש למישהו אקורדים ל....")
        data = data[data.index(" ל") + 2:]

    # אם ההודעה נכתבה ע"י המתכנת, היא לא נכנסת לסטטיסטיקות.
    elif chat_id != 386848836:

        # אם הערך כבר נמצא במילון וחופש בעבר..
        try:

            # מוסיפים 1 למונה החיפושים שלו.
            statistics[data] += 1

        # אם זה החיפוש הראשון של הערך..
        except KeyError:

            # יוצרים את הערך במילון, עם המונה על הערך 1.
            statistics[data] = 1

        # בכל מקרה בסוף הטיפול בסטטיסטיקות צריך לעדכן את הקובץ.
        finally:

            # פותח את הקובץ ששומר את הסטטיסטיקות..
            with open(STATISTICS_PATH, 'wb') as statistics_file:

                # שומר את הנתונים החדשים לקובץ.
                pickle.dump(statistics, statistics_file)

    # בסוף רשימת שירים יש למשתמש כפתור "חזור".
    if data == "חזור":
        # אם המשתמש לחץ "חזור" הבוט שולח לו הודעה "חוזר" ומשנה את המקלדת.
        bot.sendMessage(text="חוזר..", chat_id=chat_id, reply_markup=random_keyboard)
        return "OK"

    # רשימה שלתוכה יישמרו תוצאות החיפוש.
    files = []

    # חותך את data ל2 חלקים - שם השיר ושם הזמר.
    # מעביר אותם דרך is_upper.
    # אם השם לא מורכב רק מאותיות גדולות, הוא עובר title כדי לחזור לאיות הנכון.
    data = " - ".join(list(map(is_upper, data.split(' - '))))

    folder = f'{ROOT_PATH}/uploaded/*'

    try:
        data = data.replace(data[data.index("'"):data.index("'") + 2],
                            data[data.index("'"):data.index("'") + 2].lower())
    except ValueError:
        pass

    glb = UPLOADED_LIST

    full_name = f"{folder[:-1]}{data}.txt"

    if full_name in glb:
        files = [glb[glb.index(full_name)]]
        build_message(files, update)
        return

    for fpath in glb:

        # some songs names have "and" or "the" in there names, what goes bad with "search.title()" (returns "And" or "The").
        # so if the song is not in the songs list, it'll be when the file name will be titled.
        if fpath.title() == full_name.title():
            files = [fpath]
            build_message(files, update)
            return
        if data in fpath:
            files.append(fpath)

    build_message(files, update)


# הפונקציה מטפלת בלחיצות כפתור של inline (המרת סולם).
def inline_button_handler(update):
    # שולף את הטקסט של הכפתור - callback_data.
    clicked = get_message_text(update)

    # מחלץ את האינדקס של השיר - איפה הוא ממוקם ב uploaded_list. משמש להמרות עצמן - שולפים את השיר מהקובץ המקורי, יותר נח להתעסק איתו.
    index = clicked.split("|")[1]

    # התו הראשון הוא סימן "+" או "-". אם התו השני הוא "|" אין מספר, נלחץ כפתור "+" או "-", מה שאומר שצריך לעדכן את המקלדת.
    if clicked[1] == "|":

        # אם נלחץ כפתור "+"..
        if clicked[0] == "+":

            # עורכים את המקלדת של ההודעה המתאימה - למקלדת המרה עם כפתורי ה"+".
            bot.editMessageReplyMarkup(chat_id=get_message_from_id(update), message_id=get_message_id(update),
                                       reply_markup=keyboard_plus(index))
            return

        # אם נלחץ כפתור "+"..
        elif clicked[0] == "-":

            # עורכים את המקלדת של ההודעה המתאימה - למקלדת המרה עם כפתורי ה"+".
            bot.editMessageReplyMarkup(chat_id=get_message_from_id(update), message_id=get_message_id(update),
                                       reply_markup=keyboard_minus(index))
            return

    # אם הכפתור הוא בקשה להמרה, ממיר את השיר. שומר שוב את easy_key כי צריך אותו ל send_data כדי ליצור את המקלדת הרגילה.
    data, easy_key = new_key(int(index), clicked.split("|")[0])

    # שולח את השיר החדש אחרי ההמרה למשתמש.
    send_data(data, update["callback_query"], True, True, None, easy_key, index)

    # מדווח לטלגרם שהבקשה טופלה בהצלחה.
    bot.answerCallbackQuery(get_message_id(update))


# הפונקציה שמטפלת בהודעות טקסט, ומגיבה להן.
def message_handler(update):
    # משמש כדי להכניס את החיפוש לסטטיסטיקה.
    global statistics

    # הטקסט של ההודעה.
    message = get_message_text(update)

    # ה ID של הצ'אט (לא של המשתמש).
    chat_id = get_message_chat_id(update)

    # אם המשתמש לא ברשימה והוא שלח הודעה, צריך להוסיף אותו.
    if str(get_message_from_id(update)) not in USERS:
        # מוסיף את המשתמש לרשימה.
        USERS.append(str(get_message_from_id(update)))

        # כותב את השינויים לקובץ שלא ישתנה אם התוכנה תיפול.
        write_users()

        # מעדכן את מתכנת הבוט במספר המשתמשים.
        bot.sendMessage(text=len(USERS), chat_id=386848836)

    # אם מדובר בקבוצה, ה ID תמיד יהיה קטן מ0 (מתחיל במינוס, לדוגמא "-43452543642345" - לעומת משתמש שיהיה חיובי (לדוגמא, "6453245734").
    if chat_id < 0:

        # אם כתוב "אקורד" ולא "אקורדים", הוא רוצה תמונה של אקורד.
        # מוחקים את המילה "אקורד" וממשיכים כמו בשיחה רגילה (הבוט ימצא את התמונה וישלח בקבוצה).
        if "אקורד " in message:
            message = message.replace("אקורד ", "")

        # אם אין את המילה "אקורד", בודקים אם יש "אקורדים".
        else:

            # אם יש בהודעה את המילה "אקורדים", הוא מחפש אקורדים לשיר. שולחים את הטקסט שלו לחיפוש.
            if "אקורדים" in message:
                search_songs(update)
                return

            # אם אין "אקורדים" ואין "אקורד", זו סתם הודעה בקבוצה. מתעלמים ממנה.
            else:
                return

    # אם הID הוא של המתכנת, יש פקודות מיוחדות שהוא יכול להריץ.
    if chat_id == 386848836:

        # שולח את רשימת הסטטיסטיקה, לערכים שחופשו החל מפעמיים (יותר מידי ערכים חופשו פעם אחת)
        if message.title() == "St":
            # ממיין מחדש את statistics לקראת שליחה.
            statistics = collections.OrderedDict(sorted(statistics.items(), key=lambda kv: kv[1]))

            # שומר לתוך str את הנתונים בפורמט נח לקריאה, ורק את הערכים שחופשו יותר מפעם אחת (יש יותר מידי כאלו שחופשו רק פעם אחת).
            statistics_to_send = [f"{k} : {v}\n" for k, v in statistics.items() if v > 1]

            # שולח את הנתונים למתכנת.
            send_data(statistics_to_send, update)

            return "OK"

        # שולח את מספר המשתמשים העדכני.
        if message.title() == "Cu":
            # שולח למתכנת את מספר המשתמשים.
            bot.sendMessage(text=str(len(USERS)), chat_id=chat_id)

            return "OK"

        # מאפשר למתכנת לשלוח הודעה לכלל המשתמשים.
        if "Msg" == message[:3].title():
            # מריץ את הפונקציה ששולחת, עם הטקסט לשליחה (הכל חוץ מ "Msg ").
            msg(message[4:])

            return "OK"

        # שולח למתכנת את רשימת היוזרים (ID'S)
        if message.title() == "Usr":
            # שולח דרך הפונקציה, כי לפעמים ההודעה ארוכה מידי וצריך לחתוך אותה וכו'.
            send_data("\n".join(USERS), update)

            return "OK"

    # שולח שיר אקראי למשתמש.
    if message == "שיר אקראי":
        # מפעיל פונקציה ששולחת שיר אקראי למשתמש.
        send_random(update)

        return "OK"

    # אם מישהו רוצה את רשימת הזמרים, הוא שולח "רשימת אמנים" ומקבל את הרשימה.
    if "רשימת אמנים" in message:
        # התוצאות הן רשימת האמנים חתוכה - שורה חדשה לכל שם.
        result = '\n'.join(ARTISTS_LIST)

        # שולח דרך הפונקציה כי לפעמים ההודעה ארוכה מידי.
        send_data(result, update)

        return "OK"

    # מבצע טייטל להודעה - קודם כל מזיז את התווים שיכולים להפריע הצידה ( "_" לפני תחילת מילה או "#"), מבצע title (שמות השירים בקובץ הם בטייטל - אות ראשונה גדולה) ומחזיר את הסימנים המקוריים.
    # לפעמים מבקשים אקורד ורוצים תמונה שלו, אבל יש אקורדים עם שני שמות - ולכן מחליפים את האקורד לשם הקביל עם התמונה (לדוגמא יש תמונה רק ל"Eb", ולכן מחליפים את "D#" להיות "Eb" - אותו אקורד בשמות שונים).
    chord = message.replace("_", "_ ").replace("#", "# P").title().replace("_ ", "_").replace("# P", "#").replace("/",
                                                                                                                  "_").replace(
        "\\", "_").replace("A#", "Bb") \
        .replace("Db", "C#").replace("D#", "Eb").replace("Gb", "F#").replace("G#", "Ab")

    # אם הטקסט נמצא בספריית האקורדים, הוא אקורד והשולח רוצה לקבל חזרה תמונה.
    if chord in CHORDS_LIBRARY:

        # שולח את התמונה של האקורד.
        bot.sendPhoto(caption=message.replace("_", "/"),
                      chat_id=chat_id,
                      photo=open(f'{ROOT_PATH}/chords/{chord}.png', 'rb'))

        return "OK"

    # אם הטקסט הוא לא אקורד, הוא שיר וצריך לחפש אותו.
    else:

        # מריץ את הפונקציה שמחפשת שירים.
        search_songs(update)
    return "OK"


# מגדירים למה המשימה תענה: פניות מסוג POST לכתובת הספציפית הזו.
@app.route(f'/{BOT_TOKEN}', methods=["POST"])
def main_handler():
    # משנה את הקידוד. העדכון מתקבל בקידוד JSON. מחליף את הקידוד להיות dict של python
    update = request.get_json()

    if 'message' in update:
        print("message")
    if 'callback_query' in update:
        print("callback_query")
        print(update['callback_query']['data'])
        inline_button_handler(update)
        return "OK"

    chat_id = get_message_chat_id(update)

    try:
        message = get_message_text(update)
    except KeyError:
        # אם אין טקסט בהודעה, מתעלמים ממנה. חסרת משמעות עבור הבוט.
        bot.sendMessage(text="no message", chat_id=chat_id)
        return "OK"

    # אם זו הודעת "/start" היא לא דורשת תגובה עניינית לטקסט, אלא תחילת עבודה.
    if message == "/start":
        # שולח את הנתונים (update) לפונקציה שמטפלת  ב START ומסיים את הפעולה.
        start_handler(update)
        return "OK"

    elif "/start" in message:
        # אם ההודעה היא /start אבל יש בה עוד טקסט, מדובר ב /start עם HASH.
        if "/start" in get_message_text(update):
            # מריץ את הפונקציה עם ה HASH כדי לטפל בהודעה.
            start_hash_handler(update)
            return "OK"

    # אם יש טקסט והוא לא START , צריך לחפש את השיר המתאים וכד' - שולח את הנתונים (update) לפונקציה שמטפלת בהודעות.
    message_handler(update)

    return "OK"
