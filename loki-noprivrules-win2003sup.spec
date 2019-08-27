# -*- mode: python -*-

a = Analysis(['loki.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)

a.datas = list({tuple(map(str.upper, t)) for t in a.datas})

exe = EXE(pyz,
          a.scripts,
          a.binaries + [('msvcr100.dll', 'C:\Windows\System32\msvcr100.dll', 'BINARY')],
          a.zipfiles,
          a.datas,
          name='loki.exe',
          debug=False,
          strip=None,
          upx=False,
          console=True , icon='loki.ico')
