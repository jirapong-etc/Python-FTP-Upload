import os.path, os, sys
import argparse
import schedule
import time as tm
from ftplib import FTP, error_perm

class Deployer:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Basic FTP program by jirapong-etc")
        parser.add_argument('-f', '--fresh', action="store_true", help="Remove files from the remote directory if they exist locally.")
        parser.add_argument('-t', '--time', help="Schedule the upload at a specific time (format: 'HH:MM').")
        parser.add_argument('-p', '--path', help="Upload only the specified file or directory.")
        self.parser = parser.parse_args()
        
        self.host = 'localhost'
        self.username = 'ftp_user'
        self.passwd = 'ftp_password'
        self.port = 21
        self.path = '.'
        self.ftp_dir = '.'
        self.time = None
        self.mode = 0 #0 none select, 1 at time, 2 upload now

        # List of file extensions to ignore
        self.ignore_extensions = [
            'env',
            'vs',
            'vscode',
            'ignore',
            'gitignore',
            'gitattributes'
        ]

        #List of file name to ignore
        self.ignore_files = [
            '.\\.env.backup',
            '.\\.env.production',
            '.\\.phpunit.result.cache',
            '.\\.fleet',
            '.\\.idea',
            '.\\.git',
            '.\\.editorconfig',
            '.\\Homestead.json',
            '.\\Homestead.yaml',
            '.\\auth.json',
            '.\\npm-debug.log',
            '.\\yarn-error.log',
            '.\\deployer.py',
            '.\\deploy.log',
            '.\\public\\hot',
            '.\\public\\storage',
            '.\\tests',
            '.\\deployer.py.example',
            '.\\temps',
            '.\\storage',
            '.\\node_modules',
            '.\\vendor',
        ]

    def main(self, argv):
        if self.parser.time is not None:
            schedule.every().day.at(self.parser.time).do(self.job)
            self.schedule_task()
        else:
            self.job()

    def checkIgnore(self, file_name):
        # Check if the file extension is in the ignore list
        if file_name.split('.')[-1] in self.ignore_extensions:
            return True
        
        # Check if the file name is in the ignore list
        if file_name in self.ignore_files:
            return True
        
        return False

    def placeFiles(self, ftp, path):
        if self.parser.fresh:
            for name in ftp.nlst():
                local_path = os.path.join(path, name)
                # Check ignore file
                if self.checkIgnore(local_path):
                    print(f"Ignore Delete \t\t{local_path}")
                    continue
                elif not name in os.listdir(path):
                    self.deleteFilesAndDirectory(ftp, name)

        for name in os.listdir(path):
            local_path = os.path.join(path, name)

            # Check ignore file
            if self.checkIgnore(local_path):
                print(f"Ignore STOR \t\t{local_path}")
                continue

            if os.path.isfile(local_path):
                # writeLog("STOR "+ local_path)
                print(f"STOR \t\t\t{local_path}")

                # Use 'wb' mode to overwrite existing files
                ftp.storbinary('STOR ' + name, open(local_path,'rb'))

                # During times
                tm.sleep(0.01)

            elif os.path.isdir(local_path):
                try:
                    ftp.mkd(name)
                    print(f"MKD \t\t\t{local_path}")

                # ignore "directory already exists"
                except error_perm as e:
                    if not e.args[0].startswith('550'): 
                        raise

                ftp.cwd(name)
                print(f"CWD \t\t\t{local_path}")
                self.placeFiles(ftp, local_path)
                ftp.cwd("..")
                print(f"CWD \t\t\t{path}")

    def deleteFilesAndDirectory(self, ftp, directory):
        ftp_path = ftp.pwd()
        ftp_path = "."+ftp_path.replace("/", "\\")
        ftp_path = os.path.join(ftp_path, directory)

        if self.checkIgnore(ftp_path):
            return

        try:
            ftp.delete(directory)
            print(f"Deleted file: \t\t{ftp_path}")
        except error_perm:
            # Change to the target directory
            ftp.cwd(directory)

            # List all files and directories in the directory
            items = ftp.nlst()

            for item in items:
                self.deleteFilesAndDirectory(ftp, item)

            ftp.cwd("..")
            try:
                ftp.rmd(directory)
                print(f"Deleted directory: \t{ftp_path}")
                print()
            except error_perm as e:
                pass

    def job(self):
        ftp = FTP()
        ftp.connect(self.host,self.port)
        ftp.login(self.username,self.passwd)

        # Change Directory To Project Folder
        if self.parser.path is not None:
            if os.path.isfile(self.parser.path):
                try:
                    ftp.cwd(os.path.dirname(self.parser.path))
                except error_perm:
                    ftp.mkd(os.path.dirname(self.parser.path))
                    ftp.cwd(os.path.dirname(self.parser.path))

                ftp.storbinary('STOR ' + os.path.basename(self.parser.path), open(self.parser.path, 'rb'))
                print(f"STOR \t\t\t{self.parser.path}")
            else:
                try:
                    ftp.cwd(self.parser.path)
                except error_perm:
                    ftp.mkd(self.parser.path)
                    ftp.cwd(self.parser.path)
                self.placeFiles(ftp, self.parser.path)
        else:
            if self.ftp_dir == '.':
                self.placeFiles(ftp, self.path)
            else:
                ftp.cwd(self.ftp_dir)
                self.placeFiles(ftp, self.path)

        ftp.quit()

        if self.parser.time is not None:
            schedule.CancelJob
        exit()
    
    def schedule_task(self):
        while True:
            schedule.run_pending()
            tm.sleep(1)

if __name__ == "__main__":
    app = Deployer()
    app.main(sys.argv)