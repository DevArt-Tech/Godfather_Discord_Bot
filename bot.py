import os
from threading import Thread

import discord
import random

from flask import Flask

from discord.ext import commands

# permissions
intents = discord.Intents.default()
# Allows the bot to read message content to process commands. This is essential if your bot will respond to messages.
intents.message_content = True

# Necessary if your bot needs to react to events related to members, such as when someone joins or leaves the server.
intents.members = True

# Required for handling events related to guilds, such as server configuration updates or when roles are added or
# removed.
intents.guilds = True

# Enables the bot to detect and respond to reactions on messages.
intents.reactions = True

# Configura tu aplicación Flask (aunque no la uses realmente)
app = Flask('')


@app.route('/')
def index():
    return "El bot de Discord está corriendo."


DISCORD_TOKEN = os.environ["discord_token"]

config = {
    "bot_answers": [
        "tienes agallas al venir a pedirme algo así. Veremos si eres digno de esta misión...",
        "¿crees que estás listo para algo grande? No todos pueden manejarlo. Adelante...",
        "si estás buscando una oportunidad, asegúrate de no decepcionarme. Aquí tienes tu misión.",
        "te daré lo que pides, pero recuerda: si fallas, no habrá segundas oportunidades...",
        "bien, me gusta tu ambición. Pero asegúrate de que esa hambre no te lleve a un mal paso.",
        "no es un trabajo fácil. Si aceptas, más te vale cumplirlo sin errores. ¿Entendido?",
        "eres valiente al pedirlo. Pero la valentía sin inteligencia es un billete directo al cementerio. Más vale que tengas cuidado.",
        "si te doy esta misión, es porque confío en que no me defraudarás. No me hagas lamentarlo.",
        "te daré una tarea, pero cuidado si te metes en problemas.",
        "que quede claro: si te doy esta misión, es porque espero resultados, no excusas...",
        "si quieres probarte, aquí tienes tu oportunidad. No la desperdicies...",
        "te daré una tarea, pero recuerda: no es un juego. Quiero resultados.",
        "lo que me estás pidiendo no es fácil. Espero que estés a la altura.",
        "tienes mi atención. No me hagas arrepentirme de confiar en ti.",
        "está bien, te lo concedo. Pero no olvides quién manda aquí.",
        "veremos si tienes lo que se necesita. No me falles.",
        "si te encargas de esto, más te vale hacerlo bien. Mi paciencia tiene límites.",
        "te lo daré, pero a cambio, espero tu lealtad absoluta y un trabajo impecable.",
        "tienes el deseo, ahora muéstrame que también tienes las habilidades.",
        "si te doy esta misión, estaré observando cada uno de tus movimientos. No me des una razón para dudar de ti."
    ],
    "games": {
        "habbo": {
            "missions": {
                "Intimida a externos": "Intimida a propietarios o miembros de famiglias, negocios o imperios para que entiendan qué facción manda en el hotel, es decir, nosotros.",
                "Tráfico de Armas": "Transporta un arma y trafícala ilegalmente a compradores en diferentes partes del hotel.",
                "Contrabando de Drogas": "Distribuye drogas por el hotel, evitando los Staffs y rivales.",
                "Contrabando Internacional": "Viaja a origins.com y organiza la exportación de items ilegales (armas, drogas, etc).",
                "Asesinato por Encargo": "Investiga quién puede ser un enemigo para la famiglia o para alguno de nuestros miembros y elimínalo.",
                "Ajuste de Cuentas": "Encuentra y elimina a un traidor dentro de la organización o a un rival de otra facción.",
                "Espionaje Industrial": "Infiltrate en un imperio, famiglia u organización y roba información que pueda ser de interés para tus superiores.",
                "Grabación de Conversaciones": "Instalate un micrófono oculto en un lugar clave para obtener información sobre los rivales. Retransmite esa conversación en un canal de voz.",
                "Secuestro de Rivales": "Secuestra a un miembro importante de una facción rival para pedir un rescate o usarlo como moneda de cambio.",
                "Conquista de Zonas": "Toma el control de una facción contraria. Controlala, impón tu presencia o petale su inmobiliario.",
                "Establecimiento de Bases": "Crea nuevas bases o salas para la famiglia, que nos permitan expandirnos como famiglia en el hotel.",
                "Protección de Territorio": "Defiende el territorio de la mafia contra ataques de rivales",
                "Reclutamiento de Nuevos Miembros": "Busca y recluta a nuevos miembros para la organización, evaluando sus habilidades.",
                "Formación y Entrenamiento": "Entrena a nuevos reclutas en tácticas de combate, espionaje, o manejo de armas.",
                "Prueba de Lealtad": "Somete a los nuevos integrantes a pruebas para demostrar su lealtad. Intenta que quebranten las normas de la famiglia y enseñales de qué pasta estamos hechos.",
                "Destrucción de Propiedades": "Ataca y destruye propiedades o negocios de un enemigo para enviar un mensaje de quien manda.",
                "Mantenimiento de Infraestructura": "Asegurate de que los puntos de reunión y otros activos de la mafia estén seguros y operativos. Puertas cerradas, ports volteados... Investiga todas las salas de la famiglia.",
                "Difusión de Propaganda": "Difunde rumores o desinformación para desacreditar a rivales o manipular la opinión pública de otras organizaciones. Por el contrario, difunde buenas criticas de nuestra famiglia.",
                "Organización de Fiestas": "Organiza eventos sociales para consolidar alianzas o mostrar poder dentro de la comunidad. Utiliza el bar de la famiglia para ello.",
                "Investigación de Rivales": "Recopila información sobre las operaciones, puntos débiles, y estructura de una facción rival.",
                "Operaciones en el Extranjero": "Ejecuta una operación criminal en otro país (origins.com) para expandir la influencia y reconocimiento de la famiglia.",
                "Ayuda a tus miembros heridos": "Ve al hospital y cura a tus compañeros heridos después de un encuentro peligroso con otras facciones."
            }
        }
    }
}

# Configura tu bot con los intents y el prefijo
bot = commands.Bot(command_prefix='p!', intents=intents, help_command=None)


# Evento cuando el bot está listo
@bot.event
async def on_ready():
    message = '¡Encantado de estar aquí para ayudarte a rolear!'
    print(message)


@bot.command()
async def status(ctx):
    await ctx.send(f"¿Te pensabas que me había ido a alguna parte, <@{ctx.author.id}>?")


@bot.command()
async def mission(ctx, game: str = 'habbo'):
    if config is not None:
        bot_anwser = random.choice(config["bot_answers"])
        print(f'Respuesta escogida: {bot_anwser}')

        await ctx.send(f"<@{ctx.author.id}>, {bot_anwser}")

        pairs = list(config["games"][game]["missions"].items())

        random_pair = random.choice(pairs)

        embed = discord.Embed(
            title=f'{random_pair[0]}',
            description=f'{random_pair[1]}',
            color=discord.Color.from_rgb(199, 179, 76)  # Color amarillo/beige
        )
        await ctx.send(embed=embed)

    else:
        print("No se pudieron cargar los datos de missions.json.")


# Función para correr el bot en un hilo separado
def run_bot():
    bot.run(DISCORD_TOKEN)


# Crear y lanzar el hilo para el bot de Discord
Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
