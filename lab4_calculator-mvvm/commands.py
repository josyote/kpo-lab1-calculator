from abc import ABC, abstractmethod
import math


class Command(ABC):
    """Classe abstraite pour le pattern Command"""

    @abstractmethod
    def execute(self):
        """Exécute la commande"""
        pass

    @abstractmethod
    def undo(self):
        """Annule la commande"""
        pass


class CalculateCommand(Command):
    """Commande pour effectuer un calcul"""

    def __init__(self, model, expression: str):
        self.model = model
        self.expression = expression
        self.result = None
        self.previous_state = None

    def execute(self):
        """Exécute le calcul"""
        try:
            self.result = self.model.evaluate(self.expression)
            return str(self.result)
        except Exception as e:
            return f"Erreur: {str(e)}"

    def undo(self):
        """Annule le calcul (retourne 0)"""
        return "0"


class FunctionCommand(Command):
    """Commande pour appliquer une fonction mathématique"""

    def __init__(self, model, func: str, value: float):
        self.model = model
        self.func = func
        self.value = value
        self.result = None

    def execute(self):
        """Exécute la fonction"""
        try:
            self.result = self.model.apply_function(self.func, self.value)
            return str(self.result)
        except Exception as e:
            return f"Erreur: {str(e)}"

    def undo(self):
        """Annule la fonction (retourne 0)"""
        return "0"


class ClearCommand(Command):
    """Commande pour effacer tout"""

    def __init__(self, view_model):
        self.view_model = view_model
        self.previous_expression = ""
        self.previous_history = []

    def execute(self):
        """Efface tout"""
        self.previous_expression = self.view_model.current_expression
        self.previous_history = self.view_model.history.copy()
        self.view_model.current_expression = ""
        self.view_model.history = []
        self.view_model.result_shown = False
        self.view_model.last_result = ""
        return "0"

    def undo(self):
        """Restaure l'état précédent"""
        self.view_model.current_expression = self.previous_expression
        self.view_model.history = self.previous_history.copy()
        return self.previous_expression if self.previous_expression else "0"


class BackspaceCommand(Command):
    """Commande pour supprimer le dernier caractère"""

    def __init__(self, view_model):
        self.view_model = view_model
        self.previous_expression = ""

    def execute(self):
        """Supprime le dernier caractère"""
        self.previous_expression = self.view_model.current_expression
        if self.view_model.current_expression:
            self.view_model.current_expression = self.view_model.current_expression[:-1]
        return self.view_model.current_expression if self.view_model.current_expression else "0"

    def undo(self):
        """Restaure le caractère supprimé"""
        self.view_model.current_expression = self.previous_expression
        return self.previous_expression if self.previous_expression else "0"