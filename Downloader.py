import os
try:
    import requests
except ImportError:
    os.system("pip install requests")

os.system(f"title Cwelium Downloader")

def download_latest_release():
    try:
        response = requests.get("https://api.github.com/repos/Tips-Discord/Cwelium/releases/latest")
        response.raise_for_status()

        response = requests.get(response.json()['assets'][0]['browser_download_url'])
        response.raise_for_status()

        with open(f"Cwelium.exe", "wb") as file:
            file.write(response.content) 
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print(f"""
{'██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ '.center(os.get_terminal_size().columns)}
{'██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗'.center(os.get_terminal_size().columns)}
{'██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝'.center(os.get_terminal_size().columns)}
{'██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗'.center(os.get_terminal_size().columns)}
{'██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║'.center(os.get_terminal_size().columns)}
{'╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝'.center(os.get_terminal_size().columns)}
{f'Stars {requests.get(f"https://api.github.com/repos/Tips-Discord/Cwelium").json()["stargazers_count"]}'.center(os.get_terminal_size().columns)}""")
    download_latest_release()
    os.system("start Cwelium.exe")
