import pickle
from threading import Lock


class CommandNode:
    def __init__(self, commande, utilisateur):
        self.commande = commande
        self.utilisateur = utilisateur
        self.suivant = None
        self.precedent = None

class UserHistory:
    def __init__(self, user_id):
        self.user_id = user_id
        self.commands = []

    def get_user_commands(self, user_id):
        if self.user_id == user_id:
            return self.commands
        return []

    def set_user_commands(self, user_id, commands):
        if self.user_id == user_id:
            self.commands = commands

class HistoriqueCommandes:
    def __init__(self):
        self.tete = None
        self.queue = None
        self.lock = Lock()
        self.exclude_lock = False

    def ajouter_commande(self, commande, utilisateur):
        noeud = CommandNode(commande, utilisateur)
        with self.lock:
            if not self.tete:
                self.tete = noeud
                self.queue = noeud
            else:
                noeud.precedent = self.queue
                self.queue.suivant = noeud
                self.queue = noeud

    def obtenir_derniere_commande(self):
        with self.lock:
            if self.queue:
                return self.queue.commande
            return None

    def obtenir_commandes_utilisateur(self, utilisateur):
        commandes_utilisateur = []
        with self.lock:
            noeud = self.tete
            while noeud:
                if noeud.utilisateur == utilisateur:
                    commandes_utilisateur.append(noeud.commande)
                noeud = noeud.suivant
        return commandes_utilisateur

    def deplacer_suivant(self):
        with self.lock:
            if self.queue and self.queue.suivant:
                self.queue = self.queue.suivant

    def deplacer_precedent(self):
        with self.lock:
            if self.queue and self.queue.precedent:
                self.queue = self.queue.precedent

    def vider_historique(self):
        with self.lock:
            self.tete = None
            self.queue = None

    def __getstate__(self):
        state = self.__dict__.copy()
        if state['exclude_lock']:
            del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.exclude_lock:
            self.lock = Lock()
            self.exclude_lock = False
