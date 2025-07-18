import discord
import random
import string
from flask import Flask
import threading

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Simuler une base de codes en mémoire
valid_codes = {}


def generate_secret_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower().startswith("!code"):
        code = generate_secret_code()
        valid_codes[code] = message.author.id
        await message.author.send(f"Voici ton code secret : **{code}** (valable 2 min)")

        # Expiration du code au bout de 2 minutes
        import threading, time

        def expire():
            time.sleep(120)
            valid_codes.pop(code, None)

        threading.Thread(target=expire, daemon=True).start()


# Flask app pour exposer les codes à ton dashboard
flask_app = Flask(__name__)


@flask_app.route("/api/check_code/<code>")
def check_code(code):
    if code in valid_codes:
        return {"valid": True}
    return {"valid": False}


def run_flask():
    flask_app.run(port=10000)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    with open('token.txt', 'r') as f:
        contenu = f.read()
    bot.run(contenu)
