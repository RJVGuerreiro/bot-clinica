import os
import telebot
import google.generativeai as genai

# 1. Configuração das Chaves Secretas (Puxadas do Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializa o Bot do Telegram e a IA da Google
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Configura o modelo Gemini (Rita) com as instruções de comportamento
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Tu és a Rita, uma assistente virtual simpática, prestável e profissional de uma clínica médica. "
        "O teu objetivo é ajudar os pacientes com dúvidas, informações sobre consultas e horários. "
        "Responde sempre em português, de forma acolhedora e breve."
    )
)

# 2. Comando /start (Quando o utilizador inicia o bot)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    boas_vindas = (
        "Olá! 😊 Eu sou a Rita, a assistente virtual da clínica.\n"
        "Estou aqui para ajudar a esclarecer dúvidas ou dar informações. "
        "Como posso ajudar hoje?"
    )
    bot.reply_to(message, boas_vindas)

# 3. Captura todas as outras mensagens e envia para o Gemini
@bot.message_handler(func=lambda message: True)
def responder_com_gemini(message):
    try:
        # Envia a mensagem do utilizador para a IA
        response = model.generate_content(message.text)
        
        # Envia a resposta da IA de volta para o utilizador no Telegram
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Erro ao processar com Gemini: {e}")
        bot.reply_to(message, "Peço desculpa, tive um pequeno problema a processar a tua mensagem. Podes tentar novamente?")

# 4. Inicialização Segura (Apaga webhooks antigos e liga o bot)
if __name__ == "__main__":
    print("A limpar conexões antigas do Telegram...")
    # Esta linha apaga o webhook antigo que estava a dar o erro 409
    bot.delete_webhook(drop_pending_updates=True)
    
    print("A Rita está online e pronta a ajudar no Telegram!")
    # Inicia o bot com folga de tempo para evitar timeouts
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
