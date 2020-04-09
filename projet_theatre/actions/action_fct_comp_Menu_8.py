import sqlite3

from actions.action_fct_comp_8 import AppFctComp8
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import  sqlite3

# Classe permettant d'afficher la fonction à compléter 1
from actions.action_fct_comp_8_1 import AppFctComp8_1


class AppFctCompMenu8(QDialog):
    fct_comp_8_dialog = None
    fct_comp_8_1_dialog = None
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_Menu_8.ui", self)
        self.data = data

    def open_fct_comp_8(self):
        window = AppFctComp8(self.data)
        window.show()

    def open_fct_comp_8_1(self):
        window1 = AppFctComp8_1(self.data)
        window1.show()