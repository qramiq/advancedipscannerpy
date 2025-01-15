from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import platform

class PingThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, target, count):
        super().__init__()
        self.target = target
        self.count = count

    def run(self):
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, str(self.count), self.target]
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_signal.emit(output.strip())
            
            rc = process.poll()
            if rc != 0:
                error = process.stderr.read()
                self.error_signal.emit(f"Ping failed with error: {error}")
            
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

class TracerouteThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, target, max_hops):
        super().__init__()
        self.target = target
        self.max_hops = max_hops

    def run(self):
        try:
            if platform.system().lower() == 'windows':
                command = ['tracert', '-h', str(self.max_hops), self.target]
            else:
                command = ['traceroute', '-m', str(self.max_hops), self.target]
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_signal.emit(output.strip())
            
            rc = process.poll()
            if rc != 0:
                error = process.stderr.read()
                self.error_signal.emit(f"Traceroute failed with error: {error}")
            
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

