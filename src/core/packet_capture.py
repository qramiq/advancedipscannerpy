from PyQt5.QtCore import QThread, pyqtSignal
from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from queue import Queue
import threading

class PacketCaptureThread(QThread):
    update_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self, interface, filter_text="", buffer_size=10000):
        super().__init__()
        self.interface = interface
        self.filter_text = filter_text
        self.buffer_size = buffer_size
        self.is_running = True
        self.packet_queue = Queue(maxsize=buffer_size)
        self.processing_thread = None
    
    def run(self):
        try:
            # Start packet processing thread
            self.processing_thread = threading.Thread(target=self.process_packets)
            self.processing_thread.start()
            
            # Start packet capture
            sniff(
                iface=self.interface,
                filter=self.filter_text,
                prn=self.enqueue_packet,
                stop_filter=lambda _: not self.is_running
            )
            
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def enqueue_packet(self, packet):
        if self.packet_queue.full():
            self.packet_queue.get()  # Remove oldest packet if buffer is full
        self.packet_queue.put(packet)
    
    def process_packets(self):
        while self.is_running:
            try:
                packet = self.packet_queue.get(timeout=1)
                if IP in packet:
                    packet_info = self.analyze_packet(packet)
                    self.update_signal.emit(packet_info)
            except:
                continue
    
    def analyze_packet(self, packet):
        packet_type = self.get_packet_type(packet)
        return {
            'time': time.strftime("%H:%M:%S"),
            'source': packet[IP].src,
            'destination': packet[IP].dst,
            'protocol': packet[IP].proto,
            'length': len(packet),
            'type': packet_type,
            'details': self.get_packet_details(packet)
        }
    
    def get_packet_type(self, packet):
        if TCP in packet:
            if packet[TCP].dport == 80:
                return "HTTP Request"
            elif packet[TCP].sport == 80:
                return "HTTP Response"
            elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                return "HTTPS"
            else:
                return f"TCP ({packet[TCP].dport})"
        elif UDP in packet:
            return f"UDP ({packet[UDP].dport})"
        elif ICMP in packet:
            return "ICMP"
        else:
            return "Other"
    
    def get_packet_details(self, packet):
        details = []
        
        if TCP in packet:
            details.append(f"TCP Flags: {packet[TCP].flags}")
            details.append(f"Sequence: {packet[TCP].seq}")
            details.append(f"Window: {packet[TCP].window}")
        elif UDP in packet:
            details.append(f"Length: {packet[UDP].len}")
        elif ICMP in packet:
            details.append(f"Type: {packet[ICMP].type}")
            details.append(f"Code: {packet[ICMP].code}")
            
        return ", ".join(details)
    
    def stop(self):
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join()

