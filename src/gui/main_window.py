from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar, 
                           QTabWidget, QFileDialog, QComboBox, QLineEdit, QPushButton, 
                           QLabel, QCheckBox, QMessageBox, QSpinBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QDateTime
from .components.menu_bar import create_menu_bar
from .components.toolbar import create_toolbar
from .components.search_bar import create_search_bar
from .components.results_table import ResultsTable
from .components.wireshark_table import WiresharkTable
from .components.summary_view import SummaryView
from .components.port_scanner import PortScannerWidget
from .components.network_tools import NetworkToolsWidget
from core.scanner import ScannerThread
from core.packet_capture import PacketCaptureThread
from core.port_scanner import PortScannerThread
from core.network_tools import PingThread, TracerouteThread
import psutil
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Network Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('resources/icon.ico'))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.create_tab_widget()
        self.create_menu_bar()
        self.create_toolbar()
        self.create_search_bar()
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initialize all threads as None
        self.scanner_thread = None
        self.packet_capture_thread = None
        self.port_scanner_thread = None
        self.ping_thread = None
        self.traceroute_thread = None
        
        self.dark_mode = False
        self.create_dark_mode_toggle()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_results)
        self.auto_save_timer.start(300000)  # Auto-save every 5 minutes
        
        self.load_settings()
        
        # Connect network tools signals
        self.network_tools_widget.ping_requested.connect(self.start_ping)
        self.network_tools_widget.traceroute_requested.connect(self.start_traceroute)

    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        
        # IP Scanner Tab
        self.ip_scanner_tab = QWidget()
        self.tab_widget.addTab(self.ip_scanner_tab, "IP Scanner")
        self.ip_scanner_layout = QVBoxLayout(self.ip_scanner_tab)
        self.results_table = ResultsTable()
        self.ip_scanner_layout.addWidget(self.results_table)
        
        # Packet Capture Tab
        self.wireshark_tab = QWidget()
        self.tab_widget.addTab(self.wireshark_tab, "Packet Capture")
        self.create_wireshark_layout()
        
        # Port Scanner Tab
        self.port_scanner_tab = QWidget()
        self.tab_widget.addTab(self.port_scanner_tab, "Port Scanner")
        self.port_scanner_widget = PortScannerWidget()
        self.port_scanner_layout = QVBoxLayout(self.port_scanner_tab)
        self.port_scanner_layout.addWidget(self.port_scanner_widget)
        
        # Network Tools Tab
        self.network_tools_tab = QWidget()
        self.tab_widget.addTab(self.network_tools_tab, "Network Tools")
        self.network_tools_widget = NetworkToolsWidget()
        self.network_tools_layout = QVBoxLayout(self.network_tools_tab)
        self.network_tools_layout.addWidget(self.network_tools_widget)
        
        self.layout.addWidget(self.tab_widget)

    def create_wireshark_layout(self):
        layout = QVBoxLayout(self.wireshark_tab)
        
        # Create controls for packet capture
        controls_layout = QHBoxLayout()
        
        self.interface_combo = QComboBox()
        self.interface_combo.addItems(self.get_network_interfaces())
        controls_layout.addWidget(QLabel("Interface:"))
        controls_layout.addWidget(self.interface_combo)
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter capture filter")
        controls_layout.addWidget(QLabel("Filter:"))
        controls_layout.addWidget(self.filter_input)
        
        self.start_capture_btn = QPushButton("Start Capture")
        self.start_capture_btn.clicked.connect(self.start_packet_capture)
        controls_layout.addWidget(self.start_capture_btn)
        
        self.stop_capture_btn = QPushButton("Stop Capture")
        self.stop_capture_btn.clicked.connect(self.stop_packet_capture)
        self.stop_capture_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_capture_btn)
        
        layout.addLayout(controls_layout)
        
        # Create Wireshark-like table
        self.wireshark_table = WiresharkTable()
        layout.addWidget(self.wireshark_table)
        
        # Create summary view
        self.summary_view = SummaryView()
        layout.addWidget(self.summary_view)

    def get_network_interfaces(self):
        return list(psutil.net_if_addrs().keys())

    def start_packet_capture(self):
        if self.packet_capture_thread and self.packet_capture_thread.isRunning():
            QMessageBox.warning(self, "Warning", "Packet capture already in progress")
            return
        
        interface = self.interface_combo.currentText()
        filter_text = self.filter_input.text()
        
        self.wireshark_table.clear_results()
        self.summary_view.clear()
        
        self.packet_capture_thread = PacketCaptureThread(interface, filter_text)
        self.packet_capture_thread.update_signal.connect(self.update_packet_capture)
        self.packet_capture_thread.error_signal.connect(self.handle_error)
        
        self.start_capture_btn.setEnabled(False)
        self.stop_capture_btn.setEnabled(True)
        self.status_bar.showMessage("Capturing packets...")
        self.packet_capture_thread.start()

    def stop_packet_capture(self):
        if self.packet_capture_thread and self.packet_capture_thread.isRunning():
            self.packet_capture_thread.stop()
            self.packet_capture_thread.wait()
            self.start_capture_btn.setEnabled(True)
            self.stop_capture_btn.setEnabled(False)
            self.status_bar.showMessage("Packet capture stopped")

    def update_packet_capture(self, packet_info):
        self.wireshark_table.add_packet(packet_info)
        self.summary_view.update_summary(packet_info)

    def start_ping(self, target, count):
        if self.ping_thread and self.ping_thread.isRunning():
            QMessageBox.warning(self, "Warning", "Ping already in progress")
            return
        
        self.network_tools_widget.clear_results()
        
        self.ping_thread = PingThread(target, count)
        self.ping_thread.update_signal.connect(self.network_tools_widget.add_result)
        self.ping_thread.finished_signal.connect(self.ping_finished)
        self.ping_thread.error_signal.connect(self.handle_error)
        
        self.status_bar.showMessage("Pinging...")
        self.ping_thread.start()

    def ping_finished(self):
        self.status_bar.showMessage("Ping completed")

    def start_traceroute(self, target, max_hops):
        if self.traceroute_thread and self.traceroute_thread.isRunning():
            QMessageBox.warning(self, "Warning", "Traceroute already in progress")
            return
        
        self.network_tools_widget.clear_results()
        
        self.traceroute_thread = TracerouteThread(target, max_hops)
        self.traceroute_thread.update_signal.connect(self.network_tools_widget.add_result)
        self.traceroute_thread.finished_signal.connect(self.traceroute_finished)
        self.traceroute_thread.error_signal.connect(self.handle_error)
        
        self.status_bar.showMessage("Tracing route...")
        self.traceroute_thread.start()

    def traceroute_finished(self):
        self.status_bar.showMessage("Traceroute completed")

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
        self.status_bar.showMessage("Error occurred")

    def create_dark_mode_toggle(self):
        self.dark_mode_toggle = QCheckBox("Dark Mode")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        self.layout.addWidget(self.dark_mode_toggle)

    def toggle_dark_mode(self, state):
        self.dark_mode = state == Qt.Checked
        self.apply_style()

    def apply_style(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #ffffff; }
                QTableWidget { gridline-color: #3a3a3a; }
                QHeaderView::section { background-color: #3a3a3a; }
                QPushButton { background-color: #3a3a3a; border: 1px solid #5a5a5a; }
                QLineEdit, QComboBox { background-color: #3a3a3a; border: 1px solid #5a5a5a; }
            """)
        else:
            self.setStyleSheet("")

    def auto_save_results(self):
        timestamp = QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        filename = f"auto_save_{timestamp}.json"
        
        data = {
            "ip_scan": self.results_table.get_all_data(),
            "packet_capture": self.wireshark_table.get_all_data(),
            "port_scan": self.port_scanner_widget.get_all_data(),
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f)
        
        self.status_bar.showMessage(f"Results auto-saved to {filename}")

    def load_settings(self):
        try:
            with open("settings.json", 'r') as f:
                settings = json.load(f)
            
            self.dark_mode = settings.get("dark_mode", False)
            self.dark_mode_toggle.setChecked(self.dark_mode)
            self.apply_style()
            
            # Load other settings as needed
        except FileNotFoundError:
            pass  # No settings file found, use defaults

    def save_settings(self):
        settings = {
            "dark_mode": self.dark_mode,
            # Add other settings as needed
        }
        
        with open("settings.json", 'w') as f:
            json.dump(settings, f)

    def closeEvent(self, event):
        # Stop all running threads
        threads = [
            self.scanner_thread,
            self.packet_capture_thread,
            self.port_scanner_thread,
            self.ping_thread,
            self.traceroute_thread
        ]
        
        for thread in threads:
            if thread and thread.isRunning():
                thread.stop()
                thread.wait()
        
        # Save settings
        self.save_settings()
        
        # Accept the close event
        event.accept()

    def create_menu_bar(self):
        self.setMenuBar(create_menu_bar(self))

    def start_scan(self):
        if self.scanner_thread and self.scanner_thread.isRunning():
            QMessageBox.warning(self, "Warning", "Scan already in progress")
            return
    
        ip_range = self.search_input.text()
    
        self.results_table.clear_results()
    
        self.scanner_thread = ScannerThread(ip_range)
        self.scanner_thread.update_signal.connect(self.results_table.add_device)
        self.scanner_thread.finished_signal.connect(self.scan_finished)
        self.scanner_thread.error_signal.connect(self.handle_error)
    
        self.status_bar.showMessage("Scanning...")
        self.scanner_thread.start()

    def scan_finished(self):
        self.status_bar.showMessage("Scan completed")

    def create_toolbar(self):
        toolbar = create_toolbar(self)
        self.addToolBar(toolbar)