az config set core.login_experience_v2=off
az login
del "C:\Users\%username%\.ssh\csctcloud"
mkdir -p "C:\Users\%username%\.ssh\csctcloud"
az ssh config --ip csctcloud.uwe.ac.uk --file "C:\Users\%username%\.ssh\config" --keys-destination-folder "C:\Users\%username%\.ssh\csctcloud"
code -n --remote ssh-remote+csctcloud.uwe.ac.uk