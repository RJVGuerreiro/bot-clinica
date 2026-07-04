import os
import threading
import telebot
from flask import Flask
from google import genai
from google.genai import types

# 1. Configuração do Flask (Simulador de site para o Render não reclamar da porta)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot da Clínica está online!", 200

# 2. Configuração das Chaves Secretas
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

config_rita = types.GenerateContentConfig(
    system_instruction=(
        "Tu és a Rita, uma assistente virtual simpática, prestável e profissional de uma clínica médica. "
        "O teu objetivo é ajudar os pacientes com dúvidas, informações sobre consultas e horários. "
        "Responde sempre em português, de forma acolhedora e breve."
    ),
    model="gemini-2.5-flash"
)

# 3. Comandos do Telegram
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    boas_vindas = (
        "Olá! 😊 Eu sou a Rita, a assistente virtual da clínica.\n"
        "Estou aqui para ajudar a esclarecer dúvidas ou dar informações. "
        "Como posso ajudar hoje?"
    )
    bot.reply_to(message, boas_vindas)

@bot.message_handler(func=lambda message: True)
def responder_com_gemini(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
            config=config_rita
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"ERRO REAL GEMINI: {e}")
        bot.reply_to(message, "Peço desculpa, tive um pequeno problema a processar a tua mensagem. Podes tentar novamente?")

# Função para correr o Telegram em segundo plano
def run_bot():
    print("A limpar conexões antigas do Telegram...")
    bot.delete_webhook(drop_pending_updates=True)
    print("A Rita está online e pronta a ajudar no Telegram!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    # Inicia o bot do Telegram numa thread separada
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Inicia o servidor Flask na porta que o Render exige
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
