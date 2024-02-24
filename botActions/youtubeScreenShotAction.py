# Import System libraries
import os

# Import 3rd party libraries
from pytube import YouTube
import cv2

# Import project classes
from botActions.action import Action


class YoutubeScreenShotAction(Action):
    """
    An Benchmarkbot Action class that takes a video and extracts a screenshot at a given number
    of seconds into the video
    """

    def run(self, config, result):
        """
        Extracts a single frame from a video at a specified time and saves it as an image.

        This function checks if a frame at the specified time already exists at the output path.
        If not, it captures the frame from the video at the given time (in seconds), then saves
        that frame as an image to the specified path. If the output frame already exists, it
        will not overwrite the existing file and will return True immediately.

        Parameters:
        - video_path (str): Path to the video file from which to extract the frame.
        - time_sec (float): The time point in the video (in seconds) at which to extract the frame.
        - cached_file_path (str): Path where the extracted frame will be saved as an image.
        Defaults to "frame.jpg".

        Returns:
        - bool: True if the frame was successfully extracted and saved, or if the frame already
        exists at the specified output path. False if the frame could not be extracted or saved.

        Side Effects:
        - A file at `cached_file_path` may be created or overwritten (if it doesn't already exist).
        - Prints a message if the output frame already exists.
        """
        print("\t\033[92mYoutubeScreenShotAction running ...\033[0m")
        self.url = config["url"]
        self.timeIndex = config["timeindex"]
        self.cache_dir = "cachedData"

        cached_dirname_path = os.path.dirname(result)

        cached_file_path = os.path.join(
            cached_dirname_path, str(self.timeIndex) + ".jpg"
        )

        # Create 'cachedData' directory if it doesn't exist
        os.makedirs(cached_dirname_path, exist_ok=True)

        # Check if the video is already cached
        if os.path.exists(cached_file_path):
            print(f"\t Screenshot already cached at {cached_file_path}")
            return cached_file_path

        # Initialize video capture with the given video file path
        cap = cv2.VideoCapture(result)
        # Retrieve the frames per second (fps) of the video to calculate the frame index
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Calculate the frame index to extract, based on the provided time in seconds and the video's fps
        frame_index = int(self.timeIndex * fps)
        # Set the video position to the calculated frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        # Attempt to read the frame at the calculated index
        success, image = cap.read()
        if success:
            # If the frame is successfully read, save it to the specified output path
            cv2.imwrite(cached_file_path, image)
            print(f"\t Screenshot extracted successfully to {cached_file_path}")
        # Release the video capture object to free resources
        cap.release()
        # Return the success status of reading and saving the frame
        return cached_file_path
