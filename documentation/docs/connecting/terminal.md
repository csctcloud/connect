# Connect to the server using a terminal
Once you've copied your public key to the server, you can connect by entering the following command in a [terminal](../additional/terminals.md) window:

``` bash
ssh <UWE email address>@csctcloud.uwe.ac.uk
```

!!! tip "UWE lab computers"
    If you're using a UWE lab computer you need to enter a modified version of this command to use the version of your key stored on OneDrive instead:

    ``` powershell
    ssh -i $env:USERPROFILE'\OneDrive - UWE Bristol\.ssh\id_rsa' <UWE email address>@csctcloud.uwe.ac.uk
    ```

    If you chose to use a different public key algorithm when you generated your key you'll need to update the command to reference that key.

Replace `<UWE email address>` with your full UWE email address, making sure it is completely in lowercase and then press ++return++ to run the command.

!!! example
    If your email address was `A.Student@live.uwe.ac.uk` you would connect using the command:

    ``` { .bash .no-copy }
    ssh a.student@live.uwe.ac.uk@csctcloud.uwe.ac.uk
    ```

When prompted, enter the passphrase for your key if you set one.

If you've successfully connected you should find yourself in a terminal session on the server:
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

<!-- ## Troubleshooting
If you're having problems connecting, or are receiving an error (`Permission denied (publickey)`) then you should follow the steps in the [troubleshooting guide](../troubleshooting/publickey.md). -->

## What next?
If you're new to entering and running commands using a terminal, Linux Journey has some good tutorials on [using the command line](https://labex.io/lesson/the-shell){:target="_blank"} and [working with text](https://labex.io/lesson/stdout-standard-out-redirect){:target="_blank"}.

If you wanted, you could stop here and only work using the terminal and terminal based text editors like `nano`, `emacs` or `vim` - which is best is a [contentious topic](https://xkcd.com/378/){:target="_blank"}!

Most students will want to continue to the next page to setup Visual Studio Code to connect to the server however.