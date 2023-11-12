import sys
from PyQt6 import QtWidgets
from ui import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    try:
        with open("ui/style.css","r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError as e:
        print(e.strerror, e.filename)

    Window().show()
    sys.exit(app.exec())