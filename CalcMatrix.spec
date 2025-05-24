from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('PySide6.QtWidgets') + \
                collect_submodules('PySide6.QtGui') + \
                collect_submodules('PySide6.QtCore') + \
                ['numpy', 'matplotlib.pyplot', 'sympy']

datas = [
    ('assets/', 'assets'),
    ('styles/', 'styles'),
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
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
    exclude_binaries=False,
    name='CalcMatrix v1.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon='assets/icons/_ico.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CalcMatrix v1.2',
)
