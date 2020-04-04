import glob

from telegram.ext import (Updater, MessageHandler, Filters)


def build_message(files, update):

    fname = "/home/la/Downloads/HtmlsaveToTxt/message-intro.txt"
    with open(fname, "r") as f:
        introB = f.read()

    fname = "/home/la/Downloads/HtmlsaveToTxt/message-end.txt"
    with open(fname, "r") as f:
        endB = f.read()

    for fpath in files:
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

                update.message.reply_text(song[counter])
                counter += 1


def search_songs(data, update):
    files = []
    data = data.title()
    for fpath in glob.glob("/home/la/Downloads/HtmlsaveToTxt/songs/*"):
        if data in fpath:
            files.append(fpath)
    print("files: \n", files)
    build_message(files, update)


def start(update, context):
    update.message.reply_text(
        '#' + update.message.text.replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(".", "_")
        .replace(",", ""))
    search_songs(update.message.text, update)


def main():
    updater = Updater("999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add message handler.
    conv_handler = MessageHandler(Filters.text, start)

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
