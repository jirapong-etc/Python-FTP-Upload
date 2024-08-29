# FTP Deployer by jirapong-etc

This is a Python-based FTP deployment script that allows you to upload files or directories to an FTP server. The script provides options to upload files immediately, schedule uploads, and manage the contents of the remote directory.

## Features

- **Immediate Upload**: Upload files or directories to the FTP server right away.
- **Scheduled Upload**: Schedule uploads at a specific time.
- **Fresh Mode**: Remove files from the remote directory if they not exist locally.
- **Selective Upload**: Upload only a specified file or directory.
- **Ignore List**: Skip specific files or directories during the upload process.

## Prerequisites

Make sure you have Python installed on your system. The script requires the following Python modules:

- `argparse`
- `schedule`
- `ftplib`

You can install the required modules using `pip`:

```bash
pip install argparse schedule
```

## Installation
1. Clone or download the script to your local machine:

```bash
git clone https://github.com/jirapong-etc/Python-FTP-Upload.git
cd Python-FTP-Upload
 ```
2. Open the script (deployer.py) and update the following FTP server details with your credentials:

```bash
self.host = 'localhost'
self.username = 'ftp_user'
self.passwd = 'ftp_password'
self.port = 21
```

## Usage

You can run the script using Python. The script offers various options to customize the behavior:

### Command-Line Arguments
- `-n`, `--now`: Immediately upload the files.
- `-f`, `--fresh`: Remove files from the remote directory if they exist locally.
- `-t`, `--time`: Schedule the upload at a specific time (format: 'HH:MM').
- `-p`, `--path`: Upload only the specified file or directory.

## Example Usage

1. Immediate Upload:
```bash
python deployer.py --now
```
2. Scheduled Upload:
```bash
python deployer.py --time "23:59"
```
3. Selective Upload:
```bash
python deployer.py --path "/path/to/your/file_or_directory"
```

### Interactive Mode
If no arguments are provided, the script will prompt you to choose between uploading immediately or scheduling an upload:
```bash
python deployer.py
```
The script will present the following options:

```bash
1. Upload now.
2. Set upload time.
Enter number of choices. : 
```
Select an option to proceed with the desired action.

### Ignore List
The script has a predefined list of files and directories to ignore during the upload process. You can customize this list by modifying the self.ignore_extensions and self.ignore_files variables in the script.
