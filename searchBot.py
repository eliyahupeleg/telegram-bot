import configparser

from telegram.ext import (Updater, MessageHandler, Filters)


def start(update, context):
    update.message.reply_text('#' + update.message.text.replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(".", "_").replace(",", ""))


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
    read()
