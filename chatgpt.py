import openai
from telebot import TeleBot

TELEGRAM_TOKEN = '6752071699:AAF8FYHZySix_Dx7jmsq1LjeoieaRZi47yU'
OPENAI_API_KEY = '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'
bot = TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

user_history = {}

def update_user_history(chat_id, message, role):
    user_history.setdefault(chat_id, []).append({"role": role, "content": message})

def is_identity_question(message):
    return 'как тебя зовут' in message.text.lower()

def is_creator_question(message):
    text = message.text.lower()
    return 'кто твой создатель' in text or 'кто тебя создал' in text

@bot.message_handler(func=is_identity_question)
def handle_identity_question(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "iminov's GPT")

@bot.message_handler(func=is_creator_question)
def handle_creator_question(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Мой создатель - Iminov Elyor @itsmyIink")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_message = message.text
    update_user_history(chat_id, user_message, "user")

    try:
        conversation_history = user_history.get(chat_id, [])
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        bot_reply = response.choices[0].message.content
        
        update_user_history(chat_id, bot_reply, "assistant")
        bot.send_message(chat_id, bot_reply)
    except Exception as e:
        bot.send_message(chat_id, f'Произошла ошибка: {e}')

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Я бот, который может отвечать на вопросы. Попробуйте спросить что-нибудь!")

bot.infinity_polling()
