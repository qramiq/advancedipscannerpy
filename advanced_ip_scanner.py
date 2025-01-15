import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                           QWidget, QMessageBox, QTableWidget, QTableWidgetItem, 
                           QMenuBar, QMenu, QStatusBar, QToolBar, QLineEdit, 
                           QHBoxLayout, QHeaderView, QFileDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from scapy.all import ARP, Ether, srp
import socket
import time

class ScannerThread(QThread):
    update_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(str)
    
    def __init__(self, ip_range):
        super().__init__()
        self.ip_range = ip_range
        
    def run(self):
        try:
            if not self.ip_range:
                local_ip = socket.gethostbyname(socket.gethostname())
                self.ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'

            arp = ARP(pdst=self.ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp

            start_time = time.time()
            result = srp(packet, timeout=3, verbose=0)[0]

            for sent, received in result:
                ip = received.psrc
                mac = received.hwsrc
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    hostname = "Unknown"
                    
                device_info = {
                    'status': 'Online',
                    'name': hostname,
                    'ip': ip,
                    'mac': mac,
                    'manufacturer': self.get_manufacturer(mac)
                }
                self.update_signal.emit(device_info)

            scan_time = time.time() - start_time
            self.finished_signal.emit(f"Scan completed in {scan_time:.2f} seconds")
        except Exception as e:
            self.finished_signal.emit(f"An error occurred: {str(e)}")

    def get_manufacturer(self, mac):
        # This is a simplified version. In a real application,
        # you would want to use a MAC address lookup database
        return "Unknown"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced IP Scanner")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create search bar
        self.create_search_bar()
        
        # Create table
        self.create_table()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initialize scanner thread
        self.scanner_thread = None

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        save_action = file_menu.addAction('Save Results')
        save_action.triggered.connect(self.save_results)
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = help_menu.addAction('About')
        about_action.triggered.connect(self.show_about)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Scan button
        scan_btn = QPushButton("Start Scan")
        scan_btn.clicked.connect(self.start_scan)
        toolbar.addWidget(scan_btn)
        
        # Save button
        save_btn = QPushButton("Save to TXT")
        save_btn.clicked.connect(self.save_results)
        toolbar.addWidget(save_btn)

    def create_search_bar(self):
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Example: 192.168.0.1-100, 192.168.0.200")
        search_layout.addWidget(self.search_input)
        self.layout.addLayout(search_layout)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Status", "Name", "IP", "Manufacturer", "MAC Address"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

    def start_scan(self):
        if self.scanner_thread and self.scanner_thread.isRunning():
            return
            
        self.table.setRowCount(0)
        ip_range = self.search_input.text()
        
        self.scanner_thread = ScannerThread(ip_range)
        self.scanner_thread.update_signal.connect(self.add_device_to_table)
        self.scanner_thread.finished_signal.connect(self.scan_finished)
        
        self.status_bar.showMessage("Scanning...")
        self.scanner_thread.start()

    def add_device_to_table(self, device_info):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(device_info['status']))
        self.table.setItem(row, 1, QTableWidgetItem(device_info['name']))
        self.table.setItem(row, 2, QTableWidgetItem(device_info['ip']))
        self.table.setItem(row, 3, QTableWidgetItem(device_info['manufacturer']))
        self.table.setItem(row, 4, QTableWidgetItem(device_info['mac']))

    def scan_finished(self, message):
        self.status_bar.showMessage(message)

    def save_results(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Warning", "No results to save!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("Advanced IP Scanner Results\n")
                f.write("=" * 50 + "\n\n")
                
                for row in range(self.table.rowCount()):
                    f.write(f"Status: {self.table.item(row, 0).text()}\n")
                    f.write(f"Name: {self.table.item(row, 1).text()}\n")
                    f.write(f"IP: {self.table.item(row, 2).text()}\n")
                    f.write(f"Manufacturer: {self.table.item(row, 3).text()}\n")
                    f.write(f"MAC Address: {self.table.item(row, 4).text()}\n")
                    f.write("-" * 50 + "\n")
                    
            self.status_bar.showMessage("Results saved successfully!")

    def show_about(self):
        about_text = """
        Advanced IP Scanner
        
        A network scanner for discovering devices on your local network.
        
        Features:
        - Fast network scanning
        - Device detection
        - Hostname resolution
        - MAC address detection
        - Export results to TXT
        
        Note: This application requires administrator privileges.
        """
        QMessageBox.about(self, "About Advanced IP Scanner", about_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

