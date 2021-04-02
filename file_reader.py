import glob
import os
import re

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
uploaded_path = this_folder + "/uploaded/"
uploaded_list = glob.glob(f"{uploaded_path}/*")

# משמש להמרת סולמות. האקורדים במרווחים של חצי בדיוק.
levels = [["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
          ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]]

# השירים נשמרים בלי הפתיחה והסיום (שורות מיוחדות עם אמוג'ים וקישור לערוץ או לרובוט).
# כדי לחסוך פתיחה מחדש של הקובץ ששומר את נתוני הפתיחה והסיום (הם קבועים), הפתיחה והסיום של ההודעות נשמרים בקבועים.
fname = f"{this_folder}/message-intro.txt"
with open(fname, "r") as f:
    INTRO = f.read()

fname = f"{this_folder}/message-end.txt"
with open(fname, "r") as f:
    # בקובץ סיום יש קישור לערוץ של האקורדים. בגלל שהבוט הוא זה ששלח את ההודעה ולא הערוץ, הקישור בסוף משתנה לקישור לבוט ולא לערוץ.
    ENDING = f.read().replace("‏@Tab4us", "‏@Tab4usBot")


# ממיר את השיר לסולם חדש
def new_key(index, key):
    # אם ממירים ב1.5, זה בעצם 3 חצאים ללמעלה.
    # ההמרה לפי חצאים כי יותר קל להשתמש ב2 מ0.5
    half_key = int(float(key) * 2)

    """
    לשלוף את ההודעה המקורית מהקובץ
    להשתמש ב RE.SUB כדי להחליף את האקורדים המתאימים
    לשנות אחד מהאקורדים, הראשון או האחרון לסימן אחר- כדי שלא ישנה אותו בהמרה, או להוסיף סימן "הומר" שיימחק מייד אחרי.
    לשלוח את ההודעה עם המרה ביחס למקור, לא להודעה.
    """

    with open(uploaded_list[index], "r") as f:

        data = f.read()

        # אחד דיאזים אחד במולים
        for level in levels:

            for chord in level:

                chord_index = level.index(chord)
                new_chord_index = half_key + chord_index
                len_level = len(level)
                print(len_level, "len_level")

                if new_chord_index >= len_level:
                    new_chord_index -= len_level

                if new_chord_index < 0:
                    new_chord_index += len_level

                print(new_chord_index, "new_chord_index")
                # מחליפים לאקורד הבא. מוסיפים | כדי לא להמיר את אותו אחד פעמיים.
                data = re.sub("\[" + chord, '[|' + str(level[new_chord_index]), data)

        if data.split("\n")[5] == "HE":
            data = data.replace("#]", "#ᶥ")

        data = data.replace("[|", "").replace("#]", "#ᶥ").replace("]", "")
        data = data.split('\n')

        intro = INTRO
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + f"   \n{data[0]}")
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + f"   \n{data[1]}")

        if "המערכת" == data[2]:
            intro = intro.replace("version", "⭐️ גרסה רשמית ⭐")
        else:
            intro = intro.replace("version", "")

        # כמה צריך להזיז כדי להגיע לגרסה קלה
        easy_key = data[3]

        # איפה לשים קאפו
        if 0 == int(data[4]) + half_key:
            intro = intro.replace("capo", "")
        else:
            intro = intro.replace("capo", f"קאפו בשריג {(int(data[4]) + half_key)}")

        # המידע בתחילת הקובץ לא נשלח, רק מ - data[3] ואילך.
        # ולכן מכניסים ל- data[3] את כל הפתיח הרשמי, והוא נשלח משם.
        data[4] = intro
        data.append(ENDING)

    # מנקים את סימני הבקרה
    print(data[4:])
    return data[4:]


print(uploaded_path, uploaded_list.index(
    "/home/la/Desktop/bots/chords-bot/uploaded/Matisyahu and Infected Mushroom - One Day (רשמי).txt"))
print(new_key(7904, "+1"))
