from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                           QPushButton, QTableWidget, QTableWidgetItem, 
                           QLabel, QSpinBox, QComboBox)
from PyQt5.QtCore import pyqtSignal

class PortScannerWidget(QWidget):
    scan_requested = pyqtSignal(str, int, int, str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter IP address or hostname")
        controls_layout.addWidget(QLabel("Target:"))
        controls_layout.addWidget(self.target_input)
        
        self.port_start = QSpinBox()
        self.port_start.setRange(1, 65535)
        self.port_start.setValue(1)
        controls_layout.addWidget(QLabel("Port range:"))
        controls_layout.addWidget(self.port_start)
        
        self.port_end = QSpinBox()
        self.port_end.setRange(1, 65535)
        self.port_end.setValue(1024)
        controls_layout.addWidget(QLabel("to"))
        controls_layout.addWidget(self.port_end)
        
        self.scan_type = QComboBox()
        self.scan_type.addItems(["TCP Connect", "SYN Scan", "UDP Scan"])
        controls_layout.addWidget(QLabel("Scan type:"))
        controls_layout.addWidget(self.scan_type)
        
        self.scan_button = QPushButton("Start Port Scan")
        self.scan_button.clicked.connect(self.request_scan)
        controls_layout.addWidget(self.scan_button)
        
        layout.addLayout(controls_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Port", "State", "Service", "Version"])
        layout.addWidget(self.results_table)
        
    def request_scan(self):
        target = self.target_input.text()
        start_port = self.port_start.value()
        end_port = self.port_end.value()
        scan_type = self.scan_type.currentText()
        
        self.scan_requested.emit(target, start_port, end_port, scan_type)
        
    def add_result(self, port, state, service, version):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        self.results_table.setItem(row, 0, QTableWidgetItem(str(port)))
        self.results_table.setItem(row, 1, QTableWidgetItem(state))
        self.results_table.setItem(row, 2, QTableWidgetItem(service))
        self.results_table.setItem(row, 3, QTableWidgetItem(version))
        
    def clear_results(self):
        self.results_table.setRowCount(0)

