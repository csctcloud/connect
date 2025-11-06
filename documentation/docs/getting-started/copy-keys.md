# Copy SSH keys to the server
To be able to connect to the server using public key authentication, you first need to copy your public key (which you created earlier) onto the server and properly configure it.

## Login with Azure CLI
We use the Azure CLI to create an initial connection to the server, which can then be used to copy your key to it.

Open up a [terminal](../additional/terminals.md) window and start the Azure CLI login process:
``` bash
az login
```

This will open up an account selector or browser window, asking you to login to Microsoft Azure. Select your UWE account (or enter your UWE email address), enter your password, and complete the Multi-Factor Authentication (MFA) steps if required. Once you have successfully logged in you can close your browser and return to the terminal.

!!! info
    If you've forgotten your UWE account password, you can use the [Microsoft online password reset tool](https://passwordreset.microsoftonline.com/Default.aspx?whr=uwe.ac.uk){:target="_blank"} to reset it. You will need access to two of your authentication methods you setup when you first logged in to do this.

    If you cannot reset your password or have other issues logging in to your UWE account you will need to contact IT Services on [01173283612](tel:01173283612) - your module tutors cannot help with this.

The first time you connect you might be asked to select which resource to use, enter ++1++ to choose the first option and press ++enter++.

## Use the CLI to connect to the server
Once logged in you can connect to the server using the Azure CLI command:
``` bash
az ssh vm --ip csctcloud.uwe.ac.uk
```

This may ask you to install the Azure CLI ssh extension, enter ++y++ then press ++enter++ to install this.

Once connected to the server you will find yourself at a terminal prompt in your home directory, with this you are now able to run commands on the server.

``` { .console .no-copy }
Welcome to UWE CSCT Cloud

By logging onto this computer, you acknowledge your obligation to
familiarise yourself with and abide by the University’s Acceptable
Use Policy. This Policy sets out the responsibilities and required
behaviours for anyone who makes use of the IT facilities provided
by UWE Bristol and is available from: http://go.uwe.ac.uk/aup

Last login: Wed Nov  5 14:00:46 2025 from 127.0.0.1
user@uwe.ac.uk@csctcloud:~$
```

## Open your public key
Your public key - one half of the SSH keypair you generated earlier - needs to be copied to the server to be able to use it to connect.

Open a new terminal window and use this command to open your public key:
=== "Windows"
    ``` powershell
    type $env:USERPROFILE\.ssh\id_rsa.pub
    ```

=== "macOS/Linux"
    ``` bash
    cat ~/.ssh/id_rsa.pub
    ```

=== "UWE lab computers"
    ``` powershell
    type $env:USERPROFILE'\OneDrive - UWE Bristol\.ssh\id_rsa.pub'
    ```

Select the entire public key (the block of text starting with `ssh-rsa`) and copy it using ++ctrl+c++ (or ++cmd+c++ on a mac).

!!! info
    If you generated your key in a different location, or you used a different public key algorithm, you'll need to change the command to reference that public key instead.

## Save your key on the server
Switch back to the terminal window connected to the server.

!!! info
    You can check you're using the correct terminal window by looking at the prompt - when working on CSCT Cloud it will include the hostname `csctcloud`, like this:
    ``` { .console .no-copy }
    user@uwe.ac.uk@csctcloud:~$
    ```

Create a new directory to store files relating to SSH connections:
``` bash
mkdir ~/.ssh
```

Use nano, a text editing program, to create and edit a file to store your keys:
``` bash
nano ~/.ssh/authorized_keys
```

Paste the public key you copied earlier into this file. You can save the file and exit by pressing ++ctrl+x++, then ++y++ to confirm you want to save the file (`Save modified buffer?`), and ++enter++ to confirm the file name.

!!! info
    If you generate additional sets of SSH keys (e.g. you generate keys both for UWE lab computers, and your own personal computer) you can add these keys by pasting them onto a new line in the `authorized_keys` file. You can then use any of these keys to connect to the server using SSH.

## Securing your keys
You need to set the correct permissions on the directory and file we've just created to prevent unauthorised access, using the following two commands:

``` bash
chmod 744 ~/.ssh
```

``` bash
chmod 644 ~/.ssh/authorized_keys
```

## Testing your SSH keys
You should now be able to connect to the server using your SSH key.

To test this, disconnect from the server using the `exit` command and continue to the next page to connect to the server using your SSH keys.