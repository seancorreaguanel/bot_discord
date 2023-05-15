import discord
from discord.ext import commands
from historique_liste_chainee import HistoriqueCommandes
import arbre_discussion
import sauvegarder as sauvegarder
from moderation import Moderation
import requests



intents = discord.Intents.all()
client = commands.Bot(command_prefix="/", intents=intents)

historique = HistoriqueCommandes()  # Crée une instance de la classe HistoriqueCommandes
moderation = Moderation()

banned_words = ["mot1", "mot2"]  # Liste des mots interdits
warnings = {}  # Dictionnaire pour stocker les avertissements des utilisateurs

@client.event 
async def on_message(message):
    if not message.author.bot:
        content = message.content.lower()
        for word in banned_words:
            if word in content:
                await warn_user(message.author)
                await moderation.ban_user(message.author, message.guild)  # Utilise la méthode ban_user de la classe Moderation
                break
    await client.process_commands(message)

async def warn_user(user):
    if user.id not in warnings:
        warnings[user.id] = 1
        await user.send("Attention : L'utilisation de mots interdits est interdite sur ce serveur. C'est votre premier avertissement.")
    else:
        warnings[user.id] += 1
        if warnings[user.id] == 2:
            await user.send("Attention : Vous avez utilisé des mots interdits à plusieurs reprises. C'est votre deuxième avertissement.")
        elif warnings[user.id] == 3:
            await user.send("Attention : Vous avez utilisé des mots interdits à plusieurs reprises. C'est votre troisième et dernier avertissement. Vous allez être banni du serveur.")


# Création de l'instance du bot de conversation
bot_conversation = arbre_discussion.ConversationBot()
bot_conversation.add_topic("sport")
bot_conversation.add_topic("sante")
bot_conversation.create_tree()

@client.event
async def on_message(message):
    global last_command
    await client.process_commands(message)

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command(name="bonjour")
async def dire_bonjour(ctx):
    await ctx.send("Bonjour, je suis un bot codé par Sean pour faciliter votre vie dans le discord")

@client.command(name="capacites")
async def afficher_capacites(ctx):
    await ctx.send("Je suis un bot capable de stocker vos commandes, d'avoir une discussion avec vous, d'afficher des images de chat et chien ectt")

@client.command(name="derniere_commande")
async def afficher_derniere_commande(ctx):
    derniere_commande = historique.obtenir_derniere_commande()
    await ctx.send(f"Dernière commande : {derniere_commande}")
    # Ajouter la commande à l'historique
    historique.ajouter_commande(ctx.message.content, ctx.author.id)

@client.command(name="commandes_utilisateur")
async def afficher_commandes_utilisateur(ctx):
    utilisateur = ctx.author.id
    commandes_utilisateur = historique.obtenir_commandes_utilisateur(utilisateur)
    response = f"Commandes de l'utilisateur {utilisateur} :"
    for commande in commandes_utilisateur:
        response += f"\n- {commande}"
    await ctx.send(response)
    # Ajouter la commande à l'historique
    historique.ajouter_commande(ctx.message.content, ctx.author.id)

@client.command(name="deplacer_suivant")
async def deplacer_suivant(ctx):
    historique.deplacer_suivant()
    await ctx.send("Déplacement vers la commande suivante effectué")
    historique.ajouter_commande(ctx.message.content, ctx.author.id)


@client.command(name="deplacer_precedent")
async def deplacer_precedent(ctx):
    historique.deplacer_precedent()
    await ctx.send("Déplacement vers la commande précédente effectué")
    historique.ajouter_commande(ctx.message.content, ctx.author.id)


@client.command(name="vider_historique")
async def vider_historique(ctx):
    historique.vider_historique()
    await ctx.send("L'historique des commandes a été vidé")
    historique.ajouter_commande(ctx.message.content, ctx.author.id)


@client.command(name="start")
async def start_conversation(ctx):
    response = bot_conversation.start()
    await ctx.send(response)


@client.command(name="process_response")
async def process_bot_response(ctx, *, user_input):
    async with ctx.typing():
        bot_response = bot_conversation.process_input(user_input)
        await ctx.send(bot_response)
    
@client.command(name="save")
async def save_history(ctx):
    sauvegarder.sauvegarder_commandes(historique, "command.txt")
    await ctx.send("L'historique des commandes a été sauvegardé.")

@client.command(name="load")
async def charger_commandes(ctx):
    nom_fichier = "command.txt"
    sauvegarder.charger_commandes(historique, nom_fichier)
    await ctx.send(f"L'historique des commandes a été chargé depuis le fichier {nom_fichier}.")

@client.command(name="image")
async def send_random_image(ctx, keyword):
    if keyword.lower() == "chat":
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        image_url = data[0]["url"]
        await ctx.send(image_url)
    elif keyword.lower() == "chien":
        response = requests.get("https://random.dog/woof.json")
        data = response.json()
        image_url = data["url"]
        await ctx.send(image_url)
    else:
        await ctx.send("Désolé, je ne peux vous fournir que des images de chats ou de chiens.")


client.run("MTA5MTI1OTQzMjM5MTk1MDQ0Nw.GSANbX.vBQ20zEUnJkR1UPOZFTtcy_X5rIQvCKwRakrlU")
