import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "--onefile",
        "--icon=src/icon/csctcloud.ico",
        "--distpath=.",
        "src/connect.py",
    ]
)
