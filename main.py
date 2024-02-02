import os
import sys

import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [900, 450]


class Example(QWidget):
    def __init__(self):

        self.sh, self.d = 37.5306, 55.7029

        self.zoom = 12  # 1, 2, 3, 4, ..., 19, 20

        self.map_type = "sat"

        self.kwargs = {
            "ll": f"{self.sh},{self.d}",
            "z": f"{self.zoom}",
            "l": f"{self.map_type}"
        }

        super().__init__()
        self.initUI()

    def setImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=self.kwargs)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setImage()

        self.line_sh, self.line_d, self.line_z = (
            QLineEdit(f"{self.sh}", self), QLineEdit(f"{self.d}", self), QLineEdit(f"{self.zoom}", self))

        [
            line.setPlaceholderText(text) for line, text in
            [(self.line_sh, "Ширина"), (self.line_d, "Долгота"), (self.line_z, "Увеличение")]
        ]

        [
            (line.setGeometry(625, 25 + (75 * index), 250, 50), line.setStyleSheet("font: bold 30px"), line.show())
            for index, line in enumerate([self.line_sh, self.line_d])]

        [
            (line.setGeometry(625, 175 + (75 * index), 250, 60), line.setStyleSheet("font: bold 40px"), line.show())
            for index, line in enumerate([self.line_z])
        ]

        self.button_update = QPushButton("Обновить", self)
        self.button_update.setGeometry(625, 275, 250, 50)
        self.button_update.clicked.connect(self.update_data)
        self.button_update.setStyleSheet("font: bold 35px")

        self.resize(*SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.image.show()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def update_data(self):
        self.sh = self.line_sh.text()
        self.d = self.line_d.text()
        self.zoom = self.line_z.text()

        self.image.hide()

        self.kwargs = {
            "ll": f"{self.sh},{self.d}",
            "z": f"{self.zoom}",
            "l": f"{self.map_type}"
        }

        self.initUI()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.line_z.setText(str(min([20, max([0, int(self.line_z.text()) - 1])])))
            self.update_data()

        if event.key() == Qt.Key_PageUp:
            self.line_z.setText(str(min([20, max([0, int(self.line_z.text()) + 1])])))
            self.update_data()


app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec())
