import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urljoin, urlparse

# Import project classes
from botActions.action import Action

CACHE_DIR = "cachedData"


class ArticleImagesDownloadAction(Action):
    """
    Download all tables from a URL and save their text to a file with a Mozilla User-Agent.

    Args:
      url: The URL to download.
      filename: The name of the file to save the tables to.
    """

    def run(self, config, result=""):
        print("\t\033[92m ArticleImagesDownloadAction running ...\033[0m")

        url = config["url"]
        save_folder = os.path.join(CACHE_DIR, config["sheet"])

        os.makedirs(save_folder, exist_ok=True)

        # Get HTML content
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")

        for img in images:
            # Extract image source URL
            src = img.get("src")
            if not src:
                # If no src attribute, skip
                continue
            # Make the URL absolute
            src = urljoin(url, src)
            # Parse the URL, remove query parameters, and extract the path
            parsed_src = urlparse(src)
            clean_path = parsed_src.path
            filename = os.path.basename(clean_path)
            save_path = os.path.join(save_folder, filename)
            # filename = os.path.join(save_folder, src.split("/")[-1])

            if filename.lower().endswith(".png") == False:
                continue

            if os.path.exists(filename):
                print(f"Article Image already downloaded at {filename}")
                return save_folder

            # Download and save the image
            try:
                with requests.get(src, stream=True) as r:
                    r.raise_for_status()
                    with open(save_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded {save_path}")
            except requests.exceptions.HTTPError as err:
                print(f"Failed to download {src}: {err}")

        return save_folder
