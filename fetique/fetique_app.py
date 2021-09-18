#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QSpinBox
from PyQt5 import QtSvg
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt
import svgwrite
try:
    from .feuille import Feuille
    from .f_widgets import FSelectFile, FInputQSpinBox
except :
    from feuille import Feuille
    from f_widgets import FSelectFile, FInputQSpinBox
import sys, logging

class FetiqueApp(QMainWindow):

    def __init__(self, parent = None):
        super(FetiqueApp, self).__init__(parent)
        self.setWindowTitle("Fetique")
        #Main
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        #Selection fichier
        self.qt_path_file = FSelectFile("Fichier étiquettes :")
        main_layout.addWidget(self.qt_path_file)
        self.qt_path_file.pathChanged.connect(self.update_feuille)
        #largeur
        self.qt_witdh = FInputQSpinBox("Largeur en mm :", default_value = 50)
        main_layout.addWidget(self.qt_witdh)
        self.qt_witdh.valueChanged.connect(self.update_feuille)
        #hauteur
        self.qt_height = FInputQSpinBox("hauteur en mm :", default_value = 40)
        main_layout.addWidget(self.qt_height)
        self.qt_height.valueChanged.connect(self.update_feuille)
        #qté
        self.qt_qty = FInputQSpinBox("Nombre d'étiquettes :", default_value = 1)
        main_layout.addWidget(self.qt_qty)
        self.qt_qty.valueChanged.connect(self.update_feuille)
        #print
        bt_print = QPushButton("Imprime")
        main_layout.addWidget(bt_print)
        bt_print.clicked.connect(self.print)
        #image
        self.feuille = Feuille()
        main_layout.addWidget(self.feuille)
        self.show()
        self.update_feuille()


    def update_feuille(self):
        '''Met à jour l'image
        '''
        self.feuille.update(
            self.qt_path_file.path(),
            self.qt_witdh.value(),
            self.qt_height.value(),
            self.qt_qty.value())

    def print(self):
        '''Imprime l'image
        TODO : faire en SVF et non PNG (qui est dégeux)
        '''
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPaperSize(QPrinter.A4)
        printer.setPageSize(QPrinter.A4)
        printer.setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setColorMode(QPrinter.Color)
        dialog = QPrintDialog(printer)
        if dialog.exec_():
            image = QPixmap('temp.svg')
            painter = QPainter()
            painter.begin(printer)
            painter.setRenderHint(QPainter.Antialiasing)
            rect = painter.viewport()
            size = image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(image.rect())
            painter.drawPixmap(0, 0, image)
            painter.end()

if __name__ == "__main__":
    app = QApplication([])
    fetique = FetiqueApp()
    sys.exit(app.exec())
