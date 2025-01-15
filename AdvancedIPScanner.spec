# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[('C:\\Windows\\System32\\Npcap\\wpcap.dll', '.')],
    datas=[('resources/icon.ico', '.'), ('src', 'src')],
    hiddenimports=['sip', 'PyQt5.sip', 'scapy.layers.all', 'scapy.arch.windows', 'psutil', 'core.scanner', 'core.packet_capture', 'core.port_scanner', 'core.network_tools'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AdvancedIPScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\icon.ico'],
)
