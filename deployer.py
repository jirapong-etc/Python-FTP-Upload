import os.path, os
import schedule
import time as tm
from ftplib import FTP, error_perm

# List of file extensions to ignore
ignore_extensions = []

#List of file name to ignore
ignore_files = [
    '.\public\build',
    '.\public\hot',
    '.\public\storage',
    '.\storage\*.key',
    '.\.env',
    '.\.env.backup',
    '.\.env.production',
    '.\.phpunit.result.cache',
    '.\Homestead.json',
    '.\Homestead.yaml',
    '.\auth.json',
    '.\npm-debug.log',
    '.\yarn-error.log',
    '.\.fleet',
    '.\.idea',
    '.\.vs',
    '.\.vscode',
    '.\.ignore',
    '.\deployer.py',
    '.\deploy.log',
    '.\storage',
    '.\tests',
    '.\.editorconfig',
    '.\deployer.py.example'
]

ftp = FTP()

host = 'localhost'
username = 'jiraphong'
password = '0123456789'
port = 21
filenameCV = "."
log_path = "deploy.log"

# Write a log file
def writeLog(text):
    with open(log_path, 'a+') as file:
        # Write data to the file
        file.write(text+'\n')

# Check ignore fn
def checkIgnore(file_name):
    # Check if the file extension is in the ignore list
    if os.path.splitext(file_name)[1] in ignore_extensions:
        return True
    
    # Check if the file name is in the ignore list
    if file_name in ignore_files:
        return True
    
    return False

def placeFiles(ftp, path):
    for name in os.listdir(path):
        local_path = os.path.join(path, name)

        # Check ignore file
        if checkIgnore(local_path):
            # writeLog("Ignore "+ local_path)
            print("Ignore", local_path)
            continue

        if os.path.isfile(local_path):
            # writeLog("STOR "+ local_path)
            print("STOR", local_path)

            # Use 'wb' mode to overwrite existing files
            ftp.storbinary('STOR ' + name, open(local_path,'rb'))

        elif os.path.isdir(local_path):
            # writeLog("MKD "+ local_path)
            print("MKD", local_path)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            ftp.cwd(name)
            placeFiles(ftp, local_path)
            ftp.cwd("..")

def job():
    ftp.connect(host,port)
    ftp.login(username,password)

    # Change Directory To Project Folder
    # ftp.cwd("test.lims")
    placeFiles(ftp, filenameCV)

    ftp.quit()

    schedule.CancelJob
    exit()

# Deploy time
schedule.every().day.at('23:59').do(job)
while True:
    schedule.run_pending()
    tm.sleep(1)