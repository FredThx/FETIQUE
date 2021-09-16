#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
import sys

import fetique

app = QApplication([])
fetique = fetique.FetiqueApp()
sys.exit(app.exec())
