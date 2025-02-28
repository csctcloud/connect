# CSCT Cloud
## Connect
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

## Troubleshooting
### raygui webpage refuses to load
Web page refuses to load at all on a specific machine (but can be loaded on a different machine by manually forwarding the port)

Can verify issue by trying to open the web page with cURL - will see the request fail with bytes unread (ERR_CONTENT_LENGTH_MISMATCH).

* Open settings and search for `remote.ssh.useExecServer` and untick (setting it to false)
* Restart vscode
* Try again

[Github issue](https://github.com/microsoft/vscode-remote-release/issues/9548)


### Permission denied (publickey)
If an SSH config exists (it'll be created when they first setup a connection through vscode), open it up and check:
* User is their full UWE email address (including host portion), spelt correctly, all in lowercase
* Host is `csctcloud.uwe.ac.uk` (spelt correctly)
* IdentityFile either correctly points to `H:\.ssh\id_rsa`, or on personal machines to `C:\Users\X\.ssh\id_rsa`, `/Users/X/.ssh/id_rsa`, or `/home/X/.ssh/id_rsa` (or another properly created keyfile if they've chosen a non-default location), or is omitted (so default keyfile used)

If this is all correct/they haven't got to setting up vscode yet:
* Look in their `.ssh` folder (check this matches what is in SSH config) and check both public and private key are present
* If they don't have a `.ssh` folder - get them to go back to 'Generating a key' section of guide and go from there
* Open up public key in notepad and check not malformed or accidentally overwritten

Get them to connect to the server using Azure CLI (`az login`):
* Have they created the .ssh folder?
* Have they created an authorized_keys file -- is this spelt correctly?!
* In the authorized_keys file have they correctly copied the public key (and not their private key, or saved a blank file etc.)?

If in doubt just generate a new keypair and try copying that...

### Issue with installing Azure CLI SSH extension (`az ssh`)
Installation fails with pip error, running with --debug flag will show problem with winreg.XX function call (file not found). Issue is caused by conflicting Anaconda libraries being included by Azure CLI during extension install.

Temporarily change Anaconda directory to prevent conflict during extension installation:
* Change: `C:/Users/<username>/anaconda3` to `C:/Users/<username>/anaconda3_temp`
* Retry ssh extension installation `az ssh ...`
* Revert anaconda3 directory name back to original