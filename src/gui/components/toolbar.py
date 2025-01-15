from PyQt5.QtWidgets import QToolBar, QPushButton, QMenu, QAction

def create_toolbar(parent):
    toolbar = QToolBar()
    
    scan_btn = QPushButton("Start IP Scan")
    scan_btn.clicked.connect(parent.start_scan)
    toolbar.addWidget(scan_btn)
    
    capture_btn = QPushButton("Start Packet Capture")
    capture_btn.clicked.connect(parent.start_packet_capture)
    toolbar.addWidget(capture_btn)
    
    stop_capture_btn = QPushButton("Stop Packet Capture")
    stop_capture_btn.clicked.connect(parent.stop_packet_capture)
    toolbar.addWidget(stop_capture_btn)
    
    save_menu = QMenu()
    save_ip_action = QAction("Save IP Scan Results", parent)
    save_ip_action.triggered.connect(parent.save_ip_scan_results)
    save_menu.addAction(save_ip_action)
    
    save_wireshark_action = QAction("Save Packet Capture Results", parent)
    save_wireshark_action.triggered.connect(parent.save_packet_capture_results)
    save_menu.addAction(save_wireshark_action)
    
    save_all_action = QAction("Save All Results", parent)
    save_all_action.triggered.connect(parent.save_all_results)
    save_menu.addAction(save_all_action)
    
    save_btn = QPushButton("Save Results")
    save_btn.setMenu(save_menu)
    toolbar.addWidget(save_btn)
    
    return toolbar

