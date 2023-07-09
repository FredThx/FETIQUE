#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QSpinBox
from PyQt5 import QtSvg
from PyQt5.QtGui import QPainter, QPixmap, QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt, QSize
import svgwrite
try:
    from .feuille import Feuille
    from .f_widgets import FSelectFile, FInputQSpinBox
    PATH = "fetique/"
except ModuleNotFoundError as e:
    print(e)
    from feuille import Feuille
    from f_widgets import FSelectFile, FInputQSpinBox
    PATH = ""
import sys, logging

class FetiqueApp(QMainWindow):

    def __init__(self, parent = None):
        super(FetiqueApp, self).__init__(parent)
        self.setWindowTitle("Fetique")
        self.icons_bt_maintain_ratio = (QIcon(PATH + "ratio_on"), QIcon(PATH + "ratio_off"))
        self.image_size = QSize()
        #Main
        main_layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        #Selection fichier
        self.qt_path_file = FSelectFile("Fichier étiquettes :")
        main_layout.addWidget(self.qt_path_file)
        self.qt_path_file.pathChanged.connect(self.on_file_changed)
        # Dimensions
        dimensions_layout = QHBoxLayout()
        main_layout.addLayout(dimensions_layout)
        dimensions_interior_layout = QVBoxLayout()
        dimensions_layout.addLayout(dimensions_interior_layout)
        ##largeur
        self.qt_witdh = FInputQSpinBox("Largeur  :", default_value = 50, suffix = " mm", min_value = 10, max_value = 210)
        dimensions_interior_layout.addWidget(self.qt_witdh)
        self.qt_witdh.valueChanged.connect(self.on_width_changed)
        ##hauteur
        self.qt_height = FInputQSpinBox("hauteur :", default_value = 40, suffix = " mm", min_value = 10, max_value = 297)
        dimensions_interior_layout.addWidget(self.qt_height)
        self.qt_height.valueChanged.connect(self.on_height_changed)
        ##Bouton maintain_ratio
        self.bt_maintain_ratio = QPushButton()
        self.bt_maintain_ratio.setIcon(self.icons_bt_maintain_ratio[0])
        self.is_maintain_ratio = True
        dimensions_layout.addWidget(self.bt_maintain_ratio)
        self.bt_maintain_ratio.clicked.connect(self.on_maintain_ratio_changed)
        #qté
        self.qt_qty = FInputQSpinBox("Nombre d'étiquettes :", default_value = 1)
        main_layout.addWidget(self.qt_qty)
        self.qt_qty.valueChanged.connect(self.update_feuille)
        #print
        bt_print = QPushButton("Imprime (mais...)")
        #main_layout.addWidget(bt_print)  "Disable!"
        bt_print.clicked.connect(self.print)
        #image
        self.feuille = Feuille()
        main_layout.addWidget(self.feuille)
        self.show()
        self.update_feuille()

    def on_maintain_ratio_changed(self):
        '''Gestion Changement
        '''
        self.is_maintain_ratio = not self.is_maintain_ratio
        self.bt_maintain_ratio.setIcon(self.icons_bt_maintain_ratio[0 if self.is_maintain_ratio else 1])
        if self.is_maintain_ratio:
            self.maintain_ratio()

    def on_file_changed(self):
        '''Quand le fichier image est modifié
        '''
        image = QPixmap(self.qt_path_file.path())
        self.image_size = image.size()
        self.maintain_ratio()
        self.update_feuille()

    def on_width_changed(self):
        #TODO : pb les valeurs sont des entiers!!!!
        if self.is_maintain_ratio:
            self.qt_height.blockSignals(True)
            self.qt_height.setValue(int(self.qt_witdh.value()*self.image_size.height()/self.image_size.width()))
            self.qt_height.blockSignals(False)
        self.update_feuille()

    def on_height_changed(self):
        #TODO : pb les valeurs sont des entiers!!!!
        if self.is_maintain_ratio:
            self.qt_witdh.blockSignals(True)
            self.qt_witdh.setValue(int(self.qt_height.value()*self.image_size.width()/self.image_size.height()))
            self.qt_witdh.blockSignals(False)
        self.update_feuille()

    def update_feuille(self):
        '''Met à jour l'image
        '''
        #print(f"self.qt_witdh.value() : {self.qt_witdh.value()}/t/tself.qt_height.value() : {self.qt_height.value()}")
        self.feuille.update(
            self.qt_path_file.path(),
            self.qt_witdh.value(),
            self.qt_height.value(),
            self.qt_qty.value())

    def maintain_ratio(self):
        '''Maintient l'aspect ratio de l'image
        '''
        size = QSize(self.image_size)
        size.scale(self.qt_witdh.value(),self.qt_height.value(), Qt.KeepAspectRatio)
        self.qt_witdh.setValue(int(size.width()))
        self.qt_height.setValue(int(size.height()))

    def print(self):
        '''Imprime l'image (mais ça ne fonctionne pas bien!!!)
        '''
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPaperSize(QPrinter.A4)
        printer.setPageSize(QPrinter.A4)
        printer.setPageMargins(5, 5, 5, 5, QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setColorMode(QPrinter.Color)
        dialog = QPrintDialog(printer)
        image = QPixmap('temp.svg')
        if dialog.exec_():
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

