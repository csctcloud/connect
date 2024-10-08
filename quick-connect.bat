@ECHO OFF

REM can we check here if az has a valid token and skip?
CALL az config set core.login_experience_v2=off
CALL az login

IF EXIST "C:\Users\%username%\.ssh\csctcloud\" (
    del /q "C:\Users\%username%\.ssh\csctcloud"
    rmdir "C:\Users\%username%\.ssh\csctcloud"
)

REM can we check here if certificate is still valid and/or if config has entry, and skip? (or combination of this?)
CALL az ssh config --ip csctcloud.uwe.ac.uk --file "C:\Users\%username%\.ssh\config" --keys-destination-folder "C:\Users\%username%\.ssh\csctcloud"

CALL code -n --remote ssh-remote+csctcloud.uwe.ac.uk