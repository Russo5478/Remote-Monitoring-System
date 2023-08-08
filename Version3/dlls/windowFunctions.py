from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon


def create_image_button(size: int, layout, tooltip: str, path: str, wxh: int):
    btn_button = QPushButton("")
    btn_button.setFixedHeight(size)
    btn_image = QPixmap(path).scaled(wxh, wxh)
    btn_icon = QIcon(btn_image)
    btn_button.setIcon(btn_icon)
    btn_button.setIconSize(btn_image.size())
    btn_button.setToolTip(tooltip)
    btn_button.setFlat(True)
    layout.addWidget(btn_button)

    return btn_button
