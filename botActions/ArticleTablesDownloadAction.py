# Import system libraries
import os
import json

# Import 3d Party Libraries
import requests
from bs4 import BeautifulSoup

# Import project classes
from botActions.action import Action

CACHE_DIR = "cachedData"


class ArticleTablesDownloadAction(Action):
    """
    Download all tables from a URL and save their text to a file with a Mozilla User-Agent.

    Args:
      url: The URL to download.
      filename: The name of the file to save the tables to.
    """

    def run(self, config, result=""):
        print("\t\033[92m ArticleTablesDownloadAction running ...\033[0m")

        url = config["url"]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        tableTexts = []
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        cached_dir_path = os.path.join(CACHE_DIR, config["sheet"])
        i = 0
        for table in soup.find_all("table"):

            cached_file_path = os.path.join(
                CACHE_DIR, config["sheet"], str(i) + "ArticleTable" + ".json"
            )

            # Create 'cachedData' directory if it doesn't exist
            os.makedirs(os.path.join(CACHE_DIR, config["sheet"]), exist_ok=True)

            # # Check if the video is already cached
            if os.path.exists(cached_file_path):
                print(f"Article Text already cached at {cached_file_path}")
                return cached_file_path

            # Remove unnecessary tags and whitespace
            for tag in table.find_all(["script", "style"]):
                tag.decompose()
            for br in table.find_all("<br>"):
                br.replace_with("\n")

            # Extract and format table text
            text = table.get_text(separator="\n", strip=True)
            # tableTexts.append(text)

            tokens = text.split("\n")

            # Serialize and save the OCR results to a JSON file
            with open(cached_file_path, "w", encoding="utf-8") as file:
                json.dump(tokens, file)

            i = i + 1
        return cached_dir_path
