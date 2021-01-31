import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

# If you saved the template in `templates/main_window.ui`
ui = uic.loadUi("templates/main.ui")
ui.show()

# Then you can access the objects from the UI
# For example, if you had a label named label1
# ui.label1.setText('new text')

sys.exit(app.exec_())
