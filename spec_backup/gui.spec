# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['/Users/pablo/Desktop/kairosBot/kairos'],
             binaries=[('chromedriver','.')],
             datas=[],
             hiddenimports=["babel.numbers"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)



a.datas += [('bot.ico','/Users/pablo/Desktop/kairosBot/kairos/bot.ico',"DATA")]
a.datas += [('button_book.png','/Users/pablo/Desktop/kairosBot/kairos/button_book.png',"DATA")]
a.datas += [('button_change_date.png','/Users/pablo/Desktop/kairosBot/kairos/button_change_date.png',"DATA")]
a.datas += [('button_close.png','/Users/pablo/Desktop/kairosBot/kairos/button_close.png',"DATA")]
a.datas += [('button_login.png','/Users/pablo/Desktop/kairosBot/kairos/button_login.png',"DATA")]
a.datas += [('button_retry.png','/Users/pablo/Desktop/kairosBot/kairos/button_retry.png',"DATA")]
a.datas += [('deadline.png','/Users/pablo/Desktop/kairosBot/kairos/deadline.png',"DATA")]
a.datas += [('kairosbot.ico','/Users/pablo/Desktop/kairosBot/kairos/kairosbot.ico',"DATA")]
a.datas += [('login_bg.png','/Users/pablo/Desktop/kairosBot/kairos/login_bg.png',"DATA")]
a.datas += [('password_entry.png','/Users/pablo/Desktop/kairosBot/kairos/password_entry.png',"DATA")]
a.datas += [('password_entry.png','/Users/pablo/Desktop/kairosBot/kairos/username_entry.png',"DATA")]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='gui.app',
             icon=None,
             bundle_identifier=None)
