from PyQt5.QtCore import QThread, pyqtSignal
from scapy.all import ARP, Ether, srp
import socket
import time
from .ip_utils import get_manufacturer

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
                    'manufacturer': get_manufacturer(mac)
                }
                self.update_signal.emit(device_info)

            scan_time = time.time() - start_time
            self.finished_signal.emit(f"Scan completed in {scan_time:.2f} seconds")
        except Exception as e:
            self.finished_signal.emit(f"An error occurred: {str(e)}")

