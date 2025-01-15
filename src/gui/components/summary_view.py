from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from collections import defaultdict

class SummaryView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        
        self.protocol_count = defaultdict(int)
        self.total_packets = 0
        self.total_bytes = 0
        
        self.protocol_label = QLabel("Protocol Summary:")
        self.total_packets_label = QLabel("Total Packets: 0")
        self.total_bytes_label = QLabel("Total Bytes: 0")
        
        self.layout.addWidget(self.protocol_label)
        self.layout.addWidget(self.total_packets_label)
        self.layout.addWidget(self.total_bytes_label)

    def update_summary(self, packet_info):
        self.protocol_count[packet_info['protocol']] += 1
        self.total_packets += 1
        self.total_bytes += packet_info['length']
        
        self.update_labels()

    def update_labels(self):
        protocol_summary = "\n".join([f"{proto}: {count}" for proto, count in self.protocol_count.items()])
        self.protocol_label.setText(f"Protocol Summary:\n{protocol_summary}")
        self.total_packets_label.setText(f"Total Packets: {self.total_packets}")
        self.total_bytes_label.setText(f"Total Bytes: {self.total_bytes}")

    def clear(self):
        self.protocol_count.clear()
        self.total_packets = 0
        self.total_bytes = 0
        self.update_labels()

