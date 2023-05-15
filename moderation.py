import discord

class Moderation:
    def __init__(self):
        self.warnings = {}  # Dictionnaire pour stocker les avertissements des utilisateurs
        self.banned_words = ["mot1", "mot2", "mot3"]  # Liste des mots interdits
        self.max_warnings = 3  # Nombre maximum d'avertissements avant la suppression de l'utilisateur

    async def check_message(self, message):
        user_id = message.author.id

        # Vérifier si l'auteur du message est déjà dans les avertissements
        if user_id in self.warnings:
            self.warnings[user_id] += 1
        else:
            self.warnings[user_id] = 1

        # Vérifier si le nombre d'avertissements a atteint le seuil maximum
        if self.warnings[user_id] >= self.max_warnings:
            # Supprimer l'utilisateur
            user = message.author
            guild = message.guild
            await guild.ban(user)
            await message.channel.send(f"L'utilisateur {user.mention} a été banni pour utilisation abusive de mots interdits.")
        else:
            # Envoyer un avertissement au joueur
            await message.channel.send(f"{message.author.mention}, veuillez éviter d'utiliser des mots interdits. C'est votre avertissement n°{self.warnings[user_id]}.")

    def check_message_content(self, content):
        for word in self.banned_words:
            if word in content:
                return True
        return False

