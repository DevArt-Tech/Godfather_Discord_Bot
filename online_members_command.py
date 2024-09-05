from datetime import datetime

import discord
import requests
from discord.ui import Button, View


def create_json_habbo_response(guild):
    response_dict = dict()
    response_dict["title"] = "Miembros conectados a Habbo"
    response_dict["fields"] = list()
    for member in guild.members:
        habbo_info = get_habbo_api_information(member.display_name)
        if "online" in habbo_info and habbo_info["online"] is True:
            iso_date = habbo_info["lastAccessTime"]
            date_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%f%z")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            response_dict["fields"].append({
                "Nombre": member.display_name,
                "Online": "Si" if habbo_info["online"] is True else "No",
                "Ult. Conexión": formatted_date
            })

    return response_dict


def get_habbo_api_information(habbo_user: str):
    response = requests.get(
        f'https://origins.habbo.es/api/public/users?name={habbo_user}'
    )
    return response.json()
