#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys

import fetique

app = QApplication([])
fetique = fetique.FetiqueApp()
fetique.setWindowIcon(QIcon("icon.png"))
sys.exit(app.exec())
