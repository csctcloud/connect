# Quick Connect
A python script for Windows machines to bootstrap a connection to the server using the Azure CLI tools to login a user and generate SSH keys.

Can be built into a standalone executable for easier distribution to campus machines.

For troubleshooting, a logfile (`csctcloud-connect.log`) is created in the users home directory.

```
usage: CSCT Cloud Connect [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-o]

Sets up an SSH configuration and necessary keys to establish a connection to the CSCT Cloud server, using the Azure CLI tools

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level to run program under
  -o, --overwrite       allow SSH configuration file to be overwritten
```

Issues:
* Certificate is only issued for an hour -- ideally would be issued for remainder of token life (or configurable) -- [Github Issue](https://github.com/Azure/azure-cli-extensions/issues/3565)