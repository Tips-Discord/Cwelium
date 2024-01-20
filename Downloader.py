import requests

def download_latest_release():
    api_url = f"https://api.github.com/repos/Tips-Discord/Cwelium/releases/latest"
    
    try:
        response = requests.get(api_url)
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
    download_latest_release()