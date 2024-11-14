#!/bin/bash
az config set core.login_experience_v2=off
az login
rm -rf ~/.ssh/csctcloud
mkdir -p ~/.ssh/csctcloud
az ssh config --ip csctcloud.uwe.ac.uk --file ~/.ssh/config --keys-destination-folder ~/.ssh/csctcloud
code -n --remote ssh-remote+csctcloud.uwe.ac.uk