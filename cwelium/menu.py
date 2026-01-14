import os
import threading

from colorama import Fore

from .console import Render
from .raider import Raider
from .utils import console_wrapper
from .files import Files
from .config import C

console = Render()


class Menu:
    """Main interactive menu for Cwelium."""

    def __init__(self, raider: Raider, tokens: list[str], proxies: list[str]):
        self.raider = raider
        self.tokens = tokens
        self.proxies = proxies
        self.bg = console.background  # shortcut

        self.options = {
            "1": self.join_server,
            "2": self.leave_server,
            "3": self.spam_channel,
            "4": self.check_tokens,
            "5": self.add_reactions,
            "7": self.format_tokens,
            "8": self.click_button,
            "9": self.accept_rules,
            "10": self.guild_checker,
            "11": self.friender,
            "13": self.onliner,
            "14": self.soundboard_spam,
            "15": self.mass_nick,
            "16": self.thread_spammer,
            "17": self.typer,
            "19": self.call_spammer,
            "20": self.change_bio,
            "21": self.voice_joiner,
            "22": self.onboard_bypass,
            "23": self.dm_spammer,
            "24": self.exit_program,
            "~": self.show_credits,
        }

    def run(self):
        while True:
            console.show_main_screen(len(self.tokens), len(self.proxies))
            choice = input(f"      {self.bg}-> ").strip().lower()

            if choice.startswith("0") and len(choice) == 2:
                choice = choice.lstrip("0")

            action = self.options.get(choice)
            if action:
                action()
            else:
                console.log("Invalid", self.bg, False, "Please enter a valid option")

    # ──────────────────────────────────────────────
    #               Menu Actions
    # ──────────────────────────────────────────────

    @console_wrapper
    def join_server(self):
        invite = input(console.prompt("Invite code or full link")).strip()
        if invite:
            self.raider.join_server(invite, self.tokens)
        input("\nPress Enter to return...")

    @console_wrapper
    def leave_server(self):
        guild_id = input(console.prompt("Guild ID")).strip()
        if guild_id:
            self.raider.leave_server(guild_id, self.tokens)
        input("\nPress Enter...")

    @console_wrapper
    def spam_channel(self):
        link = input(console.prompt("Channel link[](https://discord.com/channels/...)")).strip()
        if not link.startswith("https://discord.com/channels/"):
            console.log("Invalid", C["red"], False, "Not a valid Discord channel link")
            return

        parts = link.split("/")
        guild_id = parts[-2]
        channel_id = parts[-1]

        message = input(console.prompt("Message content")).strip()
        if not message:
            return

        massping_yn = input(console.prompt("Mass ping users? (y/n)", ask=True)).lower()
        random_str_yn = input(console.prompt("Add random string? (y/n)", ask=True)).lower()
        delay_str = input(console.prompt("Delay between messages (seconds, default 1.5)")).strip()

        delay = 1.5
        if delay_str.replace(".", "").isdigit():
            delay = float(delay_str)

        ping_count = 0
        if massping_yn.startswith("y"):
            ping_str = input(console.prompt("Number of pings per message")).strip()
            if ping_str.isdigit():
                ping_count = int(ping_str)

        self.raider.spam_channel(
            channel_id=channel_id,
            message=message,
            guild_id=guild_id,
            massping=massping_yn.startswith("y"),
            ping_count=ping_count,
            random_tail=random_str_yn.startswith("y"),
            delay=delay,
            tokens=self.tokens
        )

    @console_wrapper
    def check_tokens(self):
        console.log("Starting", C["yellow"], False, "Token validity check...")
        valid_tokens = []

        def check_one(token: str):
            try:
                r = self.raider.session.get(
                    "https://discord.com/api/v9/users/@me/library",
                    headers=self.raider.headers(token)
                )
                if r.status_code == 200:
                    console.log("Valid", C["green"], f"{token[:25]}...")
                    valid_tokens.append(token)
                elif r.status_code == 403:
                    console.log("Locked", C["yellow"], f"{token[:25]}...")
                elif r.status_code == 429:
                    console.log("Ratelimit", C["magenta"], f"{token[:25]}...")
                else:
                    console.log("Invalid", C["red"], f"{token[:25]}...")
            except:
                console.log("Error", C["red"], f"{token[:25]}...")

        threads = []
        for tk in self.tokens:
            t = threading.Thread(target=check_one, args=(tk,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if valid_tokens:
            Files.save_tokens(valid_tokens)
            console.log("Success", C["green"], False, f"Saved {len(valid_tokens)} valid tokens")
        else:
            console.log("Warning", C["yellow"], False, "No valid tokens found")

        input("\nPress Enter...")

    @console_wrapper
    def format_tokens(self):
        self.raider.format_tokens(self.tokens)
        # Reload after formatting
        self.tokens = Files.load_tokens()
        input("\nPress Enter...")

    @console_wrapper
    def change_bio(self):
        bio = input(console.prompt("New bio text")).strip()
        if bio:
            self.raider.change_bio(bio, self.tokens)
        input("\nPress Enter...")

    @console_wrapper
    def dm_spammer(self):
        user_id = input(console.prompt("Target User ID")).strip()
        if not user_id.isdigit():
            console.log("Invalid", C["red"], False, "User ID must be numeric")
            return

        message = input(console.prompt("Message to spam")).strip()
        if not message:
            return

        def spam_dm(tk: str):
            self.raider.dm_spammer(tk, user_id, message)

        self.raider._run_threads(spam_dm, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def call_spammer(self):
        user_id = input(console.prompt("Target User ID")).strip()
        if not user_id.isdigit():
            return

        def call_one(tk: str):
            self.raider.call_spammer(tk, user_id)

        self.raider._run_threads(call_one, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def onliner(self):
        def online_one(tk: str):
            self.raider.onliner(tk)

        self.raider._run_threads(online_one, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def voice_joiner(self):
        link = input(console.prompt("Voice channel link")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        parts = link.split("/")
        guild_id = parts[-2]
        channel_id = parts[-1]

        def join_vc(tk: str):
            self.raider.join_voice_channel(tk, guild_id, channel_id)

        self.raider._run_threads(join_vc, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def thread_spammer(self):
        link = input(console.prompt("Channel link")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        channel_id = link.split("/")[-1]

        name = input(console.prompt("Thread name")).strip()
        if not name:
            return

        def create_thread(tk: str):
            self.raider.thread_spammer(tk, channel_id, name)

        self.raider._run_threads(create_thread, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def typer(self):
        link = input(console.prompt("Channel link")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        channel_id = link.split("/")[-1]

        def type_one(tk: str):
            self.raider.typier(tk, channel_id)

        self.raider._run_threads(type_one, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def mass_nick(self):
        nick = input(console.prompt("New nickname")).strip()
        guild_id = input(console.prompt("Guild ID")).strip()

        if nick and guild_id:
            def change_nick(tk: str):
                self.raider.mass_nick(tk, guild_id, nick)

            self.raider._run_threads(change_nick, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def soundboard_spam(self):
        link = input(console.prompt("Voice channel link")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        guild_id = link.split("/")[-2]
        channel_id = link.split("/")[-1]

        for tk in self.tokens:
            threading.Thread(target=self.raider.join_voice_channel, args=(tk, guild_id, channel_id), daemon=True).start()
            threading.Thread(target=self.raider.soundbord, args=(tk, channel_id), daemon=True).start()

        input("\nSoundboard spam started in background. Press Enter to return...")

    @console_wrapper
    def friender(self):
        username = input(console.prompt("Username to friend (username#discriminator or just username)")).strip()
        if username:
            def friend_one(tk: str):
                self.raider.friender(tk, username)

            self.raider._run_threads(friend_one, [(t,) for t in self.tokens])
        input("\nPress Enter...")

    @console_wrapper
    def guild_checker(self):
        guild_id = input(console.prompt("Guild ID to check")).strip()
        if guild_id:
            self.raider.guild_checker(guild_id)
        input("\nPress Enter...")

    @console_wrapper
    def accept_rules(self):
        guild_id = input(console.prompt("Guild ID (rules screening)")).strip()
        if guild_id:
            self.raider.accept_rules(guild_id)
        input("\nPress Enter...")

    @console_wrapper
    def onboard_bypass(self):
        guild_id = input(console.prompt("Guild ID (onboarding)")).strip()
        if guild_id:
            self.raider.onboard_bypass(guild_id)
        input("\nPress Enter...")

    @console_wrapper
    def add_reactions(self):
        link = input(console.prompt("Message link")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        parts = link.split("/")
        channel_id = parts[-2]
        message_id = parts[-1]

        self.raider.reactor_main(channel_id, message_id)
        input("\nPress Enter...")

    @console_wrapper
    def click_button(self):
        link = input(console.prompt("Message link with button")).strip()
        if not link.startswith("https://discord.com/channels/"):
            return
        parts = link.split("/")
        guild_id = parts[-3]
        channel_id = parts[-2]
        message_id = parts[-1]

        self.raider.button_bypass(channel_id, message_id, guild_id)
        input("\nPress Enter...")

    @console_wrapper
    def show_credits(self):
        credits_text = [
            "Cwelium – Refactored Edition",
            "",
            "Special thanks to:",
            "• Tips-Discord (original author)",
            "• Aniell4 (scraper logic)",
            "• Ekkore (Helium / early Cwelium)",
            "",
            "Use responsibly.",
        ]
        for line in credits_text:
            print(line.center(os.get_terminal_size().columns))
        input("\nPress Enter to return...")

    def exit_program(self):
        console.clear()
        print(f"{self.bg}Goodbye. Stay safe.{C['white']}")
        os._exit(0)