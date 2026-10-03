import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN", "8766142799:AAHtH4iucLobzG1D8qTIKn_AuZYM_nVMZl4")

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Купить файл", callback_data="buy"))
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Это компания Brudaware.\n\n"
        "Рады приветствовать вас в нашем боте.\n"
        "Здесь вы можете приобрести наш файл.\n\n"
        "Нажмите «Купить файл» или используйте /buy.",
        reply_markup=markup
    )


@bot.message_handler(commands=['buy', 'help'])
def send_buy(message):
    bot.send_message(
        message.chat.id,
        "Для покупки файла напишите нам, либо нажмите кнопку ниже.\n"
        "Оплата и выдача файла пока настраивается."
    )


@bot.callback_query_handler(func=lambda call: call.data == "buy")
def callback_buy(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "Вы выбрали покупку файла.\nОплата и выдача файла пока настраивается."
    )


if __name__ == "__main__":
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Brudaware bot alive")

        def log_message(self, *args):
            pass

    port = int(os.getenv("PORT", "10000"))
    threading.Thread(target=HTTPServer(("0.0.0.0", port), Handler).serve_forever, daemon=True).start()

    print("Bot started...")
    bot.infinity_polling()
