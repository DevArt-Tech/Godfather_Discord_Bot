from datetime import datetime

import discord
import requests
from discord.ui import View


class PaginationView(View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        self.update_buttons()

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.message.edit(embed=self.embeds[self.current_page])
            self.update_buttons()

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            await interaction.message.edit(embed=self.embeds[self.current_page])
            self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.current_page == 0
        self.children[1].disabled = self.current_page == len(self.embeds) - 1


def create_json_habbo_response(guild):
    response_dict = dict()
    response_dict["title"] = "Miembros conectados a Habbo"
    response_dict["fields"] = list()
    for member in guild.members:
        habbo_info = get_habbo_api_information(member.name)
        if "error" in habbo_info:
            response_dict["fields"].append({
                "Nombre": member.name,
                "Online": "Error",
                "Ult. Conexión": "Error"
            })
        else:
            iso_date = habbo_info["lastAccessTime"]
            date_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%f%z")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            response_dict["fields"].append({
                "Nombre": member.name,
                "Online": "Sí" if habbo_info["online"] == "True" else "No",
                "Ult. Conexión": formatted_date
            })

    response_dict["fields"] = sorted(response_dict["fields"], key=lambda x: x["Ult. Conexión"], reverse=True) # Ordena por fecha
    response_dict["fields"] = sorted(response_dict["fields"], key=lambda x: x["Online"], reverse=True) # Ordena por conexion

    return response_dict

def get_habbo_api_information(habbo_user: str):
    response = requests.get(
        f'https://origins.habbo.es/api/public/users?name={habbo_user}'
    )
    return response.json()