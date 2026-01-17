import os
import ctypes
from datetime import datetime
import threading

from colorama import Fore, init
init(autoreset=True)

from .config import C, THEME_COLOR


class Render:
    """Console UI, logging, ASCII art and prompts."""

    def __init__(self):
        self.size = os.get_terminal_size().columns
        self.print_lock = threading.Lock()
        self.background = C.get(THEME_COLOR, C["light_blue"])

    def title(self, title_text):
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title_text)
        except:
            pass  # not Windows → ignore

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def render_ascii(self):
        self.clear()
        self.title(f"Cwelium | Connected as {os.getlogin()} | made by Tips-Discord")

        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        art = f"""
{' ██████╗██╗    ██╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗'.center(self.size)}
{'██╔════╝██║    ██║██╔════╝██║     ██║██║   ██║████╗ ████║'.center(self.size)}
{'██║     ██║ █╗ ██║█████╗  ██║     ██║██║   ██║██╔████╔██║'.center(self.size)}
{'██║     ██║███╗██║██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║'.center(self.size)}
{'╚██████╗╚███╔███╔╝███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║'.center(self.size)}
{' ╚═════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝'.center(self.size)}
{''.center(self.size)}
"""

        for line in art.splitlines():
            for edge in edges:
                line = line.replace(edge, f"{self.background}{edge}{C['white']}")
            print(line)

    def raider_options(self, token_count: int, proxy_count: int):
        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        content = f"""{Fore.RESET}{' ' * max(0, (self.size - len(f'Loaded ‹{token_count}› tokens | Loaded ‹{proxy_count}› proxies')) // 2)}Loaded ‹{self.background}{token_count}{Fore.RESET}› tokens | Loaded ‹{self.background}{proxy_count}{Fore.RESET}› proxies

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
            content = content.replace(edge, f"{self.background}{edge}{C['white']}")
        print(content)

    def log(self, text=None, color=None, token=None, log=None):
        ts = datetime.now().strftime(f"{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}")
        line = f"[{ts}] "
        if text:
            line += f"[{color}{text}{C['white']}] "
        if token:
            line += token
        if log:
            line += f" ({C['gray']}{log}{C['white']})"
        with self.print_lock:
            print(line)

    def prompt(self, text: str, ask: bool = False) -> str:
        p = f"[{C[THEME_COLOR]}{text}{C['white']}]"
        if ask:
            p += f" {C['gray']}(y/n){C['white']}: "
        else:
            p += ": "
        return p

    def show_main_screen(self, token_count: int, proxy_count: int):
        self.render_ascii()
        self.raider_options(token_count, proxy_count)