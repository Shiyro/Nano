from typing import Optional
import discord
from discord.commands import slash_command, message_command, user_command
from discord.ui import Button, View, view
from discord.ext.commands import Cog
from discord import Embed,File, interactions

import random

class MorpionButton(Button):
    def __init__(self, *, m_view: View ,custom_id: Optional[str] = None, row: Optional[int] = None, column:Optional[int]):
        super().__init__(label="-",style=discord.ButtonStyle.grey,row=row,custom_id=custom_id)
        self.m_view = m_view
        self.row = row
        self.column = column
        self.clicked = False
        
    async def callback(self,interaction):
        if self.clicked == False:
            if interaction.user == self.m_view.turn:
                joueur=self.m_view.turn
                if interaction.user == self.m_view.players[0]:
                    self.style=discord.ButtonStyle.green
                    self.label = "X"
                    self.m_view.turn = self.m_view.players[1]
                else:
                    self.style=discord.ButtonStyle.red
                    self.label = "O"
                    self.m_view.turn = self.m_view.players[0]
                    self.m_view.choix[self.column][self.row] = interaction.user
                self.m_view.choix[self.column][self.row] = interaction.user
                self.clicked = True
                
                if self.m_view.check_win():
                    await interaction.response.edit_message(content = f"**{joueur.mention} a gagné la partie !**", view=self.m_view)
                    self.m_view.stop()
                elif self.m_view.check_draw():
                    await interaction.response.edit_message(content = f"**Egalité !**", view=self.m_view)
                    self.m_view.stop()
                else:
                    await interaction.response.edit_message(content = f"Au tour de {self.m_view.turn.mention}", view=self.m_view)
                
                
            else:
                await interaction.response.send_message(content="C'est pas à toi de jouer !",ephemeral=True)

class MorpionInteraction(View):
    def __init__(self,joueurs):
        super().__init__(timeout=600)
        for i in range(3):
            for j in range(3):
                button = MorpionButton(m_view=self,row=i,column=j)
                self.add_item(button)
        self.players = joueurs
        self.turn = random.choice(self.players)
        self.choix=[[None,None,None],[None,None,None],[None,None,None]]

    async def interaction_check(self,interaction) -> bool:
        if interaction.user != self.turn:
            await interaction.response.send_message(content="Ce n'est pas encore ton tour !", ephemeral=True)
            return False
        return True

    def check_win(self) -> bool:
        last = None
        for player in self.players:
            for colonne in range(3):
                compteur_colonne = 0
                compteur_ligne = 0
                for ligne in range(3):
                    if self.choix[colonne][ligne] == player: 
                        compteur_colonne = compteur_colonne+1
                    if self.choix[ligne][colonne] == player:
                        compteur_ligne = compteur_ligne+1
                    if compteur_colonne == 3 or compteur_ligne ==3:
                        return True

            if self.choix[1][1] is not None: #Si il y'a un gagnant en diagonal, aucun des 3 sera nul, on en essaye qu'un
                if self.choix[0][0]==self.choix[1][1]==self.choix[2][2]:
                    return True
                elif self.choix[2][0]==self.choix[1][1]==self.choix[0][2]:
                    return True
        return False

    def check_draw(self) -> bool:
        compteur = 0
        for colonne in range(3):
            for ligne in range(3):
                if self.choix[colonne][ligne] is not None:
                    compteur = compteur + 1
        if compteur == 9:
            return True 
        else:
            return False      

class JoinInteraction(View):
    def __init__(self,ctx,user):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.user = user
        self.joined = False

    async def interaction_check(self,interaction) -> bool:
        if interaction.user == self.user:
            await interaction.response.send_message(content="Tu ne peut pas jouer contre toi même !", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        if not self.joined:
            await self.ctx.edit(content="L'invitation de jeu à expiré",embed=None,view=None,delete_after=5)
        else:
            pass
    
    @discord.ui.button(label="Rejoindre", style=discord.ButtonStyle.green)
    async def join_button_callback(self,button,interaction):
        joueurs = [interaction.user,self.ctx.user]
        morpion = MorpionInteraction(joueurs)
        await interaction.response.edit_message(content=f"Au tour de {morpion.turn.mention}",embed=None,view=morpion)
        self.joined = True

class Morpion(Cog):
    def __init__(self,bot):
        self.bot = bot

    @message_command(name="Morpion")
    async def user_morpion(self,interaction,message):
       embed = Embed(title="Invitation de jeu",description=f"{interaction.user.mention} à demarrer une partie de morpion !",)
       embed.set_thumbnail(url="https://cdn-icons.flaticon.com/png/512/2162/premium/2162800.png?token=exp=1641153114~hmac=812d76ba3675bac8799953adb7cbda5f")
       await interaction.response.send_message(embed=embed,view=JoinInteraction(interaction,interaction.user))

def setup(bot):
    bot.add_cog(Morpion(bot))