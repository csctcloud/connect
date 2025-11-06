---
hide:
    - footer
---
# Installing OpenSSH
OpenSSH is a tool used for remotely logging into servers using the SSH protocol. It's normally already included in modern operating systems but if you're using an older version of Windows you'll need to install it to be able to generate SSH keys and launch SSH connections.

!!! info
    You can check if OpenSSH is installed by entering the `ssh` command in a [terminal](./terminals.md) window - if you get an output similar to the one below it is properly installed:

    ``` console
    usage: ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface] [-b bind_address]
           [-c cipher_spec] [-D [bind_address:]port] [-E log_file]
           [-e escape_char] [-F configfile] [-I pkcs11] [-i identity_file]
           [-J destination] [-L address] [-l login_name] [-m mac_spec]
           [-O ctl_cmd] [-o option] [-P tag] [-p port] [-Q query_option]
           [-R address] [-S ctl_path] [-W host:port] [-w local_tun[:remote_tun]]
           destination [command [argument ...]]
    ```

## Installing on Windows
Follow the instructions on the Microsoft website to install OpenSSH:

[Install OpenSSH Server and Client](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell&pivots=windows-11#install-openssh-server--client){:target="_blank" .md-button}