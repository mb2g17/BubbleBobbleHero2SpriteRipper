from PyQt5 import uic


class MainController:
    def __init__(self):
        self._load_view()

    def _load_view(self):
        ui = uic.loadUi("templates/main.ui")
        self.ui = ui

    def show(self):
        self.ui.show()
