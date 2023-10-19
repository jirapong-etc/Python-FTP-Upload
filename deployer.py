import os.path, os, sys, getopt
import schedule
import time as tm
from ftplib import FTP, error_perm

class Deployer:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.username = 'ftp_user'
        self.passwd = 'ftp_password'
        self.port = 21
        self.path = '.'
        self.ftp_dir = '.'
        self.time = None
        self.mode = 0 #0 none select, 1 at time, 2 upload now

        # List of file extensions to ignore
        self.ignore_extensions = []

        #List of file name to ignore
        self.ignore_files = [
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

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], "hnt:", ["help", "now", "time="])
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('usage python '+argv[0]+' [option] ... [-e | -d] ... [arg]')
                print('options:')
                print('    -n \t --now \t : Upload files now')
                print('    -t \t --time \t : Set time to upload format is \'23:59\'')
            elif opt in ("-n", "--now"):
                self.mode = 2
            elif opt in ("-t", "--time"):
                self.mode = 1
                self.time = arg
        
        match self.mode:
            case 0 :
                print("\n     1.Upload now.")
                print("     2.Set upload time.")
                ch = int(input("\nEnter number of choices. : "))
                if ch == 1:
                    self.job()
                elif ch == 2:
                    self.time = input("Enter time ex.\"23:59\" : ")
                    schedule.every().day.at(self.time).do(self.job)
                    self.schedule_task()
            case 1 :
                schedule.every().day.at(self.time).do(self.job)
                self.schedule_task()
            case 2 :
                self.job()

    def checkIgnore(self, file_name):
        # Check if the file extension is in the ignore list
        if os.path.splitext(file_name)[1] in self.ignore_extensions:
            return True
        
        # Check if the file name is in the ignore list
        if file_name in self.ignore_files:
            return True
        
        return False

    def placeFiles(self, ftp, path):
        for name in os.listdir(path):
            local_path = os.path.join(path, name)

            # Check ignore file
            if self.checkIgnore(local_path):
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
                self.placeFiles(ftp, local_path)
                ftp.cwd("..")

    def job(self):
        ftp = FTP()
        ftp.connect(self.host,self.port)
        ftp.login(self.username,self.passwd)

        # Change Directory To Project Folder
        if self.ftp_dir == '.':
            self.placeFiles(ftp, self.path)
        else:
            ftp.cwd(self.ftp_dir)
            self.placeFiles(ftp, self.path)

        ftp.quit()

        if self.mode == 1:
            schedule.CancelJob
        exit()
    
    def schedule_task(self):
        while True:
            schedule.run_pending()
            tm.sleep(1)

if __name__ == "__main__":
    app = Deployer()
    app.main(sys.argv)