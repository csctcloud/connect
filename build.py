import PyInstaller.__main__
import shutil
import sys

from src.connect import __VERSION__

PyInstaller.__main__.run(
    [
        "--onefile",
        "--icon=src/icon/csctcloud.ico",
        "src/connect.py",
    ]
)

shutil.make_archive(f"release/connect_{__VERSION__}_{sys.platform}", "zip", "dist")
