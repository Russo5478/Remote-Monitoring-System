import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLabel, QTabWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from dlls.functions import center_window
from dlls.windowFunctions import create_image_button
from ctypes import windll as window_dpi
from mainContent.monitoringView import Monitoring
from mainContent.historyData import History
from PyQt5.QtWidgets import QSizePolicy, QSplitter
from mainContent.Network import NetTable

window_dpi.shcore.SetProcessDpiAwareness(1)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Declare variables
        self.core_init = self
        self.main_layout = QVBoxLayout()

        # Run main functions
        self.window_init()

    def window_init(self):
        self.resize(1000, 700)
        self.setMinimumSize(1000, 700)
        self.setWindowTitle("REMOTE ADMIN")
        center_window(self)

        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.top_frame()

    def top_frame(self):
        header_frame = QFrame(self)
        header_frame.setStyleSheet("background-color: #414657;")
        header_frame.setFixedHeight(45)
        self.main_layout.addWidget(header_frame)

        top_frame_layout = QGridLayout()
        header_frame.setLayout(top_frame_layout)
        top_frame_layout.setContentsMargins(0, 0, 0, 0)
        header_frame.setContentsMargins(0, 0, 0, 0)

        top_frame_layout.setSpacing(0)

        logo_frame = QFrame()
        logo_frame.setStyleSheet("background-color: #f59a27;")

        logo_layout = QVBoxLayout(logo_frame)

        # Load the image using QPixmap
        pixmap = QPixmap("assets/net.ico")  # Replace with your image path
        pixmap = pixmap.scaled(33, 33, Qt.KeepAspectRatio)

        # Create a QLabel to display the image
        logo_label = QLabel(logo_frame)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: #414657;")

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 0, 0, 0)
        title_label = QLabel(logo_frame)
        title_label.setStyleSheet("background-color: #414657; color: #fff;")
        title_label.setFont(QFont("yu gothic ui", 18))
        title_label.setText("ipMonitor")
        title_label.setContentsMargins(0, 0, 20, 0)
        title_layout.addWidget(title_label)

        # Create the QPushButton
        add_computer_button = create_image_button(33, title_layout, "Add Computer", 'assets/add.png', 35)
        scan_network_button = create_image_button(33, title_layout, "Scan Network", 'assets/search.png', 35)
        create_group_button = create_image_button(33, title_layout, "Create Group", 'assets/add-user.png', 35)
        settings_button = create_image_button(33, title_layout, "Configuration", 'assets/actions.png', 35)
        binding_ip = create_image_button(33, title_layout, "List of Binding IP - MAC Addresses",
                                         'assets/remote-access.png', 35)

        additional_widgets = 25
        for i in range(0, additional_widgets):
            title_layout.addWidget(QWidget())

        # Set the desired distances of the frames
        top_frame_layout.addWidget(logo_frame, 0, 0)
        top_frame_layout.setColumnStretch(0, 1)
        top_frame_layout.addWidget(title_frame, 0, 1)
        top_frame_layout.setColumnStretch(1, 20)

        self.content_frame()

    def content_frame(self):
        frame = QFrame(self)
        self.main_layout.addWidget(frame)
        self.footer_frame()

        content_frame_layout = QVBoxLayout()
        frame.setLayout(content_frame_layout)
        frame.setContentsMargins(0, 0, 0, 0)
        content_frame_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Vertical)

        splitter_style = """        
            QSplitter::handle {
                height: 0.2px;
                background: black; 
            }
        """
        splitter.setStyleSheet(splitter_style)

        upper_frame = QFrame()
        upper_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        upper_frame_layout = QVBoxLayout()
        upper_frame.setLayout(upper_frame_layout)
        upper_frame.setContentsMargins(0, 0, 0, 0)
        upper_frame_layout.setContentsMargins(0, 0, 0, 0)

        lower_frame = QFrame()
        content_frame_layout.addWidget(splitter)
        NetTable(lower_frame)

        splitter.addWidget(upper_frame)
        splitter.addWidget(lower_frame)
        splitter.setSizes([250, 80])

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                background-color: #d4d4d4;  /* Set the background color */
            }
            
            QTabBar::tab:selected {
                background-color: #ededed;  /* Set the background color for the selected tab */
            }
        """)

        # Create the content for each tab
        tab1_content = QWidget()
        tab2_content = QWidget()
        tab3_content = QWidget()

        # Add content to each tab
        tab_widget.addTab(tab1_content, 'Monitoring View')
        tab_widget.addTab(tab2_content, 'History Data View')
        tab_widget.addTab(tab3_content, 'Chart Summary')

        Monitoring(tab1_content)
        History(tab2_content)

        upper_frame_layout.addWidget(tab_widget)

    def footer_frame(self):
        frame = QFrame(self)
        frame.setStyleSheet("border-radius: 5px; background-color: blue;")
        frame.setFixedHeight(35)

        footer_frame_layout = QGridLayout()
        frame.setLayout(footer_frame_layout)
        self.main_layout.addWidget(frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
