import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "--onefile",
        "--icon=src/icon/csctcloud.ico",
        "--distpath=.",
        "--clean",
        "src/connect.py",
    ]
)
