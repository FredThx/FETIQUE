from PyQt5.QtWidgets import QApplication
import fetique
import sys

app = QApplication([])
fetique = fetique.FetiqueApp()
sys.exit(app.exec())