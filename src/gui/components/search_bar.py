from PyQt5.QtWidgets import QLineEdit

def create_search_bar():
    search_input = QLineEdit()
    search_input.setPlaceholderText("Example: 192.168.0.1-100, 192.168.0.200")
    return search_input

