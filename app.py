import os
import telebot
from google import genai
from google.genai import types

# 1. Configuração das Chaves Secretas (Puxadas do Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializa o Bot do Telegram e o Cliente Gemini moderno
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Configura as instruções de comportamento da Rita
config_rita = types.GenerateContentConfig(
    system_instruction=(
        "Tu és a Rita, uma assistente virtual simpática, prestável e profissional de uma clínica médica. "
        "O teu objetivo é ajudar os pacientes com dúvidas, informações sobre consultas e horários. "
        "Responde sempre em português, de forma acolhedora e breve."
    ),
    model="gemini-2.5-flash"  # Modelo atualizado e rápido
)

# 2. Comando /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    boas_vindas = (
        "Olá! 😊 Eu sou a Rita, a assistente virtual da clínica.\n"
        "Estou aqui para ajudar a esclarecer dúvidas ou dar informações. "
        "Como posso ajudar hoje?"
    )
    bot.reply_to(message, boas_vindas)

# 3. Respostas com o Gemini
@bot.message_handler(func=lambda message: True)
def responder_com_gemini(message):
    try:
        # Envia a mensagem usando a API moderna da Google
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
            config=config_rita
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        # Isto vai mostrar o erro real da Google nos logs do Render!
        print(f"ERRO REAL GEMINI: {e}")
        bot.reply_to(message, "Peço desculpa, tive um pequeno problema a processar a tua mensagem. Podes tentar novamente?")

# 4. Inicialização Segura
if __name__ == "__main__":
    print("A limpar conexões antigas do Telegram...")
    bot.delete_webhook(drop_pending_updates=True)
    
    print("A Rita está online e pronta a ajudar no Telegram!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
