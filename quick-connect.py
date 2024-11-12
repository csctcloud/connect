import argparse
import ctypes
import json
import logging
import os
import pathlib
import re
import subprocess
import sys
from time import sleep

SERVER_RESOURCE_NAME = "CSCT Cloud Programming"
SERVER_ADDRESS = "csctcloud.uwe.ac.uk"


class Terminal:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    BLACK = "\033[30m"
    WHITE = "\033[97m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"


class TerminalFormatter(logging.Formatter):
    message = "%(message)s"

    FORMATS = {
        logging.DEBUG: f"[{Terminal.BOLD}{Terminal.BRIGHT_BLUE}*{Terminal.RESET}] {message}",
        logging.INFO: f"[{Terminal.BOLD}{Terminal.BRIGHT_GREEN}*{Terminal.RESET}] {message}",
        logging.WARNING: f"[{Terminal.BOLD}{Terminal.BRIGHT_YELLOW}!{Terminal.RESET}] {message}",
        logging.ERROR: f"[{Terminal.BOLD}{Terminal.BRIGHT_MAGENTA}!{Terminal.RESET}] {message}",
        logging.CRITICAL: f"[{Terminal.BOLD}{Terminal.BRIGHT_RED}!{Terminal.RESET}] {message}",
    }

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(
            self.FORMATS.get(record.levelno, logging.CRITICAL)
        )
        return formatter.format(record)


logger = logging.getLogger("CSCTCLOUD-QC")


def runSubprocess(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def showMessageBox(message: str, title: str = "CSCT Cloud Connection Error") -> None:
    ctypes.windll.user32.MessageBoxExW(None, message, title, 0x40000)


def isResourceAllowed(account: str) -> bool:
    try:
        outputJSON = json.loads(account)
        if isinstance(outputJSON, list):
            resources = list(map(lambda t: t["name"], outputJSON))
            return SERVER_RESOURCE_NAME in resources
        else:
            return outputJSON["name"] == SERVER_RESOURCE_NAME

    except Exception as e:
        logger.critical(f"Unexpected error occured checking tenant: {e}")
        showMessageBox(
            "There was a problem completing your login.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
        )
        exit(1)


def main() -> int:
    logger.debug("Running CSCT Cloud Quick Connect")

    print(Terminal.BOLD + Terminal.BRIGHT_BLUE)
    print(r"""                                                                                
 ,-----. ,---.   ,-----.,--------.     ,-----.,--.    ,-----. ,--. ,--.,------.   
'  .--./'   .-' '  .--./'--.  .--'    '  .--./|  |   '  .-.  '|  | |  ||  .-.  \  
|  |    `.  `-. |  |       |  |       |  |    |  |   |  | |  ||  | |  ||  |  \  : 
'  '--'\.-'    |'  '--'\   |  |       '  '--'\|  '--.'  '-'  ''  '-'  '|  '--'  / 
 `-----'`-----'  `-----'   `--'        `-----'`-----' `-----'  `-----' `-------'""")
    print(Terminal.RESET)
    logger.info("Connecting to CSCT Cloud")

    # Check we're running on Windows
    logger.debug(f"Current platform is {os.name}")
    if os.name != "nt":
        logger.critical(
            "This script is designed to run on Windows based machines, it cannot be run on other platforms"
        )
        exit(1)

    needLogin = False

    # Check if an Azure token already exists
    logger.debug("Checking azure account status")
    output = runSubprocess(["az", "account", "show"])
    if output.returncode == 1:
        logger.debug("No azure user account currently logged in")
        needLogin = True

    else:
        logger.debug("An azure user account is currently logged in")

        # Check if token valid for UWE tenant
        if not isResourceAllowed(output.stdout):
            logger.warning(
                "Currently logged in azure user account is not allowed access to this resource"
            )
            needLogin = True
        else:
            logger.info("Azure account is allowed access to this resource")

    # If login required, call az login
    if needLogin:
        logger.debug("Running azure login flow")
        runSubprocess(["az", "config", "set", "core.login_experience_v2=off"])
        logger.info(
            "Login required, please login to your UWE account in the browser window which has just opened"
        )
        output = runSubprocess(["az", "login"])

        if output.returncode == 1:
            logger.error(
                "Login flow failed, this normally indicates an error with the actual login process (user entered incorrect password or failed MFA check)"
            )
            showMessageBox(
                "There was a problem with your login.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
            )
            return 1

        logger.info("Azure account logged in")

        # Check resource listed in account
        # TODO: not sure if there will be accounts that return more than one tenant
        # will we need to catch these and then specify tenant to use?
        logger.debug("Checking if account is allowed access to this resource")
        if not isResourceAllowed(output.stdout):
            logger.error(
                "Logged in account is not allowed access to this resource, this either means the user completed the login flow with a non-UWE account, or their UWE account does not have access to the server"
            )
            showMessageBox(
                "The account you have used to login is not a UWE account, or your UWE account is not allowed access to this resource.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
            )
            return 1

        logger.info("Azure account is allowed access to resource")

    # Check if SSH extension installed (and install if not)
    logger.debug("Checking if SSH extension is available")
    checkExtension = runSubprocess(["az", "extension", "show", "--name", "ssh"])
    if checkExtension.returncode == 1:
        logger.warning("SSH extension not currently available")
        addExtension = runSubprocess(["az", "extension", "add", "--name", "ssh"])
        if addExtension.returncode == 1:
            logger.critical(
                f"An error occurred adding the SSH extension: {addExtension.stderr}"
            )
            showMessageBox(
                "There was an unexpected error while adding the SSH extension.\n\nPlease try running the connection shortcut again."
            )
            return 1

        logger.info("SSH extension successfully added")
    else:
        logger.info("SSH extension available")

    # Check if .ssh folder exists for user
    sshDirectory = pathlib.Path.home() / ".ssh"
    logger.info(f"SSH config directory is {sshDirectory}")
    logger.debug("Checking if user's SSH config directory exists")
    if not sshDirectory.exists():
        logger.warning("SSH config directory doesn't currently exist")
        sshDirectory.mkdir()
        logger.info("SSH config directory created")

    else:
        # Check if csctcloud key directory exists and clear it
        logger.debug(
            "SSH config directory exists, checking if CSCTCloud key directory exists"
        )
        keyDirectory = sshDirectory / "csctcloud"
        logger.info(f"CSCT Cloud key directory is {keyDirectory}")

        if keyDirectory.exists():
            logger.debug("CSCT Cloud key directory exists, clearing contents")
            for root, dirs, files in keyDirectory.walk(top_down=False):
                for name in files:
                    (root / name).unlink()
                for name in dirs:
                    (root / name).rmdir()
            logger.debug("Contents of CSCT Cloud key directory cleared")
        else:
            logger.debug("CSCT Cloud key directory doesn't exist")

    # Generate SSH keys and certificate
    logger.debug("Generating SSH keys")
    sshConfig = sshDirectory / "config"
    createKeys = runSubprocess(
        [
            "az",
            "ssh",
            "config",
            "--ip",
            SERVER_ADDRESS,
            "--overwrite",
            "--file",
            sshConfig,
            "--keys-destination-folder",
            keyDirectory,
        ]
    )

    if createKeys.returncode == 1:
        logger.critical(f"Creating keys failed: {createKeys.stderr}")
        showMessageBox(
            "There was an unexpected error while creating SSH keys.\n\nPlease try running the connection shortcut again."
        )
        return 1

    # note: for some reason the output from this call comes in stderr even when returncode is successful
    expiry = re.search(r"valid until (.*) in local time", createKeys.stderr)
    if expiry:
        valid = expiry.group(1)
        logger.info(f"Generated SSH keys, certificate is valid until {valid}")
    else:
        logger.warning(
            "Generated SSH keys but couldn't extract expiry time from output"
        )

    # Launch Visual Studio Code with remote target
    logger.debug("Launching Visual Studio Code")
    vscode = runSubprocess(["code", "-n", "--remote", f"ssh-remote+{SERVER_ADDRESS}"])
    if vscode.returncode == 0:
        logger.info(
            f"Visual Studio Code launched with remote connection to {SERVER_ADDRESS}"
        )
    else:
        logger.critical(f"Failed to launch Visual Studio Code: {vscode.stderr}")
        showMessageBox(
            "An unknown error occurred while launching Visual Studio Code.\n\nPlease try running the connection shortcut again."
        )
        return 1

    logger.debug("Execution complete")
    sleep(10)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="CSCT Cloud Quick Connect",
        description="Sets up an SSH configuration and necessary keys to establish a connection to the CSCT Cloud server, using the Azure CLI tools",
    )
    parser.add_argument(
        "-l",
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="ERROR",
        help="log level to run program under",
    )
    args = parser.parse_args()

    # logging level to terminal is INFO, but file handler will only log
    # ERROR & higher messages unless otherwise specified in program arguments
    logger.setLevel(logging.INFO)

    file = logging.FileHandler(
        filename=pathlib.Path().home() / "csctcloud-quick-connect.log",
        encoding="utf-8",
    )
    file.setLevel(getattr(logging, args.log.upper(), logging.ERROR))
    file.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
    logger.addHandler(file)

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(TerminalFormatter())
    logger.addHandler(stream)

    try:
        exitCode = main()
        exit(exitCode)

    except Exception as e:
        logger.critical(f"Unexpected exception: {e}")
        exit(1)
