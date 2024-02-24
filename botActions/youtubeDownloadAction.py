# Import System libraries
import os

# Import 3rd party libraries
from pytube import YouTube
import cv2

# Import project classes
from botActions.action import Action

CACHE_DIR = "cachedData"


class YoutubeDownloadAction(Action):
    """
    An Benchmarkbot Action class downloads and caches a Youtube
    """

    def __init__(self):
        self.url = None
        self.yt = None

    def cachedFilePath(self):
        # Create 'cachedData' directory if it doesn't exist
        os.makedirs(CACHE_DIR, exist_ok=True)

        # Don't make a call to Youtube if you don't need to
        if self.yt is None:
            self.yt = YouTube(self.url)

        title = self.yt.title.replace(" :", "-")
        author = self.yt.author.replace(" :", "-")
        cached_file_path = os.path.normpath(
            self.resultFile(author + "-" + title, "video.mp4")
        )

        return cached_file_path

    def run(self, config, arg):
        """
        An Benchmarkbot Action class that downloads a YouTube video to a local cache directory
        and returns the path to the downloaded file.

        This function checks if the requested video is already cached in a specified directory (`cache_dir`).
        If the video is not already cached, it downloads the video from the provided YouTube URL,
        saving it to a file named `<author>-<title>.mp4` within the cache directory. If the video is
        already present in the cache, it skips the download and returns the path to the cached file.

        Parameters:
        - url (str): The URL of the YouTube video to download.

        Returns:
        - str: The file path to the downloaded or cached YouTube video.

        Side Effects:
        - Creates a `cache_dir` directory if it doesn't already exist.
        - Downloads a video file to the local filesystem if the video is not already cached.
        - Prints a message indicating whether the video is being downloaded or if it was already cached.

        Note:
        - This function assumes that `self.cache_dir` is a predefined attribute of the class to which this
            function belongs, specifying the path to the cache directory.
        """
        print(
            "\033[94m" + config["sheet"] + " - " + str(config["timeindex"]) + "\033[0m"
        )
        print("\t\033[92mYoutubeDownloadAction running ...\033[0m")
        self.url = config["url"]

        # I'm calling the Youtube API and getting the title and author of the video
        # because I want to make it easy for the hiring team to understand the work
        # that BenchmarkBot is performing.
        # If I were making this a production application I would simply hash the
        # Youtube URL and use that as the directory name instead of fetching the
        # title and author
        yt = YouTube(self.url)

        # Yes, I could have used a regex /[\s-:\.\!]/
        title = (
            yt.title.replace(" ", "-")
            .replace(":", "-")
            .replace(".", "")
            .replace("&", "")
            .replace("!", "")
            .replace("’", "")
        )
        author = (
            yt.author.replace(" ", "-")
            .replace(":", "-")
            .replace(".", "")
            .replace("&", "-")
            .replace("!", "")
            .replace("’", "")
        )

        cached_file_path = os.path.normpath(
            self.resultFile(author + "-" + title, "video.mp4")
        )
        cached_dirname_path = os.path.dirname(cached_file_path)

        # Create 'cachedData' directory if it doesn't exist
        os.makedirs(cached_dirname_path, exist_ok=True)

        # Check if the video is already cached
        if os.path.exists(cached_file_path):
            print(f"\t Video already cached at {cached_file_path}")
            return cached_file_path

        # The core of the run function
        print("\t Downloading video...")
        stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        stream.download(filename=cached_file_path)
        return cached_file_path
