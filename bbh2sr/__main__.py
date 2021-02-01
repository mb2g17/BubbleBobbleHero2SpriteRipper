import sys

from PyQt5.QtWidgets import QApplication

from controllers.main import MainController


def main(args=None):
    app = QApplication(sys.argv)

    main_controller = MainController()
    main_controller.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main())
