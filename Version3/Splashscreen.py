import sys
import time
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow
from dlls.functions import center_window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("assets/Background.png"))
        self.resize(200, 300)
        center_window(self)

        self.test()

    def initialization(self):
        pass

    def close_splash(self):
        print("fin")
        main_window = MainWindow()
        main_window.show()
        self.finish(main_window)

    def test(self):
        timer = QTimer()
        timer.timeout.connect(lambda: self.close_splash())
        timer.start(3000)

    def run(self, message: str):
        self.showMessage(f"{message}", alignment=Qt.AlignBottom | Qt.AlignHCenter, color=Qt.white)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
