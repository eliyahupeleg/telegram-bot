import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

js = r'''

// השם הוא "שם הזמר-שם השיר"
var name = jQuery('<div>').html(document.querySelector("#page_content > div.row > div > div.song_block_top > div.ArtistAndSongName")).text().slice(1, -1);

//אם השיר נערך על ידי המערכת (לא מצויין שנערך על ידי משתמש) השיר יסומן כגרסה רשמית.
editedBy = "המערכת";
if(document.getElementById("editByUser")) editedBy = "גולש";

//אי אפשר לשמור "\" בשם של קובץ, אז מחלפים אותו ל"_"
name = name.replace("/", "_");

//מחלק את השם לזמר ולשיר
singer = name.split("  - ")[0];
song = name.split(" - ")[1];

//אם לא כתוב איפה לשים את הקאפו, שומרים "0" כסימן ל"בלי קאפו".
capo = "0";
//הכתובית בסגנון "שים קאפו בשריג 8". שומרים רק את המספר (נח יותר להעלאה ועריכה).
if (document.querySelector("#capoAnn") != null) capo = document.querySelector("#capoAnn").textContent[document.querySelector("#capoAnn").textContent.length-1];

//יש שירים שהעמוד באתר ריק (אין מילים ואין אקורדים). מדלגים על השירים האלו. אם הסקריפט ימשיך לרוץ, הוא יקרוס עם שגיאה.
if (document.querySelector("#songContentTPL") == null){ return("null")}

//אם הדף מוצמד לימין, השפה של השיר היא עברית. אם לשמאל, אנגלית. שומר את השפה בשביל ההצמדה לימין ושמאל של האקורדים.
aligh = document.querySelector("#songContentTPL").align;
language = "HE";
if(aligh == "left") language = "EN";
if(aligh == "right") language = "HE";

//יש בדרך כלל שורות של "מעבר" בלתי נראות שצריך למחוק. לולאת פור מוחקת רק את האיבר הראשון.
var brs = document.getElementsByClassName("br");
var cnt = 0;
while(brs.length){
    brs[cnt].parentNode.removeChild(brs[cnt])
}

//מנקה את האלמנטים שנועדו להציג את צורת האקורד. משאיר באלמנט של שורת אקורדים רק את האקורדים ואת הרווחים בניהם.
var divs = document.getElementById("songContentTPL").querySelectorAll("div");
for(var i of divs){
    i.parentNode.removeChild(i);
}

//משתנה שיישמר לקובץ הטקסט, יכיל את כל השיר והאקורדים.
var textToFile = "";

//הדף בנוי כטבלה של פסקאות. שומרים את הפסקאות למערך מסודר.
//שומרים לפי פסקאות כדי לסדר נכון את הרווחים בין השורות (0 אחרי שורה בעברית, 1 אחרי שורה באנגלית, 2 בסיום פסקה).
data = document.getElementById("songContentTPL").getElementsByTagName("table");
var tableArr = Array.prototype.slice.call(data)

//כל פסקה...
for (var paragraph of tableArr){

    //מחלק את הפסקה לפי שורות,ועובר שורה שורה.
    lines = paragraph.getElementsByTagName("td");
    var linesArr = Array.prototype.slice.call(lines);

    //מוסיפים לטקסט שורה שורה, ומסדרים - שורת שיר נכנסת שלמה, שורת אקורדים נכנסת עם [] סביב כל אקורד.
    for (var line of linesArr){


        //לפני כל פסקה של טאבים מוסיף 2 שורות רווח, כדי שהשורות לא יתבלבלו.
        if (line.className == "tabs" && line.textContent[1] == "e") {
            textToFile += "\n\n"
        }

        //בודק אם מדובר בשורת אקורדים (דורש למרקר כל אקורד)
        if (line.className =="chords" || line.className =="chords_en") {

            //רוב השורות אקורדים מסודרות עם אלמנטים מיוחדים לכל אקורד, ורווחים בלי אלמנט.
            //יש שורות אקורדים בלי אלמנטים, פשוט אקורדים ורווח בצורה טקסטואלית. בשורות כאלו מספר ה"ילדים" של השורה יהיה 0.
            if (line.childElementCount == 0){

                //בתחילת כל שורת אקורדים בקובץ שמוצמד לימין, מוסיפים 2 תווים מיוחדים. אחד מצמיד לימין את השורה, והבא אחריו מסדר את הטקסט משמאל לימין בכח. התוצאה היא ששורת האקורדים עוברת לצד ימין בצורה מדוייקת. 
                if(language == "HE"){
                    textToFile += "\u200F" + "\u202d";
                }

                //יש שני סוגי רווחים. אחד רגיל, ואחד nbsp . כדי להימנע מטעויות זיהוי, הופכים את כולם לרווח רגיל.
                chords = line.textContent.replaceAll(String.fromCharCode(160), " ").split(" ");

                //מסיר כפילויות של אקורדים ותאים ריקים - אנחנו רוצים לבצע "החלף" לכל אקורד, ולשים במקומו [אקורד]. אם יש תא ריק, ייכנסו המון סוגריים סתם, ואם יש כפילות, הוא יהפוך את האקורד ל [[אקורד]].
                chords = [...new Set(chords)];
                chords = chords.filter(item => item);
                
                //יש שני סוגי רווחים. אחד רגיל, ואחד nbsp . כדי להימנע מטעויות זיהוי, הופכים את כולם לרווח רגיל.
                //מוסיפים רווח בהתחלה ובסוף כדי לוודא שכל אקורד יהיה מוקף רווחים וקל לזיהוי. הרווחים יממחקו אחר כך.
                chordsLine = " " + line.textContent.replaceAll(String.fromCharCode(160), " ") + " ";

                //עובר אקורד אקורד, בודק אם יש כזה בדיוק, ואם כן מוסיף לו [].
                for (var chord of chords){
                    //אם יש אקורד מ2 סוגים (לדוג' G וגם G7) האות תקבל שני סוגריים - אחת גם מהאקורד המקורי, ולכן צריך שיהיה רווח לפני או אחרי - מה שמתקיים רק באקורד המדוייק.
                    //לפעמים יש את אותו אקורד פעמיים רצוף - והאלגוריתם מזהה רק את הראשון (מייחס אליו את הרווח). בגלל זה יש טיפול מיוחד באקורדים כפולים ואז טיפול ברגילים.
                    chordsLine = chordsLine.replaceAll(" " + chord + " " + chord, " [" + chord + "] [" + chord + "] ");
                    chordsLine = chordsLine.replaceAll(" " + chord + " ", " [" + chord + "] ");
                }

                //מוסיפים את השורה המסודרת לטקסט של השיר אחרי שמוחקים את רווחי הביטחון.
                textToFile += chordsLine.slice(1, -1)


            }

            //אם יש לשורה "ילדים", אפשר לסדר אותה יותר בנוחות, כי לכל אקורד יש אלמנט.
            else{

                //מחלק את השורה לחוליות. חוליה יכולה להיות רווחים (לפעמים עם שורה חדשה) או אקורד.
                var nodes = line.childNodes;
                
                //עובר על כל החלקים של השורה.
                for (const node of nodes){
    
    
                    //לפני החוליה הראשונה, אם צריך להצמיד לימין, מוסיף את שני התווים - אחד מצמיד לימין והשני מכריח את הטקסט להסדר בצורה הנכונה משמאל לימין.
                    if(language == "HE" && node == nodes[0]){
                        textToFile += "\u200F" + "\u202d";
                    }
    
    
                    //שומרים את הערך של החוליה אחרי שמוחקים ממנה את כל הרווחים והשורות החדשות, וחותכים בכל מקום שיש רווח. נוצר מערך של תאים עם אקורד שלם, ותאים ריקים כמספר הרווחים.
                    chords_value = node.textContent.replaceAll(String.fromCharCode(10), "").split(String.fromCharCode(160));
    
                    //אם מורידים את הרווחים והשורות החדשות מהחוליה והיא לא ריקה, יש שם אקורד שהמערכת לא זיהתה, ומיתגה כטקסט. יש אקורדים שמסומנים כ "SPIN", אבל אלו רק האקורדים שלמערכת יש את התמונה שלהם. השאר סתם קיימים בטקסט בלי תגית.
                    if(node.textContent.replaceAll(String.fromCharCode(160), "").replaceAll(String.fromCharCode(10), "").replaceAll(" ", "") != ""){
                    
                        //בתוך chords_value יש את כל השורה חתוכה לפי "רווח", מה שיוצר תאי רווח (תאים ריקים כמספר הרווחים) ותאי אקורד (תאים שמכילים אקורד שלם).
                        //הלולאה שמה את הסוגריים על האקורד ומכניסה אותו לטקסט.
                        for (var cell of chords_value){
                            
                            //תא ריק מבטא רווח. מחליפים אותו לערך המקורי.
                            //תא מלא מכיל אקורד. מוסיפים לו [].
                            if (cell == "") {
                                cell = String.fromCharCode(160);
                            }else{
                                cell = "[" + cell + "]"
                            }
                            
                            //מוסיפים לטקסט את החלק החדש כל פעם.
                            textToFile += cell;
                        }
    
                    }
    
                    //אם מדובר במקטע של רווח, מכניסים אותו כמו שהוא לטקסט. מורידים שורות חדשות ומוסיפים ידנית בצורה נוחה יותר.
                    else{
                        textToFile += node.textContent.replace("\n","");
    
                    }
    
                }
            }
            //השורות החדשות המובנות נמחקו, ובונים אותן מחדש לפי הפורמט.
            textToFile += "\n";

        }

        //זו שורה בלי אקורדים. שומר אותה כמו שהיא, רק בלי השורה החדשה, כדי להוסיף ידנית ולפי הפורמט.
        else {
        textToFile += line.textContent.replace("\n", "");
        textToFile += "\n";

        //אם השיר באנגלית, מוסיפים עוד שורה ריקה אחרי כל שורה כדי שיהיה מסודר ונעים לעין.
        //if (language == "EN") textToFile += "\n";
        }
    }
    
    //בסוף כל פסקה יש 2 שורות רווח
    textToFile += "\n\n";
}

//אם יש גרסה קלה, מוסיף אותה. אם לא, כותב "0".
if (document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a") == null) EZTon = "0";
else EZTon = document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a").href.slice(document.querySelector("#page_content > div.row > div > div.song_block_content_wrap > div.bArae4 > a").href.search("ton=")+4);

//שומר את כל הנתונים מסודר, ומחזיר לפונקציית אם.
newData = song + '\n' + singer + '\n' + editedBy + '\n' + EZTon + '\n' + capo + '\n' + language + '\n' + textToFile;
return (newData)
'''

# בודק האם יש אקורדים בקישור בנוכחי או שהדף ריק \ רק מילים
js_is_chords = r'''return (document.getElementById("tonChange") == null)'''

# בודק האם השיר סגור חוץ מלמשתמשי פרימיום (נמנע מלהוריד)
js_is_premium = r'''return (document.querySelector("#premiumOnlyAreaInSongs") != null && document.querySelector("#premiumOnlyAreaInSongs").textContent.length == 59)'''

# שולף את הנתונים מהאתר ומסדר אותם לשמירה

# התיקייה הנוכחית. משמש לגישה לקבצים מוגדרים וספריות.
this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])

# יוצר דפדפן כרום וירטואלי.
# משתמשים בכרום כי מאוד פשוט לרנדר (מריץ לבד את הJS שלו) ולהריץ עליו JS חיצוני.
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=options, executable_path="/home/la/chromedriver")

# הקובץ שומר את המונה שירים שירדו. בהשוואה למונה באתר אפשר לדעת איזה שירים חדשים.
file_name = f"{this_folder}/lst.txt"

print("CHECKING FOR UPDATES...")

# רץ בלולאה כי הלינקים לשירים מגיעים מעמוד תוצאות חיפוש, ולפעמים יש יותר תוצאות ממה שעמוד אחד מכיל - הלולאה מתחילה שוב את החיפוש עד שנגמר העדכונים.
while True:

    # בודק את המונה שירים שירדו, כדי להשוות למספר השירים הקיימים ולבדוק אם יש עדכון.
    with open(file_name, "r") as f:
        lst = f.read()

    # הקישור של TAB4U למובייל לא דורש את שם השיר, רק את המספר, ולכן היה עדיף על האתר למחשב שולחני. ברגע שהבעיה נפתרה, הJS כבר היה מותאם לאתר לנייד ולכן לא שונה הקישור.
    basic_url = "https://www.tab4u.com/songForMobile.php?id="

    # מריץ חיפוש על כל השירים הקיימים. יש מונה של תוצאות ("X תוצאות") באתר, וכך אפשר לדעת כמה שירים יש באתר ואם יש עדכון.
    search = "https://www.tab4u.com/resultsSimple?tab=songs&type=song&q=0&content=&max_chords=0"

    # מריץ בלי מגבלת זמן. אם העדכון יקרוס באמצע הוא יצטרך הפלה מחדש ידנית, עדיף שימתין עד שיחזור החיבור לרשת.
    request = requests.get(search, timeout=None, verify=False)

    # מסדר את ה response בפורמט של HTML
    soup = BeautifulSoup(request.content, "html.parser")

    # שולף את מספר השירים שיש באתר מ HTML לתוך num.
    num = int(soup.find_all(class_="foundTxtTd")[0].getText().split(" ")[1])

    # כשמגיע למצב שמספר השירים באתר שווה למספר השירים שנשמרו, עוצר. אין עוד עדכונים.
    if int(lst) == int(num):
        print("UP-TO-DATE!")
        break

    print("שירים באתר: ", num)
    print("שירים שנשמרו: ", lst)
    print("שירים חדשים: ", int(num) - int(lst))

    # שומר את המספר של השיר האחרון שירד. יש פרמטר בחיפוש של האתר שאומר מאיזה מספר תוצאה להתחיל - וכך כל הלינקים הם רק של השירים החדשים.
    num = int(lst)

    # הלינק הוא חיפוש באתר, ומציג את כל השירים שיש באתר, משיר מספר {num} ועד הסוף (בעצם את כל העדכונים)
    url = f"https://www.tab4u.com/resultsSimple?tab=songs&q=0&type=song&cat=&content=&max_chords=0&n=30&sort=&s={num}"

    # מסדר ב HTML את תוצאות החיפוש של הלינק url.
    request = requests.get(url, timeout=None, verify=False)
    soup = BeautifulSoup(request.content, "html.parser")

    # שומר מתוך ה HTML את האובייקטים של כל התוצאות.
    links = soup.select('.songTd1 .searchLink')

    # שולף את הלינקים (הפנימיים, בלי הקידומת של האתר) של התוצאות מהאובייקטי HTML ומכניס אותם לרשימה.
    links = [i['href'][11:] for i in links]

    # עובר על כל הלינקים של העדכונים..
    for link in links:

        # מוסיף את הקידומת של האתר כדי ליצור לינק מלא מהלינק הפנימי.
        full_link = basic_url + link

        # הלינק מודפס למטרת QA וזיהוי בעיות ON-LINE
        print(full_link)

        # מבקש את העמו של השיר מהאתר, מזדהה בתור דפדפן רגיל.
        browser.get(full_link)

        # אם השיר הוא ללא אקורדים (רק מלל) מדלגים עליו.
        if browser.execute_script(js_is_chords):
            print("\n\n\nsong without chords\n\n\n")

            # אם השיר הוא ללא אקורדים, המונה שירים שהורדו סופר אותו כשיר שירד למרות שהוא לא ירד.
            # מעליםאת המונה ב1, ועוברים לשיר הבא.
            with open(file_name, "r+") as f:
                f.seek(0)
                f.truncate()
                f.write(str(num + int(links.index(link)) + 1))
            continue

        # בודק אם השיר נעול בפורמט "פרימיום"
        if browser.execute_script(js_is_premium):
            print("\n\n\npremium song\n\n\n")

            # אם השיר הוא פרימיום, המונה שירים שהורדו סופר אותו כשיר שירד למרות שהוא לא ירד.
            # מעליםאת המונה ב1, ועוברים לשיר הבא.
            with open(file_name, "r+") as f:
                f.seek(0)
                f.truncate()
                f.write(str(num + int(links.index(link)) + 1))
            continue

        # הקוד JS שומר את השיר בפורמט טקסטואלי מסויים, ומחזיר אותו כ str.
        song = browser.execute_script(js)

        # אם השיר הוא ללא אקורדים (לפעמים יש באתר רק את הכותרת בלי שיר או בלי האקורדים שלו) מדלגים עליו.
        if song == "null":
            print("\n\n\nsong without chords\n\n\n")

            # אם השיר הוא ללא אקורדים, המונה שירים שהורדו סופר אותו כשיר שירד למרות שהוא לא ירד.
            # מעליםאת המונה ב1, ועוברים לשיר הבא.
            with open(file_name, "r+") as f:
                f.seek(0)
                f.truncate()
                f.write(str(num + int(links.index(link)) + 1))
            continue

        # מדפיס את השיר למטרת QA וזיהוי בעיות בצורה יעילה.
        print(song)

        # שולף מהנתונים ב song את שם הזמר ושם השיר כדי לשים בשם הקובץ.
        song_split = song.split('\n')

        # אם השיר נערך על ידי המערכת, הוא ממורקר בתור "רשמי" - גם בשם הקובץ, מה שנותן בתוצאות החיפוש של הבוט אינדיקציה לגבי מידת הדיוק של האקורדים.
        if song_split[2] == "המערכת":
            song_split[0] += " (רשמי)"

        # שומר את השיר לקובץ עם השם המתאים בתקיית "מיועדים להעלאה".
        with open(f"{this_folder}/toUpload/{song_split[1]} - {song_split[0]}.txt", "w+") as f:
            f.write(song)
            f.close()

    # מעדכן את המונה כל פעם שמסיים שיר.
    with open(file_name, "r+") as f:
        f.seek(0)
        f.truncate()
        f.write(str(num + int(links.index(link)) + 1))

# סוגר את הדפדפן אחרי שמסיים את כל העדכונים.
browser.quit()

# מפעיל (לפי בחירה) את הקובץ שמעלה את הקבצים.
if input("UPLOAD? (Y/N)\n\n\nMake sure tou are not with 'RIOM'\n\n") == "Y":
    print("uploading...")
