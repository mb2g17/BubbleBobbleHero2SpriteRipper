import sys

from PyQt5.QtWidgets import QApplication

from controllers.main import MainController


def main(args=None):
    app = QApplication(sys.argv)

    # If you saved the template in `templates/main_window.ui`
    main_controller = MainController()
    main_controller.show()

    # Then you can access the objects from the UI
    # For example, if you had a label named label1
    # ui.label1.setText('new text')

    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main())
