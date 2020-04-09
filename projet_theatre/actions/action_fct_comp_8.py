import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate, QDateTime
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp8(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_8.ui", self)
        self.data = data
        self.refreshcomboSpec()
        self.refreshDateRep()
        self.refreshNoRang()
        self.refreshNoPlace()
        self.refreshNoDos()
        self.refreshLibelleCat()
        self.Reserver()
        self.refreshResult()
        self.ui.label_11.clear()


    # Fonction de mise à jour de l'affichage


    #fonction pour charger le combo du spéctacle
    @pyqtSlot()
    def refreshcomboSpec(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec FROM LesSpectacles ")
        except Exception as e:
            self.ui.NoSpec_fct_combo_8_1.clear()
        else:
            display.refreshGenericCombo(self.ui.NoSpec_fct_combo_8_1, result)


    #Récupérer charger la date d'une representation selon le noSpec séléctionné
    @pyqtSlot()
    def refreshDateRep(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT dateRep FROM LesRepresentations_base WHERE noSpec = ?",
                                    [self.ui.NoSpec_fct_combo_8_1.currentText()])
        except Exception as e:
            self.ui.dateRep_fct_combo_8_2.clear()
        else:
            display.refreshGenericCombo(self.ui.dateRep_fct_combo_8_2, result)


    #fonction pour charger le combo du NoRang
    def refreshNoRang(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT noRang FROM lesPlaces ")
        except Exception as e:
            self.ui.NoRang_fct_combo_8_3.clear()
        else:
            display.refreshGenericCombo(self.ui.NoRang_fct_combo_8_3, result)


    #Charger les NoPLace selon le noRang séléctionné
    def refreshNoPlace(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT noPlace FROM LesPlaces WHERE noRang = ?",
                                    [self.ui.NoRang_fct_combo_8_3.currentText()])
        except Exception as e:
            self.ui.NoPlace_fct_combo_8_4.clear()
        else:
            display.refreshGenericCombo(self.ui.NoPlace_fct_combo_8_4, result)



    #Charger le combo du noDos
    def refreshNoDos(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noDos FROM LesDossiers_base ")
        except Exception as e:
            self.ui.NoDos_fct_combo_8_5.clear()
        else:
            display.refreshGenericCombo(self.ui.NoDos_fct_combo_8_5, result)

    # Charger le combo du LibelleCat
    def refreshLibelleCat(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT libelleCat FROM LesCategoriesTickets ")
        except Exception as e:
            self.ui.fct_combo_8_12.clear()
        else:
            display.refreshGenericCombo(self.ui.fct_combo_8_12, result)

    #Reserver
    def Reserver(self):
            try:
                # Récupérer la date courante
                cursor = self.data.cursor()
                d = QDateTime.currentDateTime()
                cursor.execute(
                    "INSERT INTO LesTickets VALUES(?,?,?,?,?,?,?)",
                    [self.ui.NoSpec_fct_combo_8_1.currentText(), self.ui.dateRep_fct_combo_8_2.currentText(),
                     self.ui.NoPlace_fct_combo_8_4.currentText(), self.ui.NoRang_fct_combo_8_3.currentText(),
                     d.toString("dd/MM/yyyy hh:mm"), self.ui.fct_combo_8_12.currentText(), self.ui.NoDos_fct_combo_8_5.currentText()]
                )
            except Exception as e:
                display.refreshLabel(self.ui.label_11, "Cette place est deja reservee ")
            else:
                display.refreshLabel(self.ui.label_11, "L'operation est terminee avec succes")

    #Affichage de la table des Tickets
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT * FROM LesTickets"
            )
        except Exception as e:
            self.ui.table_fct_comp_8.setRowCount(0)
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_8, result)
            if i == 0:
                display.refreshLabel(self.ui.label_11, "Aucun résultat")


