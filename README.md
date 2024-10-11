# CSCT Cloud
## Quick Connect
Current WIP to quickly setup an SSH connection to the server, using `az ssh config` to generate the necessary SSH config and SSH key (and install it on the server) in one step.

Issues:
* Currently needs a login every time -- any way to check if token issued via Azure CLI?
* Halts if `as ssh` extension not yet installed (is this a system wide install?) until interacted with
* Certificate is only issued for an hour -- ideally would be issued for remainder of token life (or configurable) -- [Github Issue](https://github.com/Azure/azure-cli-extensions/issues/3565)

## Troubleshooting
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