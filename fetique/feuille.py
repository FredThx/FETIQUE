#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QSpinBox
from PyQt5 import QtSvg
import svgwrite
from svgwrite import mm

class Feuille(QtSvg.QSvgWidget):
    '''Une représentation de la feuille à imprimer
    '''
    def __init__(self, parent = None, width = 210, height = 296):
        super(QtSvg.QSvgWidget, self).__init__(parent)
        self.f_width = width
        self.f_height = height
        self.setFixedSize(width*3, height*3)
        self.setStyleSheet("border: 1px solid black; border-radius: 10px;");


    def update(self, path_file, width, height, qty, marge = 5, maintain_ratio = True):
        dwg = svgwrite.Drawing('temp.svg', profile = 'tiny', size=(self.f_width*mm, self.f_height*mm))
        row = 0
        column = 0
        marge = 5
        for image_no in range(qty):
            try:
                image = svgwrite.image.Image(href = path_file,
                                            insert = (column*(width + marge)*mm, row*(height+marge)*mm),
                                            size = (width*mm, height*mm))
            except:
                image = svgwrite.text.Text("No picture!",
                                            insert = (column*(width + marge)*mm, (row+0.5)*(height+marge)*mm))
            else:
                if maintain_ratio:
                    image.fit()
                else:
                    image.stretch()
            dwg.add(image)
            column+=1
            if (1+column)*(width+marge)>self.f_width:
                column = 0
                row +=1
                if (1+row)*(height+marge)>self.f_height:
                    OUPS
        dwg.save()
        self.load('temp.svg')
