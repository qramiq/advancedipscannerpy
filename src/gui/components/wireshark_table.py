from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class WiresharkTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["No.", "Time", "Source", "Destination", "Protocol", "Length", "Type"])
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def clear_results(self):
        self.setRowCount(0)

    def add_packet(self, packet_info):
        row = self.rowCount()
        self.insertRow(row)
        
        self.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.setItem(row, 1, QTableWidgetItem(packet_info['time']))
        self.setItem(row, 2, QTableWidgetItem(packet_info['source']))
        self.setItem(row, 3, QTableWidgetItem(packet_info['destination']))
        self.setItem(row, 4, QTableWidgetItem(packet_info['protocol']))
        self.setItem(row, 5, QTableWidgetItem(str(packet_info['length'])))
        self.setItem(row, 6, QTableWidgetItem(packet_info['type']))

    def get_all_data(self):
        data = []
        for row in range(self.rowCount()):
            row_data = [self.item(row, col).text() for col in range(self.columnCount())]
            data.append(row_data)
        return data

