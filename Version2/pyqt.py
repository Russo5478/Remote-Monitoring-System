import sys
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow:
    def __init__(self, core):
        self.core = core

        # Run main functions
        self.window_settings()

    def window_settings(self):
        self.core.setGeometry(100, 100, 100, 100)


def run_window():
    app = QApplication(sys.argv)
    window = QWidget()
    MainWindow(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_window()
