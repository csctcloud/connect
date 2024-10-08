az config set core.login_experience_v2=off
az login

if exist "C:\Users\%username%\.ssh\csctcloud\" (
    del /q "C:\Users\%username%\.ssh\csctcloud"
    rmdir "C:\Users\%username%\.ssh\csctcloud"
)

az ssh config --ip csctcloud.uwe.ac.uk --file "C:\Users\%username%\.ssh\config" --keys-destination-folder "C:\Users\%username%\.ssh\csctcloud"
code -n --remote ssh-remote+csctcloud.uwe.ac.uk