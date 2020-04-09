import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate, QDateTime
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp8_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_8_1.ui", self)
        self.data = data
        self.refreshAll()


    #fonction pour charger le combo du spéctacle
    @pyqtSlot()
    def refreshNoSpec(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT noSpec FROM LesTickets ")
        except Exception as e:
            self.ui.noSpec_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.noSpec_fct_combo, result)

    #Récupérer charger la date d'une representation selon le noSpec séléctionné
    @pyqtSlot()
    def refreshDateRep(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT dateRep FROM LesTickets WHERE noSpec = ?",
                                    [self.ui.noSpec_fct_combo.currentText()])
        except Exception as e:
            self.ui.dateRep_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.dateRep_fct_combo, result)




    #Charger le combo du noRang
    def refreshNoRang(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT noRang FROM LesTickets WHERE noSpec = ? AND dateRep = ?",
                     [self.ui.noSpec_fct_combo.currentText(), self.ui.dateRep_fct_combo.currentText()])
        except Exception as e:
            self.ui.noRang_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.noRang_fct_combo, result)

    #Charger les noPLace selon le noRang séléctionné
    def refreshNoPlace(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(" SELECT DISTINCT noPlace FROM LesTickets WHERE noSpec = ? AND dateRep = ? AND noRang = ?",
                                    [self.ui.noSpec_fct_combo.currentText(),self.ui.dateRep_fct_combo.currentText(),self.ui.noRang_fct_combo.currentText()])
        except Exception as e:
            self.ui.noPlace_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.noPlace_fct_combo, result)

    # Charger le combo du LibelleCat
    def refreshLibelleCat(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT libelleCat FROM LesTickets WHERE noSpec = ? AND dateRep = ? AND noPlace = ?  AND noRang = ?",
                    [self.ui.noSpec_fct_combo.currentText(), self.ui.dateRep_fct_combo.currentText(),self.ui.noPlace_fct_combo.currentText(),self.ui.noRang_fct_combo.currentText()]
            )
        except Exception as e:
            self.ui.libelleCat_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.libelleCat_fct_combo, result)


    #Charger le combo du noDos
    def refreshNoDos(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT  noDos FROM LesTickets WHERE noSpec = ? AND dateRep = ? AND noRang = ? AND noPlace = ?  AND  libelleCat = ?",
                                    [self.ui.noSpec_fct_combo.currentText(), self.ui.dateRep_fct_combo.currentText(),
                                     self.ui.noRang_fct_combo.currentText(), self.ui.noPlace_fct_combo.currentText(),
                                     self.ui.libelleCat_fct_combo.currentText()])
        except Exception as e:
            self.ui.noDos_fct_combo.clear()
        else:
            display.refreshGenericCombo(self.ui.noDos_fct_combo, result)

    #Affichage de la table des Tickets
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT * FROM LesTickets"
            )
        except Exception as e:
            self.ui.table_fct_comp.setRowCount(0)
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp, result)
            if i == 0:
                display.refreshLabel(self.ui.label_11, "Aucun résultat")


    #Fonction pour suprimer une reservation
    def Supprimer(self):
        try:
            cursor = self.data.cursor()
            #Supprimer la reservation séléctionnée
            cursor.execute( "DELETE FROM LesTickets WHERE noSpec = ? AND dateRep = ? AND noRang = ? AND noPlace = ?  AND  libelleCat = ? AND noDos = ?",
                                    [self.ui.noSpec_fct_combo.currentText(), self.ui.dateRep_fct_combo.currentText(),
                                     self.ui.noRang_fct_combo.currentText(), self.ui.noPlace_fct_combo.currentText(),
                                     self.ui.libelleCat_fct_combo.currentText(),self.ui.noDos_fct_combo.currentText()]
            )
            self.refreshAll()
        except Exception as e:
            display.refreshLabel(self.ui.label_11, "Impossible de supprimer : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_11, "Reservation supprimée")

    #Fonction pour modifier une reservation
    def Modifier(self):
        if self.ui.lineEdit_1.text().strip():
            noSpec = self.ui.lineEdit_1.text().strip()
        else:
            noSpec = self.ui.noSpec_fct_combo.currentText()

        if self.ui.lineEdit_2.text().strip():
            dateRep = self.ui.lineEdit_2.text().strip()
        else:
            dateRep = self.ui.dateRep_fct_combo.currentText()

        if self.ui.lineEdit_3.text().strip():
            noRang = self.ui.lineEdit_3.text().strip()
        else:
            noRang = self.ui.noRang_fct_combo.currentText()

        if self.ui.lineEdit_4.text().strip():
            noPlace = self.ui.lineEdit_4.text().strip()
        else:
            noPlace = self.ui.noPlace_fct_combo.currentText()

        if self.ui.lineEdit_5.text().strip():
            libelleCat = self.ui.lineEdit_5.text().strip()
        else:
            libelleCat = self.ui.libelleCat_fct_combo.currentText()

        if self.ui.lineEdit_6.text().strip():
            noDos = self.ui.lineEdit_6.text().strip()
        else:
            noDos = self.ui.noDos_fct_combo.currentText()

        try:
            cursor = self.data.cursor()
            # Update la reservation séléctionnée
            cursor.execute("UPDATE LesTickets SET noSpec = ?, dateRep = ?,  noRang = ? , noPlace = ?, libelleCat = ?, noDos = ? WHERE noSpec = ? AND dateRep = ? AND noRang = ? AND noPlace = ?  AND  libelleCat = ? AND noDos = ?",
                           [noSpec, dateRep,  noRang, noPlace, libelleCat, noDos,
                            self.ui.noSpec_fct_combo.currentText(), self.ui.dateRep_fct_combo.currentText(),
                            self.ui.noRang_fct_combo.currentText(), self.ui.noPlace_fct_combo.currentText(),
                            self.ui.libelleCat_fct_combo.currentText(), self.ui.noDos_fct_combo.currentText()])
            self.refreshAll()
        except Exception as e:
            display.refreshLabel(self.ui.label_11, "Modification Impossible : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_11, "l'operation est terminée avec succes")



    #Mettre a jour l'affichage de tous les composants dans la fenetre
    def refreshAll(self):
        self.refreshNoSpec()
        self.refreshDateRep()
        self.refreshNoPlace()
        self.refreshNoRang()
        self.refreshLibelleCat()
        self.refreshNoDos()
        self.refreshResult()

