import json
import time
import threading

from websocket import WebSocketApp

from .console import Render
from .config import C
from .utils import MemberListUtils

console = Render()


class MemberScraper(WebSocketApp):
    """WebSocket client for scraping Discord guild members via member list updates."""

    BLACKLIST = {
        "1100342265303547924",
        "1190052987477958806",
        "833007032000446505",
        "1273658880039190581",
        "1308012310396407828",
        "1326906424873193586",
        "1334512667456442411",
        "1349869929809186846"
    }

    def __init__(self, token: str, guild_id: str, channel_id: str):
        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header={
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            },
            on_open=self._on_open,
            on_message=self._on_message,
            on_close=self._on_close,
        )

        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id

        self.end_scraping = False
        self.guilds = {}
        self.members = {}
        self.ranges = [[0, 0]]
        self.last_range_idx = 0
        self.packets = 0

    def _on_open(self, ws):
        ws.send(json.dumps({
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

    def _heartbeat(self, interval: float):
        while not self.end_scraping:
            self.send(json.dumps({"op": 1, "d": self.packets}))
            time.sleep(interval)

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
        except Exception:
            return

        if data.get("op") != 11:
            self.packets += 1

        if data.get("op") == 10:
            interval = data["d"]["heartbeat_interval"] / 1000.0
            threading.Thread(
                target=self._heartbeat,
                args=(interval,),
                daemon=True
            ).start()

        if data.get("t") == "READY":
            for guild in data["d"].get("guilds", []):
                self.guilds[guild["id"]] = {"member_count": guild.get("member_count", 0)}

            total = self.guilds.get(self.guild_id, {}).get("member_count", 0)
            if total > 0:
                console.log("Info", C["yellow"], False,
                            f"Guild has {total} members → ETA ~{round(total / 150, 1)}s")

        if data.get("t") == "READY_SUPPLEMENTAL":
            self.ranges = MemberListUtils.get_ranges(
                0, 100, self.guilds.get(self.guild_id, {}).get("member_count", 0)
            )
            self._request_members()

        if data.get("t") == "GUILD_MEMBER_LIST_UPDATE":
            parsed = MemberListUtils.parse_member_list_update(data)
            if parsed["guild_id"] == self.guild_id:
                self._process_update(parsed)

    def _request_members(self):
        if self.end_scraping:
            return

        payload = {
            "op": 14,
            "d": {
                "guild_id": self.guild_id,
                "typing": True,
                "activities": True,
                "threads": True,
                "channels": {self.channel_id: self.ranges}
            }
        }
        self.send(json.dumps(payload))

    def _process_update(self, parsed):
        if "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]:
            for i, typ in enumerate(parsed["types"]):
                if typ in ("SYNC", "UPDATE"):
                    if not parsed["updates"][i]:
                        self.end_scraping = True
                        break
                    self._process_members(parsed["updates"][i])

                self.last_range_idx += 1
                self.ranges = MemberListUtils.get_ranges(
                    self.last_range_idx,
                    100,
                    self.guilds.get(self.guild_id, {}).get("member_count", 0)
                )
                self._request_members()

        if self.end_scraping:
            self.close()

    def _process_members(self, items):
        for item in items:
            member = item.get("member")
            if not member:
                continue

            user = member.get("user", {})
            uid = user.get("id")
            if uid and uid not in self.BLACKLIST and not user.get("bot", False):
                self.members[uid] = {
                    "tag": f"{user.get('username')}#{user.get('discriminator')}",
                    "id": uid
                }

    def _on_close(self, ws, code, msg):
        console.log("Success", C["green"], False,
                    f"Scraped {len(self.members)} members")


def scrape_members(token: str, guild_id: str, channel_id: str) -> dict:
    """Run member scraping via WebSocket gateway."""
    scraper = MemberScraper(token, guild_id, channel_id)
    scraper.run_forever(ping_interval=30, ping_timeout=10)
    return scraper.members