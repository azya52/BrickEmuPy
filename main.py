import sys
from PyQt6 import QtWidgets
from ui import Window
import multiprocessing

if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    app = QtWidgets.QApplication(sys.argv)

    try:
        with open("ui/style.css","r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError as e:
        print(e.strerror, e.filename)

    window = Window()
    window.show()
    sys.exit(app.exec())