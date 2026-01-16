# Quick Connect
A python script for Windows machines to bootstrap a connection to the server using the Azure CLI tools to login a user and generate SSH keys.

Can be built into a standalone executable for easier distribution to campus machines.

For troubleshooting, a logfile (`csctcloud-connect.log`) is created in the users home directory.

```
usage: CSCT Cloud Connect [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Sets up an SSH configuration and necessary keys to establish a connection to the CSCT Cloud server, using the Azure CLI tools

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level to run program under
```

Issues:
* Certificate is only issued for an hour -- ideally would be issued for remainder of token life (or configurable) -- [Github Issue](https://github.com/Azure/azure-cli-extensions/issues/3565)

## Build
From target OS (i.e. Windows for builds to be deployed to UWE lab machines)

* Create a python virtual environment
* Install [pyinstaller](https://pypi.org/project/pyinstaller/)
* Run `build.py`, built binary will be in a version/target os zip
* Pass on binary to be deployed

## Deployment
CSCT Cloud Connect is on the software deployment list so should continue being deployed to labs when they're rebuilt. Contact the Software Delivery team to request an update to deployed version or to have connect deployed to more labs/teaching spaces.
