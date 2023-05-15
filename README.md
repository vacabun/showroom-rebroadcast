# showroom-rebroadcast

rebroadcast showroom live stream.

## Installation

1. Install the python3.

2. Install requirements.

```
pip install -r requirements.txt
```

3. Install ffmpeg

```
sudo apt install ffmpeg
```

## Instructions for use

```
python3 main.py -i <room_name> -o <rtmp_url>

```

## Build

1. Install pyinstaller

``` shell
pip install pyinstaller
```

2. Create spec file

``` shell
pyi-makespec --onefile --console "main.py"
```

3. Edit spec file

Open "main.spec" file and edit it as follows.

> My streamlink is version 2.4.0, but it also conflicts with the iso639 package, so I added it.

``` python
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules  # append

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas = collect_data_files('streamlink.plugins', include_py_files=True) + collect_data_files('iso639'), # edit
    hiddenimports = collect_submodules('streamlink.plugins'),   # edit
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

3. Porting executable file

``` shell
pyinstaller --noconfirm --clean "main.spec"
```