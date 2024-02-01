# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Z:\\TRITONIA\\NMEA_GPX_CONVERTER\\nmea_gpx_converter.py'],
             pathex=[],
             binaries=[],
             datas=[('c:/users/matt/anaconda3/envs/small_waterlinked/lib/site-packages/customtkinter', 'customtkinter/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['matplotlib', 'scipy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
splash = Splash('gpx_icon.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=None,
                text_size=12,
                minify_script=True)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas, 
          splash, 
          splash.binaries,
          [],
          name='nmea_gpx_converter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='gpx_icon.ico')
