# raider.py
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
    """Core Discord API interaction class – all raiding actions live here."""

    def __init__(self, session):
        self.session = session
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
                return f"{cookies}; {self.cf_token}; locale=en-US", r.json().get("fingerprint", "")
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
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": self.fingerprint,
            "x-super-properties": self.super_properties(),
        }

    def nonce(self) -> int:
        return (int(time.time() * 1000) - 1420070400000) << 22

    def _run_threads(self, target, args_list: list[tuple]):
        threads = []
        for idx, args in enumerate(args_list):
            if PROXY_ENABLED and hasattr(self.session, "proxies_list") and self.session.proxies_list:
                proxy = self.session.proxies_list[idx % len(self.session.proxies_list)]
                self.session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            else:
                self.session.proxies = {}

            t = threading.Thread(target=target, args=args, daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # ──────────────────────────────────────────────
    #               All migrated & fixed actions
    # ──────────────────────────────────────────────

    def join_server(self, invite: str, tokens: list[str]):
        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/(invite/)?|\.gg/)", "", invite.strip())

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
                time.sleep(random.uniform(2, 6))
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
                    retry = r.json().get("retry_after", 5) + random.uniform(0.5, 2)
                    console.log("Ratelimit", C["magenta"], f"{tk[:25]}...", f"wait {retry:.1f}s")
                    time.sleep(retry)
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
        if not tokens:
            tokens = Files.load_tokens()

        if massping and guild_id:
            self.member_scrape(guild_id, channel_id, tokens)

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
                        json={"content": content, "nonce": str(self.nonce()), "tts": False}
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
                    time.sleep(delay + random.uniform(0, 2))
                except Exception as e:
                    console.log("Error", C["red"], f"{tk[:25]}...", str(e))
                    time.sleep(6)

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

    def member_scrape(self, guild_id: str, channel_id: str, tokens: list):
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

    def format_tokens(self, tokens: list):
        cleaned = []
        for line in tokens:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            cleaned.append(parts[-1] if len(parts) >= 3 else line)

        console.log("Success", C["green"], False, f"Formatted {len(cleaned)} tokens")

        try:
            with open("data/tokens.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned) + "\n")
        except Exception as e:
            console.log("Failed", C["red"], "Could not save formatted tokens", str(e))

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

    def dm_spammer(self, token: str, user_id: str, message: str):
        """Fixed DM spammer – creates DM channel first, then sends message"""
        try:
            # Step 1: Create / get DM channel
            dm_payload = {"recipients": [user_id]}
            channel_resp = self.session.post(
                "https://discord.com/api/v9/users/@me/channels",
                headers=self.headers(token),
                json=dm_payload
            )

            if channel_resp.status_code not in (200, 201):
                console.log("Failed to create/get DM channel", C["red"], f"{token[:25]}...", channel_resp.text)
                return

            channel_id = channel_resp.json()["id"]

            # Step 2: Send message
            msg_payload = {
                "content": message,
                "nonce": str(self.nonce()),
                "tts": False,
                "flags": 0
            }
            send_resp = self.session.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=self.headers(token),
                json=msg_payload
            )

            if send_resp.status_code in (200, 204):
                console.log("Sent DM", C["green"], f"{token[:25]} → {user_id}")
            else:
                console.log("Failed DM send", C["red"], f"{token[:25]}...", send_resp.text)

            # Delay for multi-message spam
            time.sleep(random.uniform(4, 10))

        except Exception as e:
            console.log("DM error", C["red"], f"{token[:25]}...", str(e))

    def call_spammer(self, token: str, user_id: str):
        """Fixed call spammer – creates group DM and rings the target"""
        try:
            # Step 1: Create group DM with the target
            group_payload = {"recipients": [user_id]}
            group_resp = self.session.post(
                "https://discord.com/api/v9/users/@me/channels",
                headers=self.headers(token),
                json=group_payload
            )

            if group_resp.status_code not in (200, 201):
                console.log("Failed to create group DM", C["red"], f"{token[:25]}...", group_resp.text)
                return

            channel_id = group_resp.json()["id"]

            # Step 2: Ring / start call
            ring_payload = {
                "recipients": [user_id],
                "ringing": [user_id]
            }
            ring_resp = self.session.post(
                f"https://discord.com/api/v9/channels/{channel_id}/call",
                headers=self.headers(token),
                json=ring_payload
            )

            if ring_resp.status_code in (200, 204):
                console.log("Call started (ringing)", C["green"], f"{token[:25]} → {user_id}")
            else:
                console.log("Call ring failed", C["red"], f"{token[:25]}...", ring_resp.text)

        except Exception as e:
            console.log("Call error", C["red"], f"{token[:25]}...", str(e))

    def onliner(self, token: str):
        try:
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "os": "Windows",
                        "browser": "Chrome",
                        "device": "",
                        "system_locale": "en-US",
                        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                        "browser_version": "139.0.0.0",
                        "os_version": "10",
                        "client_build_number": int(self.build_number)
                    },
                    "presence": {"status": "online", "afk": False}
                }
            }))
            console.log("Online", C["green"], f"{token[:25]}...")
        except Exception as e:
            console.log("Online fail", C["red"], f"{token[:25]}...", str(e))

    def join_voice_channel(self, token: str, guild_id: str, channel_id: str):
        try:
            payload = {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "self_mute": False,
                "self_deaf": False,
                "self_stream": False,
                "self_video": False
            }
            resp = self.session.patch(
                f"https://discord.com/api/v9/users/@me/guilds/{guild_id}/voice-state",
                headers=self.headers(token),
                json=payload
            )
            if resp.status_code in (200, 204):
                console.log("Joined VC", C["green"], f"{token[:25]} → {channel_id}")
            else:
                console.log("VC join failed", C["red"], f"{token[:25]}...", resp.text)
        except Exception as e:
            console.log("VC error", C["red"], f"{token[:25]}...", str(e))

    def soundbord(self, token: str, channel_id: str):
        try:
            while True:
                sound_id = random.randint(1, 20)  # placeholder
                payload = {"sound_id": str(sound_id)}
                resp = self.session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/soundboard",
                    headers=self.headers(token),
                    json=payload
                )
                if resp.status_code == 204:
                    console.log("Sound played", C["green"], f"{token[:25]}...")
                time.sleep(random.uniform(2, 6))
        except Exception as e:
            console.log("Soundboard error", C["red"], f"{token[:25]}...", str(e))

    def mass_nick(self, token: str, guild_id: str, nick: str):
        try:
            resp = self.session.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/members/@me/nick",
                headers=self.headers(token),
                json={"nick": nick}
            )
            if resp.status_code in (200, 204):
                console.log("Nick changed", C["green"], f"{token[:25]} → {nick}")
            else:
                console.log("Nick change failed", C["red"], f"{token[:25]}...", resp.text)
        except Exception as e:
            console.log("Nick error", C["red"], f"{token[:25]}...", str(e))

    def thread_spammer(self, token: str, channel_id: str, name: str):
        try:
            payload = {"name": name, "type": 11, "auto_archive_duration": 1440}
            resp = self.session.post(
                f"https://discord.com/api/v9/channels/{channel_id}/threads",
                headers=self.headers(token),
                json=payload
            )
            if resp.status_code == 201:
                console.log("Thread created", C["green"], f"{token[:25]} → {name}")
            else:
                console.log("Thread failed", C["red"], f"{token[:25]}...", resp.text)
        except Exception as e:
            console.log("Thread error", C["red"], f"{token[:25]}...", str(e))

    def typier(self, token: str, channel_id: str):
        while True:
            try:
                resp = self.session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/typing",
                    headers=self.headers(token)
                )
                if resp.status_code == 204:
                    console.log("Typing", C["green"], f"{token[:25]}...")
                time.sleep(8 + random.uniform(0, 2))
            except Exception as e:
                console.log("Typing error", C["red"], f"{token[:25]}...", str(e))
                break

    def friender(self, token: str, username: str):
        try:
            payload = {"username": username}
            resp = self.session.post(
                "https://discord.com/api/v9/users/@me/relationships",
                headers=self.headers(token),
                json=payload
            )
            if resp.status_code == 204:
                console.log("Friend request sent", C["green"], f"{token[:25]} → {username}")
            else:
                console.log("Friend failed", C["red"], f"{token[:25]}...", resp.text)
        except Exception as e:
            console.log("Friend error", C["red"], f"{token[:25]}...", str(e))

    def guild_checker(self, guild_id: str):
        def _check(tk: str):
            try:
                r = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}", headers=self.headers(tk))
                if r.status_code == 200:
                    console.log("Found", C["green"], f"{tk[:25]}... → {guild_id}")
                else:
                    console.log("Not found", C["red"], f"{tk[:25]}... → {guild_id}")
            except Exception as e:
                console.log("Check error", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_check, [(t,) for t in Files.load_tokens()])

    def accept_rules(self, guild_id: str):
        valid = []
        for token in Files.load_tokens():
            r = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification", headers=self.headers(token))
            if r.status_code == 200:
                valid.append(token)
                payload = r.json()
                break

        if not valid:
            console.log("Failed", C["red"], "No token can access rules screening")
            return

        def _accept(tk: str):
            try:
                r = self.session.put(
                    f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me",
                    headers=self.headers(tk),
                    json=payload
                )
                if r.status_code == 201:
                    console.log("Rules accepted", C["green"], f"{tk[:25]}...")
                else:
                    console.log("Accept failed", C["red"], f"{tk[:25]}...", r.text)
            except Exception as e:
                console.log("Accept error", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_accept, [(t,) for t in Files.load_tokens()])

    def onboard_bypass(self, guild_id: str):
        responses = []
        prompts_seen = {}
        responses_seen = {}

        r = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/onboarding", headers=self.headers(Files.load_tokens()[0]))
        if r.status_code != 200:
            console.log("Failed", C["red"], "Cannot access onboarding")
            return

        data = r.json()
        now = int(time.time())

        for prompt in data.get("prompts", []):
            if prompt.get("options"):
                responses.append(prompt["options"][-1]["id"])
                prompts_seen[prompt["id"]] = now
                for opt in prompt["options"]:
                    responses_seen[opt["id"]] = now

        def _bypass(tk: str):
            try:
                payload = {
                    "onboarding_responses": responses,
                    "onboarding_prompts_seen": prompts_seen,
                    "onboarding_responses_seen": responses_seen,
                }
                r = self.session.post(
                    f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                    headers=self.headers(tk),
                    json=payload
                )
                if r.status_code == 200:
                    console.log("Onboarding bypassed", C["green"], f"{tk[:25]}...")
                else:
                    console.log("Bypass failed", C["red"], f"{tk[:25]}...", r.text)
            except Exception as e:
                console.log("Bypass error", C["red"], f"{tk[:25]}...", str(e))

        self._run_threads(_bypass, [(t,) for t in Files.load_tokens()])

    def reactor_main(self, channel_id: str, message_id: str):
        try:
            r = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50", headers=self.headers(Files.load_tokens()[0]))
            if r.status_code != 200:
                console.log("Failed", C["red"], "Cannot fetch message")
                return

            msg = next((m for m in r.json() if m["id"] == message_id), None)
            if not msg or not msg.get("reactions"):
                console.log("Failed", C["red"], "No reactions found")
                return

            emoji = msg["reactions"][0]["emoji"]
            emoji_str = emoji["name"] if not emoji.get("id") else f"{emoji['name']}:{emoji['id']}"

            def _react(tk: str):
                url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji_str}/@me"
                r = self.session.put(url, headers=self.headers(tk))
                if r.status_code == 204:
                    console.log("Reacted", C["green"], f"{tk[:25]} → {emoji_str}")
                else:
                    console.log("React failed", C["red"], f"{tk[:25]}...", r.text)

            self._run_threads(_react, [(t,) for t in Files.load_tokens()])
        except Exception as e:
            console.log("React error", C["red"], str(e))

    def button_bypass(self, channel_id: str, message_id: str, guild_id: str):
        try:
            r = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50", headers=self.headers(Files.load_tokens()[0]))
            if r.status_code != 200:
                console.log("Failed", C["red"], "Cannot fetch message")
                return

            msg = next((m for m in r.json() if m["id"] == message_id), None)
            if not msg or not msg.get("components"):
                console.log("Failed", C["red"], "No buttons found")
                return

            for row in msg["components"]:
                for comp in row.get("components", []):
                    if comp.get("type") == 2 and comp.get("custom_id"):
                        custom_id = comp["custom_id"]
                        app_id = msg["author"]["id"]

                        def _click(tk: str):
                            payload = {
                                "type": 3,
                                "guild_id": guild_id,
                                "channel_id": channel_id,
                                "message_id": message_id,
                                "application_id": app_id,
                                "data": {"component_type": 2, "custom_id": custom_id},
                                "session_id": uuid.uuid4().hex,
                                "nonce": str(self.nonce())
                            }
                            r = self.session.post("https://discord.com/api/v9/interactions", headers=self.headers(tk), json=payload)
                            if r.status_code in (200, 204):
                                console.log("Button clicked", C["green"], f"{tk[:25]}...")
                            else:
                                console.log("Button failed", C["red"], f"{tk[:25]}...", r.text)

                        self._run_threads(_click, [(t,) for t in Files.load_tokens()])
                        return
        except Exception as e:
            console.log("Button error", C["red"], str(e))
