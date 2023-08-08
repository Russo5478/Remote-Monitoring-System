from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtWidgets import QStyle, QHeaderView, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from dlls.functions import database_all_lookup


class NoHeaderHighlightHeaderView(QHeaderView):
    def paintSection(self, painter, rect, logicalIndex):
        option = self.viewOptions()
        option.state &= ~QStyle.State_Selected
        super().paintSection(painter, rect, logicalIndex)


class CustomDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        row = index.row()
        if row % 2 == 0:
            option.backgroundBrush = QColor(240, 240, 240)  # Light gray
        else:
            option.backgroundBrush = QColor(220, 220, 220)


class Monitoring:
    def __init__(self, tab_widget):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        tab_widget.setLayout(self.main_layout)

        self.create_table()

    def create_table(self):
        table = QTableWidget()
        table.setRowCount(100)
        table.setColumnCount(11)
        self.main_layout.addWidget(table)

        column_headers = ['Computer Name', 'IP Address', 'MAC Address', 'Remark', 'Windows Account', 'Group',
                          'Connect time', 'Status', 'RXD Speed', 'TXD Speed', 'Events']

        values = database_all_lookup('assets/master.db', "*", "Dashboard")

        for row_idx, row_data in enumerate(values):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                table.setItem(row_idx, col_idx, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # for j in range(table.rowCount()):
        #     table.item(table.rowCount, j).setBackground(Qt.lightGray)

        header_view = NoHeaderHighlightHeaderView(Qt.Horizontal)
        table.setHorizontalHeader(header_view)

        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)

        table.setHorizontalHeaderLabels(column_headers)

        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 150)
        table.setColumnWidth(5, 100)
        table.setColumnWidth(6, 150)
        table.setColumnWidth(7, 100)
        table.setColumnWidth(8, 100)
        table.setColumnWidth(9, 100)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)

        # table.setStyleSheet(
        #     "QScrollBar:vertical, QScrollBar:horizontal { background: #323644; }"
        #     "QScrollBar:handle:vertical, QScrollBar:handle:horizontal { background: #323644; }"
        # )

        header_style = """
            QHeaderView::section {
                background-color: #ededed;
                font: yu gothic ui 100px;
                padding: 0px;
                border-bottom: 2px solid #000;
            }
        """
        table.horizontalHeader().setStyleSheet(header_style)

        cell_style = """            
            QTableWidget::item {
                padding: 0px;  /* Set the padding */
                border-right: 0px dotted transparent;
                border-bottom: 2px solid #6D7594;
            }

            QTableWidget::item:selected {
                color: #000;
                background-color: #33CCFF;  /* Set the background color for the selected tab */
            }
        """
        table.setStyleSheet(cell_style)
        table.setSelectionBehavior(QTableWidget.SelectRows)

        # Set custom row height for all rows
        custom_row_height = 1  # Adjust the value as needed
        for row in range(table.rowCount()):
            table.verticalHeader().setDefaultSectionSize(custom_row_height)
