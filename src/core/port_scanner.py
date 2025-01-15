from PyQt5.QtCore import QThread, pyqtSignal
import socket
from scapy.all import sr1, IP, TCP, UDP, ICMP

class PortScannerThread(QThread):
    update_signal = pyqtSignal(int, str, str, str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, target, start_port, end_port, scan_type):
        super().__init__()
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.scan_type = scan_type
        self.is_running = True

    def run(self):
        try:
            for port in range(self.start_port, self.end_port + 1):
                if not self.is_running:
                    break

                if self.scan_type == "TCP Connect":
                    state, service, version = self.tcp_connect_scan(port)
                elif self.scan_type == "SYN Scan":
                    state, service, version = self.syn_scan(port)
                elif self.scan_type == "UDP Scan":
                    state, service, version = self.udp_scan(port)
                else:
                    raise ValueError("Invalid scan type")

                self.update_signal.emit(port, state, service, version)

            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

    def tcp_connect_scan(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.target, port))
        if result == 0:
            service = socket.getservbyport(port, "tcp")
            version = self.get_service_version(port)
            return "Open", service, version
        sock.close()
        return "Closed", "", ""

    def syn_scan(self, port):
        packet = IP(dst=self.target)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=1, verbose=0)
        if response and response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK
                service = socket.getservbyport(port, "tcp")
                version = self.get_service_version(port)
                return "Open", service, version
            elif response[TCP].flags == 0x14:  # RST-ACK
                return "Closed", "", ""
        return "Filtered", "", ""

    def udp_scan(self, port):
        packet = IP(dst=self.target)/UDP(dport=port)
        response = sr1(packet, timeout=1, verbose=0)
        if response is None:
            return "Open|Filtered", "", ""
        elif response.haslayer(UDP):
            return "Open", socket.getservbyport(port, "udp"), ""
        elif response.haslayer(ICMP):
            if int(response[ICMP].type) == 3 and int(response[ICMP].code) in [1, 2, 3, 9, 10, 13]:
                return "Filtered", "", ""
        return "Closed", "", ""

    def get_service_version(self, port):
        # This is a placeholder. In a real application, you would implement
        # service version detection here.
        return "Unknown"

    def stop(self):
        self.is_running = False

