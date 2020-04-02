# -*- mode: python ; coding: utf-8 -*-

import os

spec_root = os.path.abspath(SPECPATH)
block_cipher = None
app_name = 'DrawingTimer'
mac_icon = 'logo.ico'


a = Analysis(['/Users/justinkim/Documents/_Development/_Drawing_Timer/drawingtimer.py'],
             pathex=['/Users/justinkim/Documents/_Development/_Drawing_Timer'],
             binaries=[],
             datas=[('*.kv','.'),('*.jpg','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter','Tkinter','enchant','twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='drawingtimer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('/Users/justinkim/Documents/_Development/_Drawing_Timer'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='drawingtimer')
app = BUNDLE(coll,
             name=app_name + '.app',
             icon=mac_icon,
             bundle_identifier=None)
