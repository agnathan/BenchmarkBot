import cv2
import easyocr
import json
import os

from botActions.action import Action


class OCRTextRecognitionAction(Action):
    def run(self, config, result):
        print("\t\033[92mOCRTextRecognitionAction running ...\033[0m")
        # Determine the directory and base filename of the result path
        cached_dirname_path = os.path.dirname(result)
        cached_basename_path, _ = os.path.splitext(os.path.basename(result))
        # cached_results_path = os.path.join(cached_dirname_path, "all-ocr-results.json")
        # Construct the path for the cached JSON file by replacing the original extension with '.json'
        cached_file_path = os.path.join(
            cached_dirname_path, cached_basename_path + ".json"
        )

        # Ensure the directory for the cached file exists; create it if not
        os.makedirs(cached_dirname_path, exist_ok=True)

        # If a cached file already exists, avoid reprocessing and return its path
        if os.path.exists(cached_file_path):
            print(f"\tInference Text Extraction already cached at {cached_file_path}")
            return cached_file_path

        # Load the image for OCR processing
        img = cv2.imread(result)

        # Initialize the easyOCR reader for English language
        reader = easyocr.Reader(["en"])

        # Perform OCR to extract text from the image without returning the bounding box details
        result = reader.readtext(img, detail=0)

        # # If a cached file already exists, avoid reprocessing and return its path
        if os.path.exists(cached_file_path):
            print(
                f"\OpenVINO or EasyOCR text extraction already cached at {cached_file_path}"
            )
            return cached_file_path

        # Serialize and save the OCR results to a JSON file
        with open(cached_file_path, "w", encoding="utf-8") as file:
            json.dump(result, file)

        # Return the path to the cached JSON file
        return cached_file_path
