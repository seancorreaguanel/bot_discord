class TreeNode:
    def __init__(self, question, yes_node=None, no_node=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node


class ConversationBot:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.topic_list = set()

    def add_topic(self, topic):
        self.topic_list.add(topic)

    def create_tree(self):
        # Niveau 1
        root_question = "Avez-vous besoin d'aide ?"

        # Niveau 2
        question1 = "Avez-vous des questions sur le sport ?"
        question2 = "Avez-vous des questions sur la santé ?"

        # Niveau 3 - Sport
        question3 = "Voulez-vous des informations sur des sports spécifiques ?"
        question4 = "Voulez-vous des conseils d'entraînement ?"

        # Niveau 3 - Santé
        question5 = "Voulez-vous des informations sur une condition de santé spécifique ?"
        question6 = "Voulez-vous des conseils pour maintenir une bonne santé ?"

        # Création de l'arbre binaire
        node3 = TreeNode(question3)
        node4 = TreeNode(question4)

        node5 = TreeNode(question5)
        node6 = TreeNode(question6)

        node1 = TreeNode(question1, node3, node4)
        node2 = TreeNode(question2, node5, node6)

        self.root = TreeNode(root_question, node1, node2)
        self.current_node = self.root


    def reset_conversation(self):
        self.current_node = self.root

    def process_input(self, user_input):
        if user_input.lower() == "reset":
            self.reset_conversation()
            return "La conversation a été réinitialisée. Comment puis-je vous aider ?"

        if user_input.lower().startswith("speak about"):
            topic = user_input[11:]
            if topic.lower() in self.topic_list:
                return f"Oui, je peux vous parler de {topic}. Quelle est votre question à ce sujet ?"
            else:
                return f"Désolé, je ne peux pas vous parler de {topic}."

        if user_input.lower() == "help":
            return self.start()


        if self.current_node is None:
            return "La conversation a atteint une impasse. Veuillez réinitialiser la conversation."
        
        if self.current_node.yes_node is None and self.current_node.no_node is None:
            return f"Votre besoin est : {self.current_node.question}. Comment puis-je vous aider ?"

        if user_input.lower() == "oui" and self.current_node.yes_node:
            self.current_node = self.current_node.yes_node
        elif user_input.lower() == "non" and self.current_node.no_node:
            self.current_node = self.current_node.no_node
        else:
            return "Je ne comprends pas votre réponse. Veuillez répondre par 'oui' ou 'non'."

        

        return self.current_node.question

    def start(self):
        self.current_node = self.root
        return self.current_node.question
    
    def main():
        bot = ConversationBot()
        bot.add_topic("sante")
        bot.add_topic("sport")
        bot.create_tree()

        print("Bienvenue dans la conversation avec le bot. Tapez 'help' pour commencer.")
        while True:
            user_input = input("Vous: ")
            bot_response = bot.process_input(user_input)
            print("Bot:", bot_response)

    if __name__ == "__main__":
        main()
