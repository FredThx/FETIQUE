from PyQt5.QtWidgets import QApplication
from fetique.fetique_app import FetiqueApp
import sys

app = QApplication([])
fetique = FetiqueApp()
sys.exit(app.exec())