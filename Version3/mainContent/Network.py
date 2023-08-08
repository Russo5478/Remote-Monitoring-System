from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QFrame, QSplitter
from PyQt5.QtCore import Qt
from dlls.functions import database_all_lookup


class NetTable:
    def __init__(self, tab_widget):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        tab_widget.setLayout(self.main_layout)

        self.create_table()

    def create_table(self):
        separator_frame = QFrame()
        separator_frame.setStyleSheet("background-color: #414657;")
        separator_frame.setFixedHeight(20)
        self.main_layout.addWidget(separator_frame)

        table = QTableWidget()
        self.main_layout.addWidget(table)

        column_headers = ['IP Address', 'MAC Address', 'Hostname', 'Status', 'Vendor']

        sample_data = [
            ['192.168.1.100', '00:11:22:33:44:55', 'SampleHost1', 'Up', 'Vendor1'],
            ['192.168.1.101', 'AA:BB:CC:DD:EE:FF', 'SampleHost2', 'Down', 'Vendor2'],
            ['192.168.1.102', '11:22:33:44:55:66', 'SampleHost3', 'Unknown', 'Vendor3'],
        ]

        table.setRowCount(len(sample_data) + 100)
        table.setColumnCount(len(column_headers))

        for row_idx, row_data in enumerate(sample_data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                table.setItem(row_idx, col_idx, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # Network table settings
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(column_headers)
        table.setFocusPolicy(Qt.NoFocus)

        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 150)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 150)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Network table styling
        header_style = """
            QHeaderView::section {
                background-color: #414657;
                font: yu gothic ui 25px;
                padding: 0px;
                border-left: 2px solid #000;
                color: #fff;
            }
        """
        table.horizontalHeader().setStyleSheet(header_style)

        cell_style = """
            QTableWidget::item {
                padding: 0px;  /* Set the padding */
                border-right: 0px dotted transparent;
                border-bottom: 1px solid #6D7594;
                color: white;
                background-color: #323644;
            }

            QTableWidget::item:selected {
                color: #000;
                background-color: #fff;  /* Set the background color for the selected tab */
            }
        """
        table.setStyleSheet(cell_style)
        table.setSelectionBehavior(QTableWidget.SelectRows)

        # Set custom row height for all rows
        custom_row_height = 1
        for row in range(table.rowCount()):
            table.verticalHeader().setDefaultSectionSize(custom_row_height)
