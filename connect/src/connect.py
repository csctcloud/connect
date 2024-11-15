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

__VERSION__ = "1.0"
SERVER_RESOURCE_NAME = "CSCT Cloud Programming"
SERVER_ADDRESS = "csctcloud.uwe.ac.uk"

logger = logging.getLogger(__name__)


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
        logging.ERROR: f"[{Terminal.BOLD}{Terminal.BRIGHT_RED}!{Terminal.RESET}] {message}",
        logging.CRITICAL: f"[{Terminal.BOLD}{Terminal.BRIGHT_MAGENTA}!{Terminal.RESET}] {message}",
    }

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(
            self.FORMATS.get(record.levelno, logging.CRITICAL)
        )
        return formatter.format(record)


def print_header() -> None:
    os.system(
        ""
    )  # this fixes ANSI escape sequences not displaying properly on some builds
    print(Terminal.BOLD + Terminal.BRIGHT_BLUE, end="")
    print(
        r" ,-----. ,---.   ,-----.,--------.     ,-----.,--.    ,-----. ,--. ,--.,------. "
    )
    print(
        r"'  .--./'   .-' '  .--./'--.  .--'    '  .--./|  |   '  .-.  '|  | |  ||  .-.  \ "
    )
    print(
        r"|  |    `.  `-. |  |       |  |       |  |    |  |   |  | |  ||  | |  ||  |  \  : "
    )
    print(
        r"'  '--'\.-'    |'  '--'\   |  |       '  '--'\|  '--.'  '-'  ''  '-'  '|  '--'  / "
    )
    print(
        r" `-----'`-----'  `-----'   `--'        `-----'`-----' `-----'  `-----' `-------' "
    )
    print(Terminal.RESET)


def run_subprocess(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def message_box(message: str, title: str = "CSCT Cloud Connection Error") -> None:
    ctypes.windll.user32.MessageBoxExW(None, message, title, 0x40000)


def check_resource_allowed(account: str) -> bool:
    try:
        output = json.loads(account)
        if isinstance(output, list):
            resources = list(map(lambda t: t["name"], output))
            return SERVER_RESOURCE_NAME in resources
        else:
            return output["name"] == SERVER_RESOURCE_NAME

    # TODO: work out what we might expect to need to handle
    # * string failing to JSONify
    # * resource name missing in account status
    # in any case - all of these would result in us needing to exit so will
    # work the same as it does currently

    except Exception as e:
        message_box(
            "There was a problem completing your login.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
        )
        raise e


def main(args: argparse.Namespace) -> int:
    print_header()
    logger.info(f"CSCT Cloud Connect (v{__VERSION__})")

    # Check we're running on Windows
    logger.debug(f"Current platform is {os.name}")
    if os.name != "nt":
        logger.error(
            "This script is designed to run on Windows based machines, it cannot be run on other platforms"
        )
        return 1

    # Check if azure CLI tools installed
    logger.debug("Checking azure tools installed")
    tools = run_subprocess(["az"])
    if tools.returncode == 1:
        logger.error("Azure CLI tools need to be installed")
        return 1

    else:
        logger.debug("Azure CLI tools installed")

    need_login = False

    # Check if an azure account is already logged in
    logger.debug("Checking azure account status")
    account = run_subprocess(["az", "account", "show"])
    if account.returncode == 1:
        logger.debug("No azure user account currently logged in")
        need_login = True

    else:
        logger.debug("An azure user account is currently logged in")

        # Check if azure account is able to access resource
        if not check_resource_allowed(account.stdout):
            logger.warning(
                "Currently logged in azure user account is not allowed access to this resource"
            )
            need_login = True
        else:
            logger.info("Azure account is allowed access to this resource")

    # If login required, start the azure login flow
    if need_login:
        logger.debug("Running azure login flow")
        run_subprocess(["az", "config", "set", "core.login_experience_v2=off"])
        logger.info(
            "Login required, please login to your UWE account in the browser window that has just opened"
        )
        login = run_subprocess(["az", "login"])

        if login.returncode == 1:
            logger.error(
                "Login flow failed, this normally indicates an error with the actual login process (user exited login flow, entered an incorrect password or failed MFA check)"
            )
            message_box(
                "There was a problem with your login.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
            )
            return 1

        logger.info("Azure account logged in")

        # Check if azure account is able to access resource
        logger.debug("Checking if account is allowed access to this resource")
        if not check_resource_allowed(login.stdout):
            logger.error(
                "Logged in account is not allowed access to this resource, this either means the user completed the login flow with a non-UWE account, or their UWE account does not have access to the server"
            )
            message_box(
                "The account you have used to login is not a UWE account, or your UWE account is not allowed access to this resource.\n\nPlease run the connection shortcut again and login with your UWE account when prompted."
            )
            return 1

        logger.info("Azure account is allowed access to resource")

    # Check if SSH extension installed (and install if not)
    logger.debug("Checking if SSH extension is available")
    show_extension = run_subprocess(["az", "extension", "show", "--name", "ssh"])
    if show_extension.returncode == 1:
        logger.warning("SSH extension not available - adding it now")
        add_extension = run_subprocess(["az", "extension", "add", "--name", "ssh"])
        if add_extension.returncode == 1:
            logger.critical(
                f"An error occurred adding the SSH extension: {add_extension.stderr}"
            )
            message_box(
                "There was an unexpected error while adding the SSH extension.\n\nPlease try running the connection shortcut again."
            )
            return 1

        logger.info("SSH extension successfully added")
    else:
        logger.info("SSH extension available")

    # Check if .ssh folder exists for user
    ssh_directory = pathlib.Path.home() / ".ssh"
    key_directory = ssh_directory / "csctcloud"

    logger.info(f"SSH config directory is {ssh_directory}")
    logger.debug("Checking if user's SSH config directory exists")
    if not ssh_directory.exists():
        logger.warning("SSH config directory doesn't currently exist")
        ssh_directory.mkdir()
        logger.info("SSH config directory created")

    else:
        # Check if csctcloud key directory exists and clear it
        logger.debug(
            "SSH config directory exists, checking if CSCTCloud key directory exists"
        )
        logger.info(f"CSCT Cloud key directory is {key_directory}")

        if key_directory.exists():
            logger.debug("CSCT Cloud key directory exists, clearing contents")
            for root, dirs, files in key_directory.walk(top_down=False):
                for name in files:
                    (root / name).unlink()
                for name in dirs:
                    (root / name).rmdir()
            logger.debug("Contents of CSCT Cloud key directory cleared")
        else:
            logger.debug("CSCT Cloud key directory doesn't exist")

    # Generate SSH keys and certificate
    logger.debug("Generating SSH keys")
    ssh_config = ssh_directory / "config"
    cmd = [
        "az",
        "ssh",
        "config",
        "--ip",
        SERVER_ADDRESS,
        "--file",
        ssh_config,
        "--keys-destination-folder",
        key_directory,
    ]

    if args.overwrite:
        cmd.append("--overwrite")

    create_keys = run_subprocess(cmd)

    if create_keys.returncode == 1:
        logger.critical(f"Creating keys failed: {create_keys.stderr}")
        message_box(
            "There was an unexpected error while creating SSH keys.\n\nPlease try running the connection shortcut again."
        )
        return 1

    # note: for some reason the output from this call comes in stderr even when returncode is successful
    expiry_time = re.search(r"valid until (.*) in local time", create_keys.stderr)
    if expiry_time:
        valid = expiry_time.group(1)
        logger.info(f"Generated SSH keys, certificate is valid until {valid}")
    else:
        logger.warning(
            "Generated SSH keys but couldn't extract expiry time from output"
        )

    # Launch Visual Studio Code with remote target
    logger.debug("Launching Visual Studio Code")
    vscode = run_subprocess(["code", "-n", "--remote", f"ssh-remote+{SERVER_ADDRESS}"])
    if vscode.returncode == 0:
        logger.info(
            f"Visual Studio Code launched with remote connection to {SERVER_ADDRESS}"
        )
    else:
        logger.critical(f"Failed to launch Visual Studio Code: {vscode.stderr}")
        message_box(
            "An unknown error occurred while launching Visual Studio Code.\n\nPlease try running the connection shortcut again."
        )
        return 1

    logger.debug("Execution complete")

    sleep(10)  # just to keep terminal up for a moment after launch
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="CSCT Cloud Connect",
        description="Sets up an SSH configuration and necessary keys to establish a connection to the CSCT Cloud server, using the Azure CLI tools",
    )
    parser.add_argument(
        "-l",
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="log level to run program under",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        default=False,
        action="store_true",
        help="allow SSH configuration file to be overwritten",
    )
    args = parser.parse_args()

    # setting the maximum possible logging level to DEBUG - terminal handler is set
    # to log INFO and above, file handler will only log ERROR and above unless
    # otherwise specified in program arguments
    logger.setLevel(logging.DEBUG)

    file = logging.FileHandler(
        filename=pathlib.Path().home() / "csctcloud-connect.log",
        encoding="utf-8",
    )
    file.setLevel((getattr(logging, args.log) if args.log else logging.ERROR))
    file.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
    logger.addHandler(file)

    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel((getattr(logging, args.log) if args.log else logging.INFO))
    stream.setFormatter(TerminalFormatter())
    logger.addHandler(stream)

    try:
        exit_code = main(args)
        sys.exit(exit_code)

    except Exception as e:
        logger.critical(f"Unexpected exception: {e}")
        sys.exit(1)
