from PyQt5.QtWidgets import QHBoxLayout, QTreeView, QFrame, QVBoxLayout, QTableWidget, QSizePolicy, QSplitter, \
    QTableWidgetItem, QPushButton, QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon


class CustomStandardItem(QStandardItem):
    def __init__(self, text, icon=None):
        super().__init__()
        self.setText(text)
        if icon is not None:
            self.setIcon(QIcon(icon))


class History:
    def __init__(self, tab_widget):
        tab_widget_layout = QHBoxLayout()
        tab_widget.setLayout(tab_widget_layout)
        tab_widget_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QSplitter(Qt.Horizontal)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget_layout.addWidget(self.main_layout)

        self.tree_view = QTreeView()
        self.child_buttons_frame = None
        self.left_panel()

    def left_panel(self):
        left_frame = QFrame()
        left_frame.setMinimumWidth(130)
        self.main_layout.addWidget(left_frame)
        left_frame_layout = QVBoxLayout()
        left_frame.setLayout(left_frame_layout)
        left_frame.setContentsMargins(0, 0, 0, 0)
        left_frame_layout.setContentsMargins(0, 0, 0, 0)

        left_frame.setMaximumWidth(50)
        left_frame.setMaximumWidth(16777215)
        self.main_layout.setSizes([60, 80])

        self.right_frame()
        left_frame_layout.addWidget(self.tree_view)

        # Create the tree model
        model = QStandardItemModel()
        self.tree_view.setModel(model)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        # Insert root item
        root_item = CustomStandardItem('Not assigned', 'assets/group.png')

        # Insert child items
        child1 = CustomStandardItem('192.168.100.2', 'assets/pc.png')
        child2 = CustomStandardItem('192.168.100.3', 'assets/pc.png')
        child3 = CustomStandardItem('192.168.100.4', 'assets/pc.png')

        # Add children to root item
        root_item.appendRow([child1])
        root_item.appendRow([child2])
        root_item.appendRow([child3])

        model.appendRow(root_item)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.expandAll()

    def right_frame(self):
        right_frame = QFrame()
        right_frame.setMinimumWidth(50)
        self.main_layout.addWidget(right_frame)

        right_frame_layout = QVBoxLayout()
        right_frame.setLayout(right_frame_layout)
        right_frame_layout.setContentsMargins(0, 0, 0, 0)
        right_frame.setContentsMargins(0, 0, 0, 0)
        right_frame_layout.setSpacing(0)

        top_button_frame = QFrame()
        top_button_frame.setFixedHeight(60)
        right_frame_layout.addWidget(top_button_frame)

        content_table = QTableWidget()
        right_frame_layout.addWidget(content_table)
        
        content_table.setRowCount(50)
        content_table.setColumnCount(5)
        content_table.horizontalHeader().setStretchLastSection(True)
        content_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_table.verticalHeader().setVisible(False)
        
        sample_data = [
            ['192.168.1.100', '00:11:22:33:44:55', 'SampleHost1', 'Up', 'Vendor1'],
            ['192.168.1.101', 'AA:BB:CC:DD:EE:FF', 'SampleHost2', 'Down', 'Vendor2'],
            ['192.168.1.102', '11:22:33:44:55:66', 'SampleHost3', 'Unknown', 'Vendor3'],
        ]
        column_headers = ['IP Address', 'MAC Address', 'Hostname', 'Status', 'Vendor']
        content_table.setHorizontalHeaderLabels(column_headers)

        header_style = """
            QHeaderView::section {
                background-color: #ededed;
                font: yu gothic ui 100px;
                padding: 0px;
                border-bottom: 2px solid #000;
            }
        """
        content_table.horizontalHeader().setStyleSheet(header_style)

        for row_idx, row_data in enumerate(sample_data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                content_table.setItem(row_idx, col_idx, item)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        header_buttons_frame = QFrame()
        top_frame_layout = QVBoxLayout()
        top_button_frame.setLayout(top_frame_layout)

        child_buttons_frame = QFrame()
        child_buttons_layout = QHBoxLayout()
        child_buttons_layout.setContentsMargins(0, 0, 0, 0)
        child_buttons_frame.setLayout(child_buttons_layout)
        self.child_buttons_frame = child_buttons_frame

        separator_frame = QFrame()
        separator_frame.setStyleSheet("background-color: black;")
        separator_frame.setFixedHeight(2)

        top_frame_layout.setContentsMargins(0, 0, 0, 0)
        top_frame_layout.setSpacing(0)
        top_frame_layout.addWidget(header_buttons_frame)
        top_frame_layout.addWidget(separator_frame)
        top_frame_layout.addWidget(child_buttons_frame)

        header_buttons_layout = QHBoxLayout()
        header_buttons_frame.setLayout(header_buttons_layout)
        header_buttons_layout.setContentsMargins(0, 0, 0, 0)
        left_spacer = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer = QSpacerItem(1, 10, QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_stylesheet = '''
            QPushButton {
                background-color: #ededed;
                border: 1px solid #2196F3; /* Flat appearance */
                border-radius: 5px;
                padding: 5px 10px;
                color: #000;
            }
            QPushButton:hover {
                border-style: sunken;
                background-color: #2196F3; /* Raised appearance on hover */
                color: white;
            }
        '''

        blocking_report = QPushButton(" Block Report")
        urls_visited = QPushButton(" Urls Visited")
        scheduled_events = QPushButton(" Scheduled Events")
        applications_report = QPushButton(" Applications Report")
        net_flow = QPushButton(" Network Flow Report")

        blocking_report.setStyleSheet(button_stylesheet)
        urls_visited.setStyleSheet(button_stylesheet)
        scheduled_events.setStyleSheet(button_stylesheet)
        applications_report.setStyleSheet(button_stylesheet)
        net_flow.setStyleSheet(button_stylesheet)

        blocking_report.setIcon(QIcon(QPixmap('assets/block.png')))
        urls_visited.setIcon(QIcon(QPixmap('assets/www.png')))
        scheduled_events.setIcon(QIcon(QPixmap('assets/deadline.png')))
        applications_report.setIcon(QIcon(QPixmap('assets/data-gathering.png')))
        net_flow.setIcon(QIcon(QPixmap('assets/bandwidth.png')))

        # Connect buttons to their respective functions
        blocking_report.clicked.connect(lambda : self.showBlockedReport())
        urls_visited.clicked.connect(lambda :self.showUrlsVisited())
        scheduled_events.clicked.connect(lambda :self.showScheduledEvents())
        applications_report.clicked.connect(lambda :self.showApplicationsReport())
        net_flow.clicked.connect(lambda :self.showNetworkFlowReport())

        blocking_report.click()
        header_buttons_layout.addItem(left_spacer)
        header_buttons_layout.addWidget(blocking_report)
        header_buttons_layout.addWidget(urls_visited)
        header_buttons_layout.addWidget(scheduled_events)
        header_buttons_layout.addWidget(applications_report)
        header_buttons_layout.addWidget(net_flow)
        header_buttons_layout.addItem(spacer)

    def showBlockedReport(self):
        self.clearChildButtonsFrame()
        programs_blocked = QPushButton("Blocked programs")
        self.child_buttons_frame.layout().addWidget(programs_blocked)

    def showUrlsVisited(self):
        self.clearChildButtonsFrame()
        urls_visited_button = QPushButton("Urls Visited Button")
        self.child_buttons_frame.layout().addWidget(urls_visited_button)

    def showScheduledEvents(self):
        self.clearChildButtonsFrame()
        scheduled_events_button = QPushButton("Scheduled Events Button")
        self.child_buttons_frame.layout().addWidget(scheduled_events_button)

    def showApplicationsReport(self):
        self.clearChildButtonsFrame()
        applications_report_button = QPushButton("Applications Report Button")
        self.child_buttons_frame.layout().addWidget(applications_report_button)

    def showNetworkFlowReport(self):
        self.clearChildButtonsFrame()
        network_flow_report_button = QPushButton("Network Flow Report Button")
        self.child_buttons_frame.layout().addWidget(network_flow_report_button)

    def clearChildButtonsFrame(self):
        layout = self.child_buttons_frame.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
