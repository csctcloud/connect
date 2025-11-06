# Install the Azure Command-Line Interface
CSCT Cloud is hosted using Azure, Microsoft's cloud computing platform. To be able to first connect to the server we need to install the Command-Line Interface (CLI) provided for the platform.

!!! tip "UWE lab computers"
    If you're working on a UWE lab computer the Azure CLI is already installed, continue on to the next page to use the CLI to copy your SSH key to the server.


## Check if the CLI is already installed
You can check if you already have access to the CLI by running the `az` command from your [terminal](../additional/terminals.md):
``` { .console .no-copy }
user@FET-CND1221PKJ:~$ az

     /\
    /  \    _____   _ _  ___ _
   / /\ \  |_  / | | | \'__/ _\
  / ____ \  / /| |_| | | |  __/
 /_/    \_\/___|\__,_|_|  \___|


Welcome to the cool new Azure CLI!
```

If you already have access, move on to the next page to use the CLI to copy your SSH key to the server.

## Installing the CLI
### Windows
The CLI can be installed on Windows by downloading a Microsoft Installer (MSI) from the website:

[Download MSI from Microsoft](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=msi#microsoft-installer-msi){:target="_blank" .md-button}

You can also install the CLI using WinGet (the Windows Package Manager), in a PowerShell window:

``` powershell
winget install --exact --id Microsoft.AzureCLI
```

!!! warning
    If you install the CLI using WinGet, you'll need to close and reopen your terminal window before being able to use the tools.

Once the installation has completed move on to the next page to use the CLI to copy your SSH keys to the server.

### macOS
To install the CLI on macOS you first need to install [Homebrew](https://brew.sh){:target="_blank"}, a package manager. Run the following in your terminal to start the installation:

``` bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the instructions on screen to complete the installation. You might be asked to enter your password as part of the installation, when you type this you won't see any characters appear on screen (like when you set a passphrase for your SSH key) - this is normal! Type in your password and press ++return++ to continue.

!!! warning
    You'll need to close and reopen your terminal window after installing Homebrew before you can continue.

Install the Azure CLI using Homebrew:

``` bash
brew install az
```

Once the installation has completed move on to the next page to use the CLI to copy your SSH keys to the server.

### Linux
The Azure CLI should be available through your Linux distribution's package manager, follow the instructions on the Microsoft website to install. Seek assistance from a lab tutor if you're having difficulties installing.

[Install the Azure CLI on Linux](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt){:target="_blank" .md-button}

Once the installation has completed move on to the next page to use the CLI to copy your SSH keys to the server.