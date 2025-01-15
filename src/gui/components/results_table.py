from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog

class ResultsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["Status", "Name", "IP", "Manufacturer", "MAC Address"])
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def clear_results(self):
        self.setRowCount(0)

    def add_device(self, device_info):
        row = self.rowCount()
        self.insertRow(row)
        
        self.setItem(row, 0, QTableWidgetItem(device_info['status']))
        self.setItem(row, 1, QTableWidgetItem(device_info['name']))
        self.setItem(row, 2, QTableWidgetItem(device_info['ip']))
        self.setItem(row, 3, QTableWidgetItem(device_info['manufacturer']))
        self.setItem(row, 4, QTableWidgetItem(device_info['mac']))

    def save_results(self):
        if self.rowCount() == 0:
            QMessageBox.warning(self, "Warning", "No results to save!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write("Advanced IP Scanner Results\n")
                f.write("=" * 50 + "\n\n")
                
                for row in range(self.rowCount()):
                    f.write(f"Status: {self.item(row, 0).text()}\n")
                    f.write(f"Name: {self.item(row, 1).text()}\n")
                    f.write(f"IP: {self.item(row, 2).text()}\n")
                    f.write(f"Manufacturer: {self.item(row, 3).text()}\n")
                    f.write(f"MAC Address: {self.item(row, 4).text()}\n")
                    f.write("-" * 50 + "\n")
                    
            QMessageBox.information(self, "Success", "Results saved successfully!")

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

