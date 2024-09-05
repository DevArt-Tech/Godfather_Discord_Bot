import os
from threading import Thread

import discord
import random
import json
from http import HTTPStatus

import requests
from discord import app_commands
from discord.ext import commands
from flask import Flask
from datetime import datetime

import config as c
import wit_ai_methods as wit_ai
from online_members_command import create_json_habbo_response

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

DISCORD_TOKEN = "MTI3OTc1MTEyMjc2ODEwNTUxNA.Ge9uZS.k6tP6WE1ckyZyWNkBE8q1HWQBSBffGR-aTkfFw" #os.environ["discord_token"]
#WIT_AI_TOKEN = #os.environ["wit_ai_token"]
SERVER_NAME = "test" #os.environ["discord_server_name"]

# Configura tu bot con los intents y el prefijo
bot = commands.Bot(command_prefix='p!', intents=intents, help_command=None)


@app.route('/')
def index():
    return "El bot de Discord está corriendo."


@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Sync the slash commands with Discord
        print(f'Synced {len(synced)} command(s)')

    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    """Informa sobre si el bot está conectado o no."""
    bot_answer = give_random_answer("status")
    await interaction.response.send_message(bot_answer)


@bot.tree.command(name="mision")
async def mission(interaction: discord.Interaction, member_to_give_mission: discord.Member):
    """Pide una mision al Padrino de la Famiglia para que la completes."""
    if c.config is not None:
        bot_answer = give_random_answer("mission")

        #await interaction.response.send_message(f"{member_to_give_mission.mention}, {bot_answer}")

        pairs = list(c.config["mission"]["games"]["habbo"]["missions"].items())

        random_pair = random.choice(pairs)

        # Obtener los roles del usuario
        user_roles = member_to_give_mission.roles
        role_names = [role.name for role in user_roles]
        ranks = c.config["ranks"]

        # Convertir listas a conjuntos y encontrar la intersección
        intersection_roles = list(set(ranks) & set(role_names))
        rank = ""
        if len(intersection_roles) != 0:
            rank = intersection_roles[0]

        embed = discord.Embed(title="Mision asignada", color=discord.Color.from_rgb(199, 179, 76))
        embed.set_thumbnail(url=member_to_give_mission.avatar.url)  # Si el usuario tiene un avatar
        embed.add_field(name="Miembro", value=member_to_give_mission.mention, inline=True)
        embed.add_field(name="Rango", value=rank, inline=True)
        embed.add_field(name="Titulo de Misión", value=f"{random_pair[0]}", inline=True)
        embed.add_field(name="Descripción", value=f"{random_pair[1]}", inline=True)

        msg = f"{member_to_give_mission.mention}, {bot_answer}"

        await interaction.response.send_message(content=msg, embed=embed)

@bot.tree.command(name="onlinemembers")
async def onlinemembers(interaction: discord.Interaction):
    """Devuelve una lista de los miembros del servidor de discord que están online en Habbo"""

    await interaction.response.send_message("Estoy recopilando la información, por favor espera...")

    guild = discord.utils.get(bot.guilds, name=SERVER_NAME)
    if guild is None:
        await interaction.response.send_message("No he encontrado ningun miembro en el servidor.")
        return

    json_response = create_json_habbo_response(guild)

    embed = discord.Embed(title=json_response["title"], color=discord.Color.from_rgb(199, 179, 76))
    if json_response["fields"]:
        for field in json_response["fields"]:
            embed.add_field(name="Nombre", value=field["Nombre"], inline=True)
            embed.add_field(name="Online", value=field["Online"], inline=True)
            embed.add_field(name="Ult. conexión", value=field["Ult. Conexión"], inline=True)

        await interaction.followup.send(embed=embed)
    else:
        embed.add_field(name="Ops", value="No hay miembros conectados", inline=True)
        await interaction.followup.send(embed=embed)


'''@bot.tree.command(name="duda")
async def question(interaction: discord.Interaction, message: str, ):
    """Responde a tu pregunta usando IA"""
    user = interaction.user  # Obteniendo el usuario que ejecutó la interacción
    wit_response = wit_ai.get_message(message, WIT_AI_TOKEN)
    if wit_response is not None:
        response_answer = wit_ai.parse_message(c.config, wit_response)

    embed = discord.Embed(title=f"Duda de {user.display_name}", color=discord.Color.blue())
    embed.add_field(name="Pregunta: ", value=message, inline=True)
    embed.add_field(name="Respuesta", value=f"{response_answer}", inline=True)

    await interaction.response.send_message(embed=embed)'''


def give_random_answer(command):
    if c.config is not None:
        bot_anwser = random.choice(c.config[command]["bot_answers"])
        print(f'Respuesta escogida: {bot_anwser}')
        return bot_anwser


def run_bot():
    bot.run(DISCORD_TOKEN)


# Crear y lanzar el hilo para el bot de Discord
Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
