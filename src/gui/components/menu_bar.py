from PyQt5.QtWidgets import QMenuBar, QAction

def create_menu_bar(parent):
    menubar = QMenuBar(parent)
    
    file_menu = menubar.addMenu('File')
    save_action = QAction('Save Results', parent)
    save_action.triggered.connect(parent.results_table.save_results)
    file_menu.addAction(save_action)
    
    exit_action = QAction('Exit', parent)
    exit_action.triggered.connect(parent.close)
    file_menu.addAction(exit_action)
    
    scan_menu = menubar.addMenu('Scan')
    start_scan_action = QAction('Start IP Scan', parent)
    start_scan_action.triggered.connect(parent.start_scan)
    scan_menu.addAction(start_scan_action)
    
    capture_menu = menubar.addMenu('Capture')
    start_capture_action = QAction('Start Packet Capture', parent)
    start_capture_action.triggered.connect(parent.start_packet_capture)
    capture_menu.addAction(start_capture_action)
    
    stop_capture_action = QAction('Stop Packet Capture', parent)
    stop_capture_action.triggered.connect(parent.stop_packet_capture)
    capture_menu.addAction(stop_capture_action)
    
    help_menu = menubar.addMenu('Help')
    about_action = QAction('About', parent)
    about_action.triggered.connect(parent.results_table.show_about)
    help_menu.addAction(about_action)
    
    return menubar

