# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[
        '.'
    ],
    binaries=[],
    datas=[('config.yaml', '.'), ('entity', 'entity'), ('common', 'common'), ('static', 'static')],
    hiddenimports=['bs4','pyperclip'],  # 遇到No module named xxx 等问题，添加依赖库到这里
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tests'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PostSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['static\\imgs\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PostSync',
)
