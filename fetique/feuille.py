#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QWidget, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import svgwrite
from svgwrite import mm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import subprocess, os, platform

class Feuille(QWidget):
    '''Une représentation de la feuille à imprimer
    '''
    def __init__(self, parent = None, width = 210, height = 297, svg_temp_file = "temp.svg", png_temp_file = "temp.png"):
        super(QWidget, self).__init__(parent)
        self.svg_temp_file = svg_temp_file
        self.png_temp_file = png_temp_file
        self.f_width = width
        self.f_height = height
        self.setFixedSize(width*1.5, height*1.5) #TODO: mettre un zoom
        self.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.label = QLabel(self)
        self.image = None

    def update(self, path_file, width, height, qty, marge = 5, maintain_ratio = True):
        dwg = svgwrite.Drawing(self.svg_temp_file, profile = 'tiny', size=(self.f_width*mm, self.f_height*mm))
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
                    pass
        dwg.save()
        drawing = svg2rlg(self.svg_temp_file)
        renderPM.drawToFile(drawing, self.png_temp_file, fmt='PNG')
        self.image = QPixmap(self.png_temp_file)
        self.label.setPixmap(self.image.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        self.label.adjustSize()
        #self.label.resize(self.width(), self.height())
        #self.resize(self.image.width(), self.image.height())


    def contextMenuEvent(self, event):
        '''Menu contextuel de la feuille
        '''
        contextMenu = QMenu(self)
        export = contextMenu.addAction("Exporter en SVG")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == export:
            self.open_svg()


    def open_svg(self):
        '''Ouvre le ficher svg avec l'application par defaut de l'os
        '''
        filepath = self.svg_temp_file
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))