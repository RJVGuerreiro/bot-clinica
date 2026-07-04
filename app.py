import os
import telebot
from google import genai
from google.genai import types

# 1. Inicializar as chaves seguras que guardaste nas definições
TELEGRAM_TOKEN = os.environ.get("clinica_teste_ai_bot")
GEMINI_API_KEY = os.environ.get("Gemini_API_Key")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Instruções da Rita (Aqui controlas TUDO o que ela sabe e faz)
INSTRUCOES_RITA = """
Tu és a Rita, uma assistente virtual extremamente simpática, profissional e prestável da Clínica Sorriso.
O teu objetivo é responder às dúvidas dos clientes com base nestas regras:
- Horário de Funcionamento: Segunda a Sexta-feira, das 9h às 18h. Aos Sábados e Domingos estamos encerrados.
- Serviços: Consultas de rotina, limpezas, branqueamentos, implantes e ortodontia.
- Tom de voz: Sempre educada, breve nas respostas e usa termos em português de Portugal.
Se não souberes responder a algo, pede cordialmente para deixarem o contacto para um assistente humano ligar mais tarde.
"""

# 3. Lógica para processar as mensagens do Telegram
@bot.message_handler(func=lambda message: True)
def responder_cliente(message):
    try:
        # Envia a pergunta do cliente para a IA da Google (Gemini 2.5 Flash - Gratuito e rápido)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCOES_RITA,
                temperature=0.7
            )
        )
        # Envia a resposta da IA de volta para o utilizador no Telegram
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Pedimos desculpa, ocorreu um pequeno erro técnico. Por favor, tente novamente em instantes.")
        print(f"Erro: {e}")

# 4. Manter o robô ligado ativamente
if __name__ == "__main__":
    print("A Rita está online e pronta a ajudar...")
    # Aumentámos o timeout para 60 segundos e adicionámos proteção contra falhas
    bot.infinity_polling(timeout=60, long_polling_timeout=60)