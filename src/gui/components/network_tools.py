from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                           QPushButton, QTextEdit, QLabel, QSpinBox)
from PyQt5.QtCore import pyqtSignal

class NetworkToolsWidget(QWidget):
    ping_requested = pyqtSignal(str, int)
    traceroute_requested = pyqtSignal(str, int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Ping controls
        ping_layout = QHBoxLayout()
        
        self.ping_target = QLineEdit()
        self.ping_target.setPlaceholderText("Enter IP address or hostname")
        ping_layout.addWidget(QLabel("Ping target:"))
        ping_layout.addWidget(self.ping_target)
        
        self.ping_count = QSpinBox()
        self.ping_count.setRange(1, 100)
        self.ping_count.setValue(4)
        ping_layout.addWidget(QLabel("Count:"))
        ping_layout.addWidget(self.ping_count)
        
        self.ping_button = QPushButton("Ping")
        self.ping_button.clicked.connect(self.request_ping)
        ping_layout.addWidget(self.ping_button)
        
        layout.addLayout(ping_layout)
        
        # Traceroute controls
        traceroute_layout = QHBoxLayout()
        
        self.traceroute_target = QLineEdit()
        self.traceroute_target.setPlaceholderText("Enter IP address or hostname")
        traceroute_layout.addWidget(QLabel("Traceroute target:"))
        traceroute_layout.addWidget(self.traceroute_target)
        
        self.max_hops = QSpinBox()
        self.max_hops.setRange(1, 64)
        self.max_hops.setValue(30)
        traceroute_layout.addWidget(QLabel("Max hops:"))
        traceroute_layout.addWidget(self.max_hops)
        
        self.traceroute_button = QPushButton("Traceroute")
        self.traceroute_button.clicked.connect(self.request_traceroute)
        traceroute_layout.addWidget(self.traceroute_button)
        
        layout.addLayout(traceroute_layout)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
    def request_ping(self):
        target = self.ping_target.text()
        count = self.ping_count.value()
        self.ping_requested.emit(target, count)
        
    def request_traceroute(self):
        target = self.traceroute_target.text()
        max_hops = self.max_hops.value()
        self.traceroute_requested.emit(target, max_hops)
        
    def add_result(self, text):
        self.results_text.append(text)
        
    def clear_results(self):
        self.results_text.clear()

