import requests
import colorama 
import os

os.system(f"title Cwelium Downloader")

stars = requests.get(f"https://api.github.com/repos/Tips-Discord/Cwelium").json()["stargazers_count"]

menu = f"""
{'██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ '.center(os.get_terminal_size().columns)}
{'██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗'.center(os.get_terminal_size().columns)}
{'██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝'.center(os.get_terminal_size().columns)}
{'██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗'.center(os.get_terminal_size().columns)}
{'██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║'.center(os.get_terminal_size().columns)}
{'╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝'.center(os.get_terminal_size().columns)}
{f'Stars {stars}'.center(os.get_terminal_size().columns)}"""

def download_latest_release():
    try:
        response = requests.get("https://api.github.com/repos/Tips-Discord/Cwelium/releases/latest")
        response.raise_for_status()
        release_info = response.json()
        asset_url = release_info['assets'][0]['browser_download_url']

        response = requests.get(asset_url)
        response.raise_for_status()

        with open(f"Cwelium.exe", "wb") as file:
            file.write(response.content)
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(menu)
    download_latest_release()
    os.system("start Cwelium.exe")
