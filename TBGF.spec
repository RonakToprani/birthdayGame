# -*- mode: python ; coding: utf-8 -*-

# Set the target_arch to 'x86_64' for Intel-based Macs
target_arch = 'x86_64'

a = Analysis(
    ['finalGame.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('PhotoP.jpg', '.'), 
        ('PhotoR.jpg', '.'), 
        ('PhotoQ.jpg', '.'), 
        ('PhotoS.jpg', '.'), 
        ('PhotoX.jpg', '.'), 
        ('PhotoY.jpg', '.'), 
        ('music.mp3', '.'), 
        ('heart.jpg', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TBGF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=target_arch,  # Set the target_arch here
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TBGF',
)

app = BUNDLE(
    coll,
    name='TBGF.app',
    icon='a7lqu-6y8oh.icns',  # Correct the icon filename if needed
    bundle_identifier=None,
)