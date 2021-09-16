#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QSpinBox
from PyQt5 import QtSvg
from PyQt5.QtGui import QPixmap
import svgwrite
from svgwrite import mm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class Feuille(QWidget):
    '''Une représentation de la feuille à imprimer
    '''
    def __init__(self, parent = None, width = 210, height = 296):
        super(QWidget, self).__init__(parent)
        self.f_width = width
        self.f_height = height
        self.setFixedSize(width*2.5, height*2.5)
        #self.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.label = QLabel(self)




    def update(self, path_file, width, height, qty, marge = 5, maintain_ratio = True):
        dwg = svgwrite.Drawing('temp.svg', profile = 'tiny', size=(self.f_width*mm, self.f_height*mm))
        row, column, marge = 0,0,5

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
        drawing = svg2rlg('temp.svg')
        renderPM.drawToFile(drawing, 'temp.png', fmt='PNG')
        image = QPixmap('temp.png')
        self.label.setPixmap(image)
        self.label.adjustSize()
        self.resize(image.width(), self.height())
