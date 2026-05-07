# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Збираємо все для PyQt6
datas, binaries, hiddenimports = collect_all('PyQt6')

# Додаємо QtCharts вручну
hiddenimports += [
    'PyQt6.QtCharts',
]

a = Analysis(
    ['main.py'],  # <-- заміни якщо інший файл
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='my_app',  # <-- назва exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # True якщо хочеш бачити консоль
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='my_app',
)