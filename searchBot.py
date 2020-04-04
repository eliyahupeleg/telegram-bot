import glob

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler)


def build_message(files, update):
    if len(files) == 0:
        update.message.reply_text("פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!")

    keyboard = []
    if len(files) > 1:
        for i in files:
            keyboard.append(i[35:-4])
        keyboard.append("חזור")
        update.message.reply_text("בחר...",
                                  reply_markup=ReplyKeyboardMarkup([[i] for i in keyboard]),
                                  one_time_keyboard=True,
                                  selective=True)
        return

    fname = "/home/la/Downloads/HtmlsaveToTxt/message-intro.txt"
    with open(fname, "r") as f:
        introB = f.read()

    fname = "/home/la/Downloads/HtmlsaveToTxt/message-end.txt"
    with open(fname, "r") as f:
        endB = f.read()

    fpath = files[0]
    with open(fpath, "r") as f:

        data = f.read().split('\n')
        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + "   \n" + data[0])
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + "   \n" + data[1])
        intro = intro.replace("capo", data[3])
        song = {0: ""}
        counter = 0
        data[3] = intro
        data.append(endB)
        for j in data[3:]:
            test = song[counter] + "%0A" + j + endB
            if len(test) >= 4096:
                counter += 1
                song[counter] = ""
            song[counter] += "\n" + j

        counter = 0
        for i in song:
            update.message.reply_text(song[counter],
                                      reply_markup=ReplyKeyboardRemove())
            counter += 1


def search_songs(update):
    data = update.message.text
    if data == "חזור":
        update.message.reply_text("חוזר..",
                                  reply_markup=ReplyKeyboardRemove())
        return
    files = []
    data = data.title()
    for fpath in glob.glob("/home/la/Downloads/HtmlsaveToTxt/songs/*"):
        if data == fpath[35:-4]:
            files = [fpath]
            build_message(files, update)
            return
        if data in fpath:
            files.append(fpath)
    print("files: \n", files)
    build_message(files, update)


def start(update, context):
    update.message.reply_text("היי, ברוכים הבאים לרובוט האקורדים של ‏@tab4us - ISRACHORD.\nשילחו את השם המלא של השיר כדי לקבל אותו, או את של הלהקה לפתיחת רשימת השירים שלהם..\nלדיווח:\n@ADtmr")


def main():
    updater = Updater("999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add message handler.
    conv_handler = MessageHandler(Filters.text, search_songs)
    start_handler = CommandHandler('start', start)

    dp.add_handler(conv_handler)
    dp.add_handler(start_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
