import pickle
# stocker et convertir objet python dans un fichier

def sauvegarder_commandes(historique, filename):
    with open(filename, "wb") as file:
        pickle.dump(historique.tete, file)

def charger_commandes(historique, filename):
    with open(filename, "rb") as file:
        historique.tete = pickle.load(file)
        # Mettez à jour la queue si nécessaire (selon la structure de votre liste chaînée)
        # historique.queue = ...
