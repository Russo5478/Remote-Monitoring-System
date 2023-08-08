from PyQt5.QtWidgets import QDesktopWidget
from sqlite3 import connect


def center_window(window):
    screen_geometry = QDesktopWidget().screenGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y - 30)


def database_all_lookup(db_path: str, what_selection: str, from_selection: str):
    db_connection = connect(db_path)
    writer = db_connection.cursor()
    lookup_command = "SELECT {} FROM {}".format(what_selection, from_selection)
    writer.execute(lookup_command)
    result = writer.fetchall()
    db_connection.close()

    return result
