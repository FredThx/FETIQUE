#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QSpinBox
from PyQt5.QtCore import pyqtSignal


class FSelectFile(QWidget):
    '''Un champ selecteur de fichier
    '''
    pathChanged = pyqtSignal(name = "pathChanged")

    def __init__(self, text, parent = None, text_button = "Ouvrir Fichier", text_dialog = "Open a file", file_types = "All Files (*.*)"):
        super(QWidget, self).__init__(parent)
        self.text_button = text_button
        self.text_dialog = text_dialog
        self.file_types = file_types
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel(text))
        self.path_file = QLineEdit()
        layout.addWidget(self.path_file)
        self.path_file.textChanged.connect(self.on_path_changed)
        bt_open_file = QPushButton(text_button)
        layout.addWidget(bt_open_file)
        bt_open_file.clicked.connect(self.open_file)

    def on_path_changed(self):
        self.pathChanged.emit()

    def open_file(self):
        '''Open a QFileDialog
        '''
        path = QFileDialog.getOpenFileName(self, self.text_dialog, '', self.file_types)
        if path !=('',''):
            self.path_file.setText(path[0])

    def path(self):
        return self.path_file.text()

class FInputQSpinBox(QWidget):
    '''Un champ SpinBox
    '''
    valueChanged = pyqtSignal(name = "valueChanged")

    def __init__(self, text, parent=None, default_value = 0, min_value = None, max_value = None, suffix = None):
        super(QWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel(text))
        self.sp_value = QSpinBox()
        if suffix:
            self.sp_value.setSuffix(suffix)
        self.sp_value.setValue(default_value)
        if min_value:
            self.sp_value.setMinimum(min_value)
        if max_value:
            self.setMaximum(max_value)
        layout.addWidget(self.sp_value)
        self.sp_value.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self):
        self.valueChanged.emit()

    def value(self):
        return self.sp_value.value()
    def setValue(self, value):
        self.sp_value.setValue(value)
