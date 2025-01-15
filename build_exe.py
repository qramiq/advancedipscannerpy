import PyInstaller.__main__
import os
import sys

def find_npcap_dll():
    possible_paths = [
        os.path.join(os.environ['WINDIR'], 'System32', 'Npcap', 'wpcap.dll'),
        os.path.join(os.environ['WINDIR'], 'SysWOW64', 'Npcap', 'wpcap.dll'),
        os.path.join('C:\\', 'Program Files', 'Npcap', 'wpcap.dll'),
        os.path.join('C:\\', 'Program Files (x86)', 'Npcap', 'wpcap.dll'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

npcap_dll = find_npcap_dll()

if not npcap_dll:
    print("Npcap DLL not found. Please make sure Npcap is installed.")
    print("You can download Npcap from: https://npcap.com/")
    print("After installation, you may need to restart your computer.")
    sys.exit(1)

print(f"Found Npcap DLL at: {npcap_dll}")

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--add-binary', f'{npcap_dll};.',
    '--name', 'AdvancedIPScanner',
    '--add-data', 'resources/icon.ico;.',
    '--icon', 'resources/icon.ico',
    '--hidden-import', 'sip',
    '--hidden-import', 'PyQt5.sip',
    '--hidden-import', 'scapy.layers.all',
    '--hidden-import', 'scapy.arch.windows',
    '--hidden-import', 'psutil',
    '--hidden-import', 'core.scanner',
    '--hidden-import', 'core.packet_capture',
    '--hidden-import', 'core.port_scanner',
    '--hidden-import', 'core.network_tools',
    '--add-data', 'src;src',
])

