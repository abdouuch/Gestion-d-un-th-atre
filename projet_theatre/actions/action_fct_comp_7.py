import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import uic, QtCore



# Classe permettant d'afficher la fonction à compléter 1
class AppFctComp7(QDialog):
    # Création d'un signal destiné à être émis lorsque la table est modifiée
    changedValue = pyqtSignal()

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_7.ui", self)
        self.data = data
        self.refreshNoSpec()
        self.refreshResult()
        self.setDateTime()

    def setDateTime(self):
        self.ui.dateRepEdit_fct_comp_7_1.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateRepEdit_fct_comp_7_2.setDateTime(QtCore.QDateTime.currentDateTime())


    # Fonction de mise à jour des spectacles
    def refreshNoSpecAdd(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec FROM LesSpectacles")
        except Exception as e:
            self.ui.noSpec_fct_combo_7_1.clear()
        else:
            display.refreshGenericCombo(self.ui.noSpec_fct_combo_7_1, result)

    def refreshNoSpecDelete(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec FROM LesSpectacles")
        except Exception as e:
            self.ui.noSpec_fct_combo_7_2_1.clear()
        else:
            display.refreshGenericCombo(self.ui.noSpec_fct_combo_7_2_1, result)

    def refreshNoSpecEdit(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec FROM LesSpectacles")
        except Exception as e:
            self.ui.noSpec_fct_combo_7_2_2.clear()
        else:
            display.refreshGenericCombo(self.ui.noSpec_fct_combo_7_2_2, result)

    # Récupérer charger la date d'une representation selon le noSpec séléctionné
    @pyqtSlot()
    def refreshDateRep(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT dateRep, promoRep FROM LesRepresentations_base WHERE noSpec = ?",
                                    [self.ui.noSpec_fct_combo_7_2_1.currentText()])
        except Exception as e:
            self.ui.dateRep_combo_fct_comp_7_2.clear()
        else:
            display.refreshGenericCombo(self.ui.dateRep_combo_fct_comp_7_2, result)


    @pyqtSlot()
    def refreshPromoRep(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT promoRep FROM LesRepresentations_base WHERE noSpec = ? AND dateRep = ? ",
                                    [self.ui.noSpec_fct_combo_7_2_1.currentText(),
                                     self.ui.dateRep_combo_fct_comp_7_2.currentText()])
        except Exception as e:
            self.ui.dateRep_combo_fct_comp_7_2.clear()
        else:
            # display.refreshGenericCombo(self.ui.dateRep_combo_fct_comp_7_2, result)
            display.refreshGenericineEdit(self.ui.promoRep_lineEdit_fct_comp_7_2_2,  result)

    def refreshNoSpec(self):
        self.refreshNoSpecAdd()
        self.refreshNoSpecDelete()
        self.refreshNoSpecEdit()


    @pyqtSlot()
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT noSpec,dateRep, promoRep, nbrPlacesDisp FROM LesRepresentations")
        except Exception as e:
            self.ui.table_fct_comp_7.setRowCount(0)
            display.refreshLabel(self.ui.message_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_7, result)
            if i == 0:
                display.refreshLabel(self.ui.message_fct_comp_7, "Aucun résultat")



    @pyqtSlot()
    # Fonction permettant d'ajouter une nouvelle représentation
    def addRepresentation(self):
        try:
            dt = self.ui.dateRepEdit_fct_comp_7_1.dateTime()
            dt_string = dt.toString(self.ui.dateRepEdit_fct_comp_7_1.displayFormat())
            cursor = self.data.cursor()
            cursor.execute(
                "INSERT INTO LesRepresentations_base(noSpec, dateRep, promoRep) VALUES (?, ?, ?)",
                [self.ui.noSpec_fct_combo_7_1.currentText(),
                 dt_string,
                 self.ui.promoRep_lineEdit_fct_comp_7_1.text().strip()]
            )
        except Exception as e:
            # self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.message_fct_comp_7, "" + repr(e))
        else:
            self.data.commit()
            display.refreshLabel(self.ui.message_fct_comp_7, "Ajout réussi")
            self.refreshResult()
            self.refreshNoSpecAdd()

    @pyqtSlot()
    def editRepresentation(self):
        try:
            dt = self.ui.dateRepEdit_fct_comp_7_2.dateTime()
            dt_string = dt.toString(self.ui.dateRepEdit_fct_comp_7_2.displayFormat())
            cursor = self.data.cursor()
            cursor.execute(
                "UPDATE LesRepresentations_base SET noSpec = ?, dateRep = ? , promoRep = ? "
                "WHERE noSpec = ? AND dateRep = ?",
                [self.ui.noSpec_fct_combo_7_2_2.currentText(),
                 dt_string,
                 self.ui.promoRep_lineEdit_fct_comp_7_2.text().strip(),
                 self.ui.noSpec_fct_combo_7_2_1.currentText(),
                 self.ui.dateRep_combo_fct_comp_7_2.currentText()]
                )
        except Exception as e:
            display.refreshLabel(self.ui.message_fct_comp_7, "" + repr(e))
        else:
            display.refreshLabel(self.ui.message_fct_comp_7, "Mise à jour réussie ")
            self.data.commit()
            self.refreshResult()

    @pyqtSlot()
    def deleteRepresentation(self):
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "DELETE FROM LesRepresentations_base WHERE noSpec = ? AND dateRep = ? ",
                [self.ui.noSpec_fct_combo_7_2_1.currentText(),
                 self.ui.dateRep_combo_fct_comp_7_2.currentText()]
                )
        except Exception as e:
            display.refreshLabel(self.ui.message_fct_comp_7, "Impossible de supprimer : " + repr(e))
        else:
            display.refreshLabel(self.ui.message_fct_comp_7, "Suppression réussie ")
            self.data.commit()
            self.refreshResult()