## Python-FTP-Upload
- options
  <pre>-h    --help : View option list
-n    --now : เริ่มอัพโหลดทันที
-t    --time : ตั้งเวลาในการอัพโหลด ตัวอย่างการใช้งาน : python deployer.py -t 23:59 | python deployer.py --time=23:59</pre>

- variables
on <code>def __init__(self) -> None:</code>
  <pre>self.path : กำหนดที่อยู่ของไฟล์ที่ต้องการอัพโหลด
self.ftp_dir : กำหนดที่อยู่ที่อยู่ปลายทางบนFTPที่ต้องการอัพโหลดไป</pre>
