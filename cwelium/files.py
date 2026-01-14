import os
import json

from .console import Render
from .config import C

console = Render()


class Files:
    @staticmethod
    def ensure_config():
        path = "config.json"
        if not os.path.exists(path):
            default = {"Proxies": False, "Theme": "light_blue"}
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(default, f, indent=4)
            except Exception as e:
                console.log("Failed", C["red"], "Failed to create config.json", str(e))

    @staticmethod
    def ensure_folders():
        for folder in ["data", "scraped"]:
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                console.log("Failed", C["red"], f"Failed to create folder {folder}", str(e))

    @staticmethod
    def ensure_files():
        for fname in ["tokens.txt", "proxies.txt"]:
            path = f"data/{fname}"
            if not os.path.exists(path):
                try:
                    open(path, "a", encoding="utf-8").close()
                except Exception as e:
                    console.log("Failed", C["red"], f"Failed to create {path}", str(e))

    @staticmethod
    def initialize():
        Files.ensure_config()
        Files.ensure_folders()
        Files.ensure_files()

    @staticmethod
    def load_tokens() -> list[str]:
        try:
            with open("data/tokens.txt", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    @staticmethod
    def load_proxies() -> list[str]:
        try:
            with open("data/proxies.txt", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

    @staticmethod
    def save_tokens(tokens: list[str]):
        try:
            with open("data/tokens.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(tokens) + "\n")
        except Exception as e:
            console.log("Failed", C["red"], "Could not save tokens", str(e))