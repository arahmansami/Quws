import telebot
import sqlite3

# Bot API Token (BotFather theke token copy kore boshaw)
API_TOKEN = "7450080960:AAF-4ZUcBKvO724vGV4I2ISjrDnLIdH15Wc"
bot = telebot.TeleBot(API_TOKEN)

# Database connection
conn = sqlite3.connect("questions.db", check_same_thread=False)
cursor = conn.cursor()

# Database Table Create Query
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT
)
""")
conn.commit()

# Save question command handler
@bot.message_handler(commands=['save'])
def save_question(message):
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        bot.reply_to(message, "Please provide a question to upload! Example: /save What is Python?")
    else:
        question = text[1]
        cursor.execute("INSERT INTO questions (question) VALUES (?)", (question,))
        conn.commit()
        bot.reply_to(message, f"Your question has been uploaded: {question}")

# Show all uploaded questions command handler
@bot.message_handler(commands=['show'])
def show_questions(message):
    cursor.execute("SELECT question FROM questions")
    all_questions = cursor.fetchall()
    if all_questions:
        questions_list = "\n".join([q[0] for q in all_questions])
        bot.reply_to(message, f"Here are all uploaded questions:\n{questions_list}")
    else:
        bot.reply_to(message, "No questions have been uploaded yet!")

# Default message response
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "Use /save [question] to upload a question or /show to see all uploaded questions.")

# Start the bot
bot.polling()