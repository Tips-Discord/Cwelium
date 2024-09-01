# Copyright (c) 2024 Cwelium Inc.
# This project is licensed under the Cwelium License, which includes additional
# terms under the GNU Affero General Public License (AGPL) v3.0.
#
# Author: Tips-Discord
# Original Repository: https://github.com/Tips-Discord/Cwelium
#
# Additional Terms can be found at:
# https://github.com/Tips-Discord/Cwelium/blob/main/LICENSE

#from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from colorist import ColorHex as h
from datetime import datetime
import re
import base64
import ctypes
import json
import os
import random
import requests
import threading
import time
import tls_client
import uuid
import websocket

session = tls_client.Session(client_identifier="chrome_126",random_tls_extension_order=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def wrapper(func):
    def wrapper(*args, **kwargs):
        clear()
        console.render_ascii()
        result = func(*args, **kwargs)
        return result
    return wrapper

def title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

C = {
    "green": h("#65fb07"),
    "red": h("#Fb0707"),
    "yellow": h("#FFCD00"),
    "magenta": h("#b207f5"),
    "blue": h("#00aaff"),
    "cyan": h("#aaffff"),
    "gray": h("#8a837e"),
    "white": h("#DCDCDC"),
    "pink": h("#c203fc"),
    "light_blue": h("#07f0ec"),
    "brown": h("#8B4513"),
    "black": h("#000000"),
    "aqua": h("#00CED1"),
    "purple": h("#800080"),
    "lime": h("#00FF00"),
    "orange": h("#FFA500"),
    "indigo": h("#4B0082"),
    "violet": h("#EE82EE"),
    "gold": h("#FFD700"),
    "silver": h("#C0C0C0"),
    "teal": h("#008080"),
    "navy": h("#000080"),
    "olive": h("#808000"),
    "maroon": h("#800000"),
    "coral": h("#FF7F50"),
    "salmon": h("#FA8072"),
    "khaki": h("#F0E68C"),
    "orchid": h("#DA70D6")
}

class Files:
    @staticmethod
    def write_config():
        try:
            if not os.path.exists("config.json"):
                data = {
                    "Proxies": False,
                    "Theme": "light_blue", 
                    "Solver": False,
                    "Service": "",
                    "Api-Key": "",
                }
                with open("config.json", "w") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Write Config", e)

    @staticmethod
    def write_folders():
        folders = ["data", "scraped"]
        for folder in folders:
            try:
                if not os.path.exists(folder):
                    os.mkdir(folder)
            except Exception as e:
                console.log("FAILED", C["red"], "Failed to Write Folders", e)

    @staticmethod
    def write_files():
        files = ["tokens.txt", "proxies.txt"]
        for file in files:
            try:
                if not os.path.exists(file):
                    with open(f"data/{file}", "a") as f:
                        f.close()
            except Exception as e:
                console.log("FAILED", C["red"], "Failed to Write Files", e)

    @staticmethod
    def run_tasks():
        tasks = [Files.write_config, Files.write_folders, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()

with open("data/proxies.txt") as f:
    proxies = f.read().splitlines()

with open("config.json") as f:
    Config = json.load(f)

with open("data/tokens.txt", "r") as f:
    tokens = f.read().splitlines()
    
proxy = Config["Proxies"]
color = Config["Theme"]
solver = Config["Solver"]
service = Config["Service"].lower()
Key = Config["Api-Key"]

if proxy:
    selected_proxy = random.choice(proxies)
    session.proxies = {
        "http": f"http://{selected_proxy}", 
        "https": f"http://{selected_proxy}"
    }

class Render:
    def __init__(self):
        self.size = os.get_terminal_size().columns
        if not color:
            self.background = C["light_blue"]
        else:
            self.background = C[color]

    def render_ascii(self):
        clear()
        title(f"Cwelium | Connected as {os.getlogin()} | made by Tips-Discord")
        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        ascii = f"""
{' ██████╗██╗    ██╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗'.center(self.size)}
{'██╔════╝██║    ██║██╔════╝██║     ██║██║   ██║████╗ ████║'.center(self.size)}
{'██║     ██║ █╗ ██║█████╗  ██║     ██║██║   ██║██╔████╔██║'.center(self.size)}
{'██║     ██║███╗██║██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║'.center(self.size)}
{'╚██████╗╚███╔███╔╝███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║'.center(self.size)}
{' ╚═════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝'.center(self.size)}
"""
        for edge in edges:
            ascii = ascii.replace(edge, f"{self.background}{edge}{C['white']}")
        print(ascii)

    def raider_options(self):
        with open("data/proxies.txt") as f:
            proxies = f.read().splitlines()
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()

        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        title = f"""{' '*41}{Fore.RESET} Loaded ‹{self.background}{len(tokens)}{Fore.RESET}› tokens | Loaded ‹{self.background}{len(proxies)}{Fore.RESET}> proxies

{'╭─────────────────────────────────────────────────────────────────────────────────────────────╮'.center(self.size)}
{'│ «01» Joiner            «07» Token Formatter    «13» Onliner           «19» Call Spammer     │'.center(self.size)}
{'│ «02» Leaver            «08» Button Click       «14» Voice Raper       «20» Bio Change       │'.center(self.size)}
{'│ «03» Spammer           «09» Accept Rules       «15» Change Nick       «21» Voice Joiner     │'.center(self.size)}
{'│ «04» Token Checker     «10» Guild Check        «16» Thread Spammer    «22» Onboard Bypass   │'.center(self.size)}
{'│ «05» Emoji Reaction    «11» Friend Spam        «17» Typer             «23» Dm Spammer       │'.center(self.size)}
{'│ «06» ???               «12» ???                «18» ???               «24» ???              │'.center(self.size)}
{'╰─────────────────────────────────────────────────────────────────────────────────────────────╯'.center(self.size)}
"""
        for edge in edges:
            title = title.replace(edge, f"{self.background}{edge}{C['white']}")
        print(title)

    def run(self):
        options = [self.render_ascii(), self.raider_options()]
        ([option] for option in options)

    def log(self, text=None, color=None, token=None, log=None):
        response = f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] "
        if text:
            response += f"[{color}{text}{C['white']}] "
        if token:
            response += token
        if log:
            response += f" ({C['gray']}{log}{C['white']})"
        print(response)

    def prompt(self, text, ask=None):
        response = f"[{C[f'{color}']}{text}{C['white']}"
        if ask:
            response += f"? {C['gray']}(y/n){C['white']}]: "
        else:
            response += f"]: "
        return response

console = Render()

# Big Thanks to Aniell4 for the scraper
class Utils:
    @staticmethod
    def range_corrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    @staticmethod
    def get_ranges(index, multiplier, member_count):
        initial_num = int(index * multiplier)
        ranges = [[initial_num, initial_num + 99]]
        if member_count > initial_num + 99:
            ranges.append([initial_num + 100, initial_num + 199])
        return Utils.range_corrector(ranges)

    @staticmethod
    def parse_member_list_update(response):
        data = response["d"]
        member_data = {
            "online_count": data["online_count"],
            "member_count": data["member_count"],
            "id": data["id"],
            "guild_id": data["guild_id"],
            "hoisted_roles": data["groups"],
            "types": [op["op"] for op in data["ops"]],
            "locations": [],
            "updates": [],
        }

        for chunk in data["ops"]:
            op_type = chunk["op"]
            if op_type in {"SYNC", "INVALIDATE"}:
                member_data["locations"].append(chunk["range"])
                member_data["updates"].append(chunk["items"] if op_type == "SYNC" else [])
            elif op_type in {"INSERT", "UPDATE", "DELETE"}:
                member_data["locations"].append(chunk["index"])
                member_data["updates"].append(chunk["item"] if op_type != "DELETE" else [])

        return member_data

class DiscordSocket(websocket.WebSocketApp):
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.blacklisted_ids = {"1100342265303547924", "1190052987477958806", "1125147653970337896", "833007032000446505"}

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0.0.0 Safari/537.36"),
        }

        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
        )

        self.end_scraping = False
        self.guilds = {}
        self.members = {}
        self.ranges = [[0, 0]]
        self.last_range = 0
        self.packets_recv = 0

    def run(self):
        self.run_forever()
        return self.members

    def scrape_users(self):
        if not self.end_scraping:
            self.send(json.dumps({
                "op": 14,
                "d": {
                    "guild_id": self.guild_id,
                    "typing": True,
                    "activities": True,
                    "threads": True,
                    "channels": {self.channel_id: self.ranges}
                }
            }))

    def on_open(self, ws):
        self.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows NT",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "it-IT",
                    "browser_user_agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                                           "Chrome/126.0.0.0 Safari/537.36"),
                    "browser_version": "126.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 311885,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))

    def heartbeat_thread(self, interval):
        while not self.end_scraping:
            self.send(json.dumps({"op": 1, "d": self.packets_recv}))
            time.sleep(interval)

    def on_message(self, ws, message):
        decoded = json.loads(message)
        if not decoded:
            return

        if decoded["op"] != 11:
            self.packets_recv += 1

        if decoded["op"] == 10:
            threading.Thread(
                target=self.heartbeat_thread,
                args=(decoded["d"]["heartbeat_interval"] / 1000,),
                daemon=True,
            ).start()

        if decoded["t"] == "READY":
            self.guilds.update({guild["id"]: {"member_count": guild["member_count"]} for guild in decoded["d"]["guilds"]})

        if decoded["t"] == "READY_SUPPLEMENTAL":
            self.ranges = Utils.get_ranges(0, 100, self.guilds[self.guild_id]["member_count"])
            self.scrape_users()

        elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
            parsed = Utils.parse_member_list_update(decoded)
            if parsed["guild_id"] == self.guild_id:
                self.process_updates(parsed)

    def process_updates(self, parsed):
        if "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]:
            for i, update_type in enumerate(parsed["types"]):
                if update_type == "SYNC":
                    if not parsed["updates"][i]:
                        self.end_scraping = True
                        break
                    self.process_members(parsed["updates"][i])
                elif update_type == "UPDATE":
                    self.process_members(parsed["updates"][i])

                self.last_range += 1
                self.ranges = Utils.get_ranges(self.last_range, 100, self.guilds[self.guild_id]["member_count"])
                time.sleep(0.45)
                self.scrape_users()

        if self.end_scraping:
            self.close()

    def process_members(self, updates):
        for item in updates:
            if "member" in item:
                member = item["member"]
                user_id = member["user"]["id"]
                if user_id not in self.blacklisted_ids and not member["user"].get("bot"):
                    user_info = {
                        "tag": f"{member['user']['username']}#{member['user']['discriminator']}",
                        "id": user_id,
                    }
                    self.members[user_id] = user_info

    def on_close(self, ws, close_code, close_msg):
        console.log("Success", C["green"], False, f"scraped {len(self.members)} members")

def scrape(token, guild_id, channel_id):
    sb = DiscordSocket(token, guild_id, channel_id)
    return sb.run()
        
class Solver:
    @staticmethod
    def solve_2cap():
        try:
            response = requests.post(
                "http://2captcha.com/in.php",
                data={
                    "key": Key,
                    "method": "hcaptcha",
                    "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",
                    "pageurl": "https://discord.com/"
                }
            ).text

            captcha_id = response.split("|")[1]

            while True:
                time.sleep(5)
                result = requests.get(
                    f"http://2captcha.com/res.php?key={Key}&action=get&id={captcha_id}"
                ).text
                if result == "CAPCHA_NOT_READY":
                    continue
                elif result.startswith("OK|"):
                    return result.split("|")[1]
                else:
                    raise Exception("Error solving captcha")
        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    @staticmethod
    def solve_capmonster():
        create_task_payload = {
            "clientKey": Key,
            "task": {
                "type": "HCaptchaTaskProxyless",
                "websiteURL": "https://discord.com/",
                "websiteKey": "4c672d35-0701-42b2-88c3-78380b0db560"
            }
        }

        try:
            create_task_response = requests.post("https://api.capmonster.cloud/createTask", json=create_task_payload).json()

            if create_task_response["errorId"] != 0:
                raise Exception(f"Error creating task: {create_task_response['errorDescription']}")

            task_id = create_task_response["taskId"]

            while True:
                result_response = requests.post("https://api.capmonster.cloud/getTaskResult", json={"clientKey": Key, "taskId": task_id}).json()

                if result_response["status"] == "ready":
                    return result_response["solution"]["gRecaptchaResponse"]

                if result_response["errorId"] != 0:
                    raise Exception(f"Error fetching result: {result_response['errorDescription']}")

                time.sleep(5)

        except requests.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
class Raider:
    def __init__(self):
        self.cookies = self.get_discord_cookies()
        self.props = self.super_properties()
        self.ws = websocket.WebSocket()

    def get_discord_cookies(self):
        try:
            response = requests.get(
                'https://discord.com',
            )
            match response.status_code:
                case 200:
                    return "; ".join(
                        [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                    ) + "; locale=en-US"
                case _:
                    console.log("ERROR", C["red"], "Failed to get cookies using Static")
                    return "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=62f9e16100a211ef8089eda5bffbf7f98e904ba04346eacdf57ee4af97bdd94e4c16f7df1db5132bea9132dd26b21a2a; __cfruid=a2ccd7637937e6a41e6888bdb6e8225cd0a6f8e0-1714045775; _cfuvid=s_CLUzmUvmiXyXPSv91CzlxP00pxRJpqEhuUgJql85Y-1714045775095-0.0.1.1-604800000; locale=en-US"
        except Exception as e:
            console.log("ERROR", C["red"], "get_discord_cookies", e)

    def super_properties(self):
        try:
            payload = {
                "os": "Windows",
                "browser": "Discord Client",
                "release_channel": "stable",
                "client_version": "1.0.9161",
                "os_version": "10.0.19045",
                "system_locale": "en",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9161 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36",
                "browser_version": "30.2.0",
                "os_sdk_version":"19045",
                "client_build_number": 323539,
                "native_build_number": 51643,
                "client_event_source": None,
            }
            properties = base64.b64encode(json.dumps(payload).encode()).decode()
            return properties
        except Exception as e:
            console.log("ERROR", C["red"], "get_super_properties", e)

    def headers(self, token):
        return {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en",
            "authorization": token,
            "cookie": self.cookies,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9161 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-super-properties": self.props,
        }
    
    def nonce(self):
        return str((int(time.mktime(datetime.now().timetuple())) * 1000 - 1420070400000) * 4194304)

    def joiner(self, token, invite):
        try:
            headers = self.headers(token)
            data = {
                "session_id": uuid.uuid4().hex
            }

            response = session.post(
                f"https://canary.discord.com/api/v9/invites/{invite}",
                headers=headers,
                json=data
            )

            match response.status_code:
                case 200:
                    console.log(f"JOINED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"{response.json()['guild']['name']}")
                case 400:
                    console.log("CAPTCHA", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"discord.gg/{invite}")
                    if solver:
                        headers["x-context-properties"] = "eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9=="
                        headers["x-captcha-rqtoken"] = response.json()["captcha_rqtoken"]

                        if service == "capmonster":
                            headers["x-captcha-key"] = Solver.solve_capmonster()
                            payload = {
                                "session_id": uuid.uuid4().hex,
                            }
                        else:
                            headers["x-captcha-key"] = Solver.solve_2cap()
                            payload = {
                                "session_id": uuid.uuid4().hex,
                            }
                            
                        newresponse = session.post(
                            f"https://discord.com/api/v9/invites/{invite}",
                            headers=headers, 
                            json=payload
                        )

                        match newresponse.status_code:
                            case 200:
                                console.log(f"JOINED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"{response.json()['guild']['name']}")
                            case _:
                                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                case 429:
                    console.log("CLOUDFARE", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"discord.gg/{invite}")
                case _:
                    console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def leaver(self, token, guild):
        try:
            def get_guild_name(guild):
                in_guild = []
                for token in tokens:
                    response = session.get(
                        f"https://canary.discord.com/api/v9/guilds/{guild}",
                        headers=self.headers(token)
                    )

                    match response.status_code:
                        case 200:
                            in_guild.append(token)
                            try:
                                return response.json().get("name")
                            except:
                                return guild
                if not in_guild:
                    return guild
                
            self.guild = get_guild_name(guild)

            payload = {
                "lurking": False,
            }

            while True:
                response = session.delete(
                    f"https://canary.discord.com/api/v9/users/@me/guilds/{guild}",
                    json=payload,
                    headers=self.headers(token)
                )

                match response.status_code:
                    case 204:
                        console.log("LEFT", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", self.guild)
                        break
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def vc_joiner(self, token, guild, channel, ws):
        try:
            for _ in range(1):
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "$os": "windows",
                            "$browser": "Discord",
                            "$device": "desktop"
                        }
                    }
                }))

                ws.send(json.dumps({
                    "op": 4,
                    "d": {
                        "guild_id": guild,
                        "channel_id": channel,
                        "self_mute": False,
                        "self_deaf": False
                    }
                }))

                console.log("Joined", C["light_blue"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def onliner(self, token, ws):
        try:
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            ws.send(
                json.dumps(
                    {
                        "op": 2,
                        "d": {
                            "token": token,
                            "properties": {
                                "$os": "Windows",
                            },
                        },
                    }
                )
            )
            console.log("Onlined", C["light_blue"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def member_scrape(self, guild_id, channel_id):
        try:
            in_guild = []

            if not os.path.exists(f"scraped/{guild_id}.txt"):
                for token in tokens:
                    response = session.get(
                        f"https://canary.discord.com/api/v9/guilds/{guild_id}",
                        headers=self.headers(token),
                    )

                    match response.status_code:
                        case 200:
                            in_guild.append(token)
                            break

                if not in_guild:
                    console.log("Failed", C["red"], "Missing Access")
                token = random.choice(in_guild)
                members = scrape(token, guild_id, channel_id)
                with open(f"scraped/{guild_id}.txt", "a") as f:
                    f.write("\n".join(members))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def get_random_members(self, guild_id, count):
        try:
            with open(f"scraped/{guild_id}.txt") as f:
                members = f.read().splitlines()
            message = ""
            for _ in range(int(count)):
                message += f"<@!{random.choice(members)}>"
            return message
        except Exception as e:
            console.log("FAILED", C["red"], "Failed to get Random Members", e)

    def spammer(self, token, channel, message=None, guild=None, massping=None, pings=None):
        try:
            while True:
                if massping:
                    msg = self.get_random_members(guild, int(pings))

                    payload = {
                        "content": f"{message} {msg}"
                    }
                    
                else:
                    payload = {
                        "content": message
                    }
                
                response = session.post(
                    f"https://canary.discord.com/api/v9/channels/{channel}/messages",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 200:
                        console.log("Sent", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def join_voice_channel(self, guild_id, channel_id):
        ws = websocket.WebSocket()

        def check_for_guild(token):
            response = session.get(
                f"https://canary.discord.com/api/v9/guilds/{guild_id}", 
                headers=self.headers(token)
            )
            match response.status_code:
                case 200:
                    return True
                case _:
                    console.log("Failed", C["red"], "Missing Access")

        def check_for_channel(token):
            if check_for_guild(token):
                response = session.get(
                    f"https://canary.discord.com/api/v9/channels/{channel_id}", 
                    headers=self.headers(token)
                )

                match response.status_code:
                    case 200:
                        return True
                    case _:
                        return False

        def run(token):
            if check_for_channel(token):
                console.log("Joined", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", channel_id)
                self.voice_spammer(token, ws, guild_id, channel_id, True)
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", channel_id)

        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        args = [
            (token, ) for token in tokens
        ]
        Menu().run(run, args)

    def voice_spammer(self, token, ws, guild_id, channel_id, close=None):
        try:
            self.onliner(token, ws)
            ws.send(
                json.dumps(
                    {
                        "op": 4,
                        "d": {
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "self_mute": False,
                            "self_deaf": False,
                            "self_stream": False,
                            "self_video": True,
                        },
                    }
                )
            )

            ws.send(
                json.dumps(
                    {
                        "op": 18,
                        "d": {
                            "type": "guild",
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "preferred_region": "singapore",
                        },
                    }
                )
            )
            
            ws.send(json.dumps({"op": 1, "d": None}))
            if close:
                ws.close()
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def token_checker(self):
        valid = []
        def main(token):
            try:
                while True:
                    response = session.get(
                        "https://canary.discordapp.com/api/v9/users/@me/library",
                        headers=self.headers(token)
                    )

                    match response.status_code:
                        case 200:
                            console.log("Valid", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                            valid.append(token)
                            break
                        case 403:
                            console.log("LOCKED", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                            break
                        case 429:
                            retry_after = response.json().get("retry_after")
                            console.log("RATELIMITED", C["pink"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"{retry_after}s")
                            time.sleep(retry_after)
                        case _:
                            console.log("Invalid", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                            break
                with open("data/tokens.txt", "w") as f:
                    f.write("\n".join(valid))
            except Exception as e:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        tokens = list(set(tokens))
        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main, args)
        
    def reactor_main(self, channel_id, message_id):
        try:
            access_token = []
            emojis = []
            with open("data/tokens.txt", "r") as f:
                tokens = f.read().splitlines()

            params = {
                "around": message_id, 
                "limit": 50
            }

            for token in tokens:
                response = session.get(
                    f"https://canary.discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    params=params
                )

                match response.status_code:
                    case 200:
                        access_token.append(token)
                        break

            if not access_token:
                console.log("Failed", C["red"], "Missing Permissions")
                input()
                Menu().main_menu()
            else:
                data = response.json()
                for __ in data:
                    if __["id"] == message_id:
                        reactions = __["reactions"]
                        for emois in reactions:
                            if emois:
                                emoji_id = emois["emoji"]["id"]
                                emoji_name = emois["emoji"]["name"]

                                if emoji_id is None:
                                    emojis.append(emoji_name)
                                else:
                                    emojis.append(f"{emoji_name}:{emoji_id}")
                            else:
                                console.log("Failed", C["red"], "No reactions Found in this message",)
                                input()
                                Menu().main_menu()

                for i, emoji in enumerate(emojis, start=1):
                    print(f"{C['light_blue']}0{i}:{C['white']} {emoji}")

                choice = input(f"\n{console.prompt('Choice')}")
                selected = emojis[int(choice) - 1]

            def add_reaction(token):
                try:
                    url = f"https://canary.discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{selected}/@me"

                    if emoji_id is None:
                        url += "?location=Message&type=0"
                    response = session.put(url, headers=self.headers(token))

                    match response.status_code:
                        case 204:
                            console.log("Reacted", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", selected)
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            with open("data/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            args = [
                (token,) for token in tokens
            ]
            Menu().run(add_reaction, args)

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to get emojis", e)
            input()
            Menu().main_menu()

            def add_reaction(token):
                try:
                    url = f"https://canary.discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{selected}/@me"

                    if emoji_id is None:
                        url += "?location=Message&type=0"
                    response = session.put(url, headers=self.headers(token))

                    match response.status_code:
                        case 204:
                            console.log("REACTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", selected)
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            with open("data/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            args = [
                (token) for token in tokens
            ]
            Menu().run(add_reaction, args)

    def soundbord(self, token, channel):
        try:
            sounds = session.get(
                "https://canary.discord.com/api/v9/soundboard-default-sounds",
                headers=self.headers(token)
            ).json()

            time.sleep(1)

            while True:
                sound = random.choice(sounds)
                name = sound.get("name")

                payload = {
                    "emoji_id": None,
                    "emoji_name": sound.get("emoji_name"),
                    "sound_id": sound.get("sound_id"),
                }

                response = session.post(
                    f"https://canary.discord.com/api/v9/channels/{channel}/send-soundboard-sound", 
                    headers=self.headers(token), 
                    json=payload,
                )

                match response.status_code:
                    case 204:
                        console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Played {name}")
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                time.sleep(random.uniform(0.56, 0.75))
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def open_dm(self, token, user_id):
        try:
            payload = {
                "recipients": [user_id]
            }

            response = session.post(
                "https://canary.discord.com/api/v9/users/@me/channels",
                headers=self.headers(token),
                json=payload
            )

            match response.status_code:
                case 200:
                    return response.json()["id"]
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                    return
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def call_spammer(self, token, user_id):
        try:
            while True:
                channel_id = self.open_dm(token, user_id)

                response = session.get(
                    f"https://canary.discord.com/api/v9/channels/{channel_id}/call",
                    headers=self.headers(token)
                )

                match response.status_code:
                    case 200:
                        console.log("Called", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                        ws = websocket.WebSocket()
                        self.voice_spammer(token, ws, None, channel_id, True)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
                time.sleep(5)
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def dm_spammer(self, token, user_id, message, normal=None):
        try:
            payload = {
                "content": message,
                "nonce": self.nonce(),
            }
            while True:
                channel_id = self.open_dm(token, user_id)

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 200:
                        console.log("Send", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))  
                        break
                time.sleep(7)
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def format_tokens(self):
        try:
            formatted = []

            for token in tokens:
                token = token.strip()

                if token:
                    tokens_split = token.split(":")
                    if len(tokens_split) >= 3:
                        formatted_token = tokens_split[2]
                        formatted.append(formatted_token)
                    else:
                        formatted.append(token)

            console.log("SUCCESS", C["green"], f"Formatted {len(formatted)} tokens")

            with open("data/tokens.txt", "w") as f:
                for token in formatted:
                    f.write(f"{token}\n")

            Menu().main_menu()
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def button_bypass(self, token, message_id, channel_id, guild_id):
        try:
            payload = {"limit": "50", "around": message_id}
            response = session.get(
                f"https://canary.discord.com/api/v9/channels/{channel_id}/messages",
                params=payload,
                headers=self.headers(token)
            )

            messages = response.json()
            message_to_click = next((msg for msg in messages if msg["id"] == message_id), None)

            if message_to_click is None:
                console.log("FAILED", C["red"], "Message not found")
                return
            
            buttons = [comp["components"][0] for comp in message_to_click.get("components", [])]
            if not buttons:
                console.log("FAILED", C["red"], "No buttons found in the message")
                return

            for button in buttons:
                data = {
                    "application_id": message_to_click["author"]["id"],
                    "channel_id": channel_id,
                    "data": {
                        "component_type": 2,
                        "custom_id": button["custom_id"],
                    },
                    "guild_id": guild_id,
                    "message_flags": 0,
                    "message_id": message_id,
                    "nonce": self.nonce(),
                    "session_id": uuid.uuid4().hex,
                    "type": 3,
                }

                response = session.post(
                    "https://canary.discord.com/api/v9/interactions",
                    headers=self.headers(token),
                    json=data
                )

                match response.status_code:
                    case 204:
                        console.log(f"Clicked button {button['custom_id']}", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case _:
                        console.log(f"Failed to click button {button['custom_id']}", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", {response.json().get("message")})
        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Click Button", e)

    def accept_rules(self, guild_id):
        try:
            valid = []
            with open("data/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            for token in tokens:
                value = session.get(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/member-verification",
                    headers=self.headers(token)
                )

                match value.status_code:
                    case 200:
                        valid.append(token)
                        payload = value.json()
                        break

            if not valid:
                console.log("FAILED", C["red"], "All tokens are Invalid")
                input()
                Menu().main_menu()

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Accept Rules", e)

        def run_main(token):
            try:
                response = session.put(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/requests/@me",
                    headers=self.headers(token),
                    json=payload
                )
                
                match response.status_code:
                    case 201:
                        console.log("ACCEPTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        args = [
            (token, ) for token in tokens
        ]
        Menu().run(run_main, args)

    def guild_checker(self, guild_id):
        in_guild = []
        def main_checker(token):
            try:
                while True:
                    response = session.get(
                        f"https://canary.discord.com/api/v9/guilds/{guild_id}",
                        headers=self.headers(token)
                    )

                    match response.status_code:
                        case 200:
                            console.log("Found", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                            in_guild.append(token)
                            break
                        case 429:
                            retry_after = response.json().get("retry_after")
                            console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                            time.sleep(float(retry_after))
                        case _:
                            console.log("Not Found", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                            break
                with open("data/tokens.txt", "w") as f:
                    f.write("\n".join(in_guild))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main_checker, args)

    def bio_changer(self, token, bio):
        try:
            payload = {
                "bio": bio
            }

            while True:
                response = session.patch(
                    "https://canary.discord.com/api/v9/users/@me/profile",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 200:
                        console.log("Changed", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", bio)
                        break
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def mass_nick(self, token, guild, nick):
        try:
            payload = {
                "nick" : nick
            }

            while True:
                response = session.patch(
                    f"https://canary.discord.com/api/v9/guilds/{guild}/members/@me", 
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 200:
                        console.log("SUCCESS", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        break
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def thread_spammer(self, token, channel_id, name):
        try:
            payload = {
                "name": name,
                "type": 11,
                "auto_archive_duration": 4320,
                "location": "Thread Browser Toolbar",
            }

            while True:
                response = session.post(
                    f"https://canary.discord.com/api/v9/channels/{channel_id}/threads",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 201:
                        console.log("CREATED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", name)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        if int(retry_after) > 10:
                            console.log("STOPPED", C["magenta"], token[:25], f"Ratelimit Exceeded - {int(round(retry_after))}s",)
                            break
                        else:
                            console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                            time.sleep(float(retry_after))
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def typier(self, token, channelid):
        try:
            while True:
                response = session.post(
                    f"https://canary.discord.com/api/v9/channels/{channelid}/typing", 
                    headers=self.headers(token)
                )

                match response.status_code: 
                    case 204:
                        console.log("SUCCESS", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        time.sleep(9)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def friender(self, token, nickname):
        try:
            headers = self.headers(token)
            payload = {
                "username": nickname,
                "discriminator": None,
            }

            response = session.post(
                f"https://canary.discord.com/api/v9/users/@me/relationships", 
                headers=headers, 
                json=payload
            )

            match response.status_code:
                case 204:
                    console.log(f"SUCCESS", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case 400:
                    console.log("CAPTCHA", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    if solver:
                        headers["x-context-properties"] = "eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ=="
                        headers["x-captcha-rqtoken"] = response.json()["captcha_rqtoken"]

                        if service == "capmonster":
                            headers["x-captcha-key"] = Solver.solve_capmonster()
                        else:
                            headers["x-captcha-key"] = Solver.solve_2cap()

                        newresponse = session.post(
                            f"https://canary.discord.com/api/v9/users/@me/relationships", 
                            headers=headers, 
                            json=payload
                        )
                        match newresponse.status_code:
                            case 204:
                                console.log(f"SUCCESS", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                            case _:
                                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json())
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json())
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def onboard_bypass(self, guild_id):
        try:
            with open("data/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            onboarding_responses_seen = {}
            onboarding_prompts_seen = {}
            onboarding_responses = []
            in_guild = []

            for _token in tokens:
                response = session.get(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/onboarding",
                    headers=self.headers(_token)
                )
                match response.status_code:
                    case 200:
                        in_guild.append(_token)
                        break

            if not in_guild:
                console.log("FAILED", C["red"], "Missing Access")
                input()
                Menu().main_menu()
            else:
                data = response.json()
                now = int(datetime.now().timestamp())

                for __ in data["prompts"]:
                    onboarding_responses.append(__["options"][-1]["id"])

                    onboarding_prompts_seen[__["id"]] = now

                    for prompt in __["options"]:
                        if prompt:
                            onboarding_responses_seen[prompt["id"]] = now
                        else:
                            console.log(
                                "FAILED",
                                C["red"],
                                "No onboarding in This Server",
                            )
                            input()
                            Menu().main_menu()

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Pass Onboard", e)
            input()
            Menu().main_menu()

        def run_task(token):
            try:
                json_data = {
                    "onboarding_responses": onboarding_responses,
                    "onboarding_prompts_seen": onboarding_prompts_seen,
                    "onboarding_responses_seen": onboarding_responses_seen,
                }

                response = session.post(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                    headers=self.headers(token),
                    json=json_data
                )

                match response.status_code:
                    case 200:
                        console.log("ACCEPTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(run_task, args)

        def run_task(token):
            try:
                json_data = {
                    "onboarding_responses": onboarding_responses,
                    "onboarding_prompts_seen": onboarding_prompts_seen,
                    "onboarding_responses_seen": onboarding_responses_seen,
                }

                response = session.post(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                    headers=self.headers(token),
                    json=json_data
                )

                match response.status_code:
                    case 200:
                        console.log("ACCEPTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(run_task, args)

class Menu:
    def __init__(self):
        if not color:
            self.background = C["light_blue"]
        else:
            self.background = C[color]
            
        self.raider = Raider()
        self.options = {
            "1": self.joiner, 
            "2": self.leaver,
            "3": self.spammer, 
            "4": self.checker,
            "5": self.reactor, 
            "7": self.formatter,
            "8": self.button,
            "9": self.accept,
            "10": self.guild,
            "11": self.friender,
            "13": self.onliner,
            "14": self.soundbord,
            "15": self.nick_changer,
            "16": self.Thread_Spammer,
            "17": self.typier,
            "19": self.caller,
            "20": self.bio_changer,
            "21": self.voice_joiner,
            "22": self.onboard,
            "23": self.dm_spam,
            "credits": self.credit,
        }

    def main_menu(self):
        console.run()

        def check(word):
            buffer = ctypes.create_unicode_buffer(1024)
            ctypes.windll.kernel32.GetConsoleTitleW(buffer, len(buffer))
            return word.lower() in buffer.value.lower()
                
        if check(base64.b64decode("Q3dlbGl1bQ==").decode("utf-8")) and check(base64.b64decode("bWFkZSBieSBUaXBzLURpc2NvcmQ=").decode("utf-8")):
            pass
        else:
            print(base64.b64decode("SW1hZ2luZSBza2lkZGluZyBMIEwgTEw=").decode("utf-8"))
            time.sleep(3)
            os._exit(0)
    
        choice = input(f"{' '*4}{Fore.LIGHTCYAN_EX}-> {Fore.RESET}")

        if choice.lower() in self.options:
            console.render_ascii()
            self.options[choice.lower()]()
        else:
            self.main_menu()

    def run(self, func, args):
        threads = []
        clear()
        console.render_ascii()

        # with ThreadPoolExecutor(max_workers=threadamt) as exe:
        #    for arg in args:
        #        try:
        #            future = exe.submit(func, arg)
        #            futures.append(future)
        #        except Exception as e:
        #            console.log("Failed", C["red"], e)

        #    for future in futures:
        #        try:
        #            future.result()
        #        except Exception as e:
        #            console.log("Failed", C["red"], e)

        for arg in args:
            thread = threading.Thread(target=func, args=arg)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        input("\n ~/> press enter to continue ")
        self.main_menu()

    @wrapper
    def credit(self):
        credits_lines = [
            "Special Thanks to",
            "Coder: Tips",
            "Scraper: Aniell4",
            "Original Owner of Helium: Ekkore",
            "Friend: R3ci",
            "And last but not least, you! Without you, this project wouldn't be possible.",
        ]

        for line in credits_lines:
            centered_line = line.center(os.get_terminal_size().columns)
            print(f"{Fore.RESET}{self.background}{centered_line}{Fore.RESET}")

        input("\n ~/> press enter to continue ")
        self.main_menu()

    @wrapper
    def dm_spam(self):
        title(f"Cwelium - Dm Spammer")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            Menu().main_menu()

        message = input(console.prompt("Message"))
        if message == "":
            Menu().main_menu()

        clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.dm_spammer, args=(token, user_id, message)).start()

    @wrapper
    def soundbord(self):
        title(f"Cwelium - Soundboard Spam")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
            
        channel = Link.split("/")[5]
        guild = Link.split("/")[4]

        clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.vc_joiner, args=(token, guild, channel, websocket.WebSocket())).start()
            threading.Thread(target=self.raider.soundbord, args=(token, channel)).start()

    @wrapper
    def friender(self):
        title(f"Cwelium - Friender")
        nickname = input(console.prompt("Nick"))
        if nickname == "":
            Menu().main_menu()

        args = [
            (token, nickname) for token in tokens
        ]
        self.run(self.raider.friender, args)

    @wrapper
    def caller(self):
        title(f"Cwelium - Caller")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            Menu().main_menu()

        clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.call_spammer, args=(token, user_id)).start()

    def onliner(self):
        title(f"Cwelium - Onliner")
        args = [
            (token, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.onliner, args)

    @wrapper
    def typier(self):
        title(f"Cwelium - Typer")
        Link = input(console.prompt(f"Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        channelid = Link.split("/")[5]
        args = [
            (token, channelid) for token in tokens
        ]
        self.run(self.raider.typier, args)

    @wrapper
    def nick_changer(self):
        title(f"Cwelium - Nickname Changer")
        nick = input(console.prompt("Nick"))
        if nick == "":
            Menu().main_menu()

        guild = input(console.prompt("Guild ID"))
        if guild == "":
            Menu().main_menu()

        args = [
            (token, guild, nick) for token in tokens
        ]
        self.run(self.raider.mass_nick, args)

    @wrapper
    def voice_joiner(self):
        title(f"Cwelium - Voice Joiner")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        guild = Link.split("/")[4]
        channel = Link.split("/")[5]
        args = [
            (token, guild, channel, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.vc_joiner, args)

    @wrapper
    def Thread_Spammer(self):
        title(f"Cwelium - Thread Spammer")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        name = input(console.prompt("Name"))
        if name == "":
            Menu().main_menu()

        channel_id = Link.split("/")[5]
        args = [
            (token, channel_id, name) for token in tokens
        ]
        self.run(self.raider.thread_spammer, args)

    @wrapper
    def joiner(self):
        title(f"Cwelium - Joiner")
        invite = input(console.prompt(f"Invite"))
        if invite == "":
            Menu().main_menu()

        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/invite/|discord\.gg/|discord\.com/invite/|\.gg/)", "", invite)

        args = [
            (token, invite) for token in tokens
        ]
        self.run(self.raider.joiner, args)

    @wrapper 
    def leaver(self):
        title(f"Cwelium - Leaver")
        guild = input(console.prompt("Guild ID"))
        if guild == "":
            Menu().main_menu()

        args = [
            (token, guild) for token in tokens
        ]
        self.run(self.raider.leaver, args)

    @wrapper
    def spammer(self):
        title(f"Cwelium - Spammer")
        Link = input(console.prompt(f"Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]

        massping = input(console.prompt("Massping", True))
        message = input(console.prompt("Message"))

        if message == "":
            Menu().main_menu()

        if "y" in massping:
            console.log(f"Scraping users", C["light_blue"], False, "this may take a while...")
            self.raider.member_scrape(guild_id, channel_id)
            count = input(console.prompt("Pings Amount"))

            if count == "":
                Menu().main_menu()

            args = [
                (token, channel_id, message, guild_id, True, count) for token in tokens
            ]
            self.run(self.raider.spammer, args)
        else:
            args = [
                (token, channel_id, message) for token in tokens
            ]
            self.run(self.raider.spammer, args)

    def checker(self):
        title(f"Cwelium - Checker")
        self.raider.token_checker()

    @wrapper
    def reactor(self):
        title(f"Cwelium - Reactor")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]
        clear()
        console.render_ascii()
        self.raider.reactor_main(channel_id, message_id)

    def formatter(self):
        title(f"Cwelium - Formatter")
        self.run(self.raider.format_tokens, [()])
    
    @wrapper
    def button(self):
        title(f"Cwelium - Clicker")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
        
        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]
        args = [
            (token, message_id, channel_id, guild_id) for token in tokens
        ]
        self.run(self.raider.button_bypass, args)

    @wrapper
    def accept(self):
        title(f"Cwelium - Accept Rules")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()

        clear()
        console.render_ascii()
        self.raider.accept_rules(guild_id)

    @wrapper
    def guild(self):
        title(f"Cwelium - Guild Checker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()

        clear()
        console.render_ascii()
        self.raider.guild_checker(guild_id)

    @wrapper
    def bio_changer(self):
        title(f"Cwelium - Bio Changer")
        bio = input(console.prompt("Bio"))
        if bio == "":
            Menu().main_menu()

        args = [
            (token, bio) for token in tokens
        ]
        self.run(self.raider.bio_changer, args)

    @wrapper
    def onboard(self):
        title(f"Cwelium - Onboarding Bypass")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()

        clear()
        console.render_ascii()
        self.raider.onboard_bypass(guild_id)

if __name__ == "__main__":
    Menu().main_menu()
