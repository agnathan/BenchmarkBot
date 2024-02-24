# Import System Libraries
import os
from pathlib import Path

# Import 3rd party libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import openvino as ov
from PIL import Image

# Import project classes
from botActions.action import Action


class OpenVINOTextRecognitionAction(Action):

    def run(self, config, result):
        print("\t\033[92m OpenVINOTextRecognitionAction running ...\033[0m")
        threshold = 0.12
        cached_dirname_path = os.path.dirname(result)
        cached_basename_path, _ = os.path.splitext(os.path.basename(result))

        cached_file_path = os.path.join(
            cached_dirname_path, cached_basename_path + "-" + str(threshold) + ".txt"
        )

        # Create 'cachedData' directory if it doesn't exist
        os.makedirs(cached_dirname_path, exist_ok=True)

        # Check if the video is already cached
        if os.path.exists(cached_file_path):
            print(
                f"OpenVINO or EasyOCR text extraction already cached at {cached_file_path}"
            )
            return cached_file_path

        core = ov.Core()

        model_dir = Path("model")
        precision = "FP16"
        detection_model = "horizontal-text-detection-0001"
        recognition_model = "text-recognition-resnet-fc"

        model_dir.mkdir(exist_ok=True)
        detection_model_path = Path(
            "..\\openvino-models\\intel\\horizontal-text-detection-0001\\FP16\\horizontal-text-detection-0001.xml"
        )
        recognition_model_path = Path(
            "..\\openvino-models\\public\\text-recognition-resnet-fc\\FP16\\text-recognition-resnet-fc.xml"
        )

        detection_model = core.read_model(
            model=detection_model_path, weights=detection_model_path.with_suffix(".bin")
        )
        detection_compiled_model = core.compile_model(
            model=detection_model, device_name="AUTO"
        )

        detection_input_layer = detection_compiled_model.input(0)
        # The `image_file` variable can point to a URL or a local image.
        # image_file = ".\\Hardware-Canucks-Intel-Finally-Nailed-It121.jpg"
        image_file = result
        image = cv2.imread(image_file)
        wshape, hshape = image.shape[:2]

        # N,C,H,W = batch size, number of channels, height, width.
        N, C, H, W = detection_input_layer.shape

        # Resize the image to meet network expected input sizes.
        resized_image = cv2.resize(image, (W, H))

        # Reshape to the network input shape.
        input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        output_key = detection_compiled_model.output("boxes")
        boxes = detection_compiled_model([input_image])[output_key]

        # Remove zero only boxes.
        boxes = boxes[~np.all(boxes == 0, axis=1)]

        def multiply_by_ratio(ratio_x, ratio_y, box):
            return [
                max(shape * ratio_y, 10) if idx % 2 else shape * ratio_x
                for idx, shape in enumerate(box[:-1])
            ]

        def multiply_by_ratio2(ratio_x, ratio_y, box):
            return [
                max(shape * ratio_y, 10) if idx % 2 else shape * ratio_x
                for idx, shape in enumerate(box)
            ]

        def run_preprocesing_on_crop(crop, net_shape):
            temp_img = cv2.resize(crop, net_shape)
            temp_img = temp_img.reshape((1,) * 2 + temp_img.shape)
            return temp_img

        def convert_result_to_image(
            bgr_image, resized_image, boxes, threshold=0.3, conf_labels=True
        ):
            # Define colors for boxes and descriptions.
            colors = {
                "red": (255, 0, 0),
                "green": (0, 255, 0),
                "white": (255, 255, 255),
            }

            # Fetch image shapes to calculate a ratio.
            (real_y, real_x), (resized_y, resized_x) = (
                image.shape[:2],
                resized_image.shape[:2],
            )
            ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

            # Convert the base image from BGR to RGB format.
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

            # Iterate through non-zero boxes.
            for box, annotation in boxes:
                # Pick a confidence factor from the last place in an array.
                print("Box: ", box)
                conf = box[-1]
                if conf > threshold:
                    # Convert float to int and multiply position of each box by x and y ratio.
                    mr = multiply_by_ratio2(ratio_x, ratio_y, box)
                    (x_min, y_min, x_max, y_max) = map(int, mr)

                    # Draw a box based on the position. Parameters in the `rectangle` function are: image, start_point, end_point, color, thickness.
                    cv2.rectangle(
                        rgb_image, (x_min, y_min), (x_max, y_max), colors["green"], 3
                    )

                    # Add a text to an image based on the position and confidence. Parameters in the `putText` function are: image, text, bottomleft_corner_textfield, font, font_scale, color, thickness, line_type
                    if conf_labels:
                        # Create a background box based on annotation length.
                        (text_w, text_h), _ = cv2.getTextSize(
                            f"{annotation}", cv2.FONT_HERSHEY_TRIPLEX, 0.8, 1
                        )
                        image_copy = rgb_image.copy()
                        cv2.rectangle(
                            image_copy,
                            (x_min, y_min - text_h - 10),
                            (x_min + text_w, y_min - 10),
                            colors["white"],
                            -1,
                        )
                        # Add weighted image copy with white boxes under a text.
                        cv2.addWeighted(image_copy, 0.4, rgb_image, 0.6, 0, rgb_image)
                        cv2.putText(
                            rgb_image,
                            f"{annotation}",
                            (x_min, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            colors["red"],
                            1,
                            cv2.LINE_AA,
                        )
            print(rgb_image)
            return rgb_image

        recognition_model = core.read_model(
            model=recognition_model_path,
            weights=recognition_model_path.with_suffix(".bin"),
        )

        recognition_compiled_model = core.compile_model(
            model=recognition_model, device_name="AUTO"
        )

        recognition_output_layer = recognition_compiled_model.output(0)
        recognition_input_layer = recognition_compiled_model.input(0)

        # Get the height and width of the input layer.
        _, _, H, W = recognition_input_layer.shape

        # Calculate scale for image resizing.
        (real_y, real_x), (resized_y, resized_x) = (
            image.shape[:2],
            resized_image.shape[:2],
        )
        ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

        # Convert the image to grayscale for the text recognition model.
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Get a dictionary to encode output, based on the model documentation.
        letters = "~0123456789abcdefghijklmnopqrstuvwxyz"

        # Prepare an empty list for annotations.
        annotations = list()
        cropped_images = list()
        # fig, ax = plt.subplots(len(boxes), 1, figsize=(5,15), sharex=True, sharey=True)
        # Get annotations for each crop, based on boxes given by the detection model.
        for i, crop in enumerate(boxes):
            # Get coordinates on corners of a crop.
            (x_min, y_min, x_max, y_max) = map(
                int, multiply_by_ratio(ratio_x, ratio_y, crop)
            )
            image_crop = run_preprocesing_on_crop(
                grayscale_image[y_min:y_max, x_min:x_max], (W, H)
            )

            # Run inference with the recognition model.
            result = recognition_compiled_model([image_crop])[recognition_output_layer]

            # Squeeze the output to remove unnecessary dimension.
            recognition_results_test = np.squeeze(result)

            # Read an annotation based on probabilities from the output layer.
            annotation = list()
            for letter in recognition_results_test:
                parsed_letter = letters[letter.argmax()]

                # Returning 0 index from `argmax` signalizes an end of a string.
                if parsed_letter == letters[0]:
                    break
                annotation.append(parsed_letter)
            annotations.append("".join(annotation))
            cropped_image = Image.fromarray(image[y_min:y_max, x_min:x_max])
            cropped_images.append(cropped_image)

        boxes_with_annotations_orig = list(zip(boxes, annotations))
        sorted_array = sorted(
            boxes_with_annotations_orig, key=lambda x: x[0][1]
        )  # Sort by the second element of the first element in each tuple

        # If you want to sort in descending order, you can use the reverse parameter
        # sorted_array = sorted(your_array, key=lambda x: x[0][1], reverse=True)

        boxes_with_annotations = sorted_array

        # (array([86.22356, 514.95044, 126.24007, 534.7881, 0.5981575], dtype=float32), '171360')
        # print(boxes_with_annotations)
        # boxes_with_annotations = np.copy(boxes_with_annotations_orig)
        # Set the y1 threshold
        y1_threshold = 100  # You can adjust this threshold value

        def group_text_lines(currentItem, boxes, grouped=[], threshold=0.06):
            """
            This function finds all text bounding boxes that are near each other and combines them to
            have bounding box that don't just surrent single words but entire phrases
            """

            # print(
            #     "\n\n==========================group_text_lines called =============================================="
            # )
            # print("currentItem: ", currentItem)
            # print("Boxes: ", boxes)

            # Get the y1 coordinate of the text box and calculate a lower and upper threshold for grouping
            y1_center = currentItem[0][1]
            y1_threshold_lower = y1_center - int(
                (float(y1_center) * threshold)
            )  # You can adjust this threshold value
            y1_threshold_upper = y1_center + int(
                (float(y1_center) * threshold)
            )  # You can adjust this threshold value

            print("y1_threshold_lower: ", y1_threshold_lower)
            print("y1_threshold_upper: ", y1_threshold_upper)

            grouped_items = [currentItem]
            grouped_item_indices = []
            for index, item in enumerate(boxes):
                coordinates = item[0]
                label = item[1]
                if (
                    int(y1_threshold_lower)
                    < int(coordinates[1])
                    < int(y1_threshold_upper)
                ):
                    # print(index, int(y1_threshold_lower), coordinates[1], int(y1_threshold_upper))
                    grouped_item_indices.append(index)
                    grouped_items.append(item)
            # print("+++++++++++++++++++++++++++++")
            # print(grouped_item_indices)
            print("+++++++++++++++++++++++++++++")
            print(grouped_items)

            remaining_items = [
                item
                for index, item in enumerate(boxes)
                if index not in grouped_item_indices
            ]
            # print(remaining_items)

            # Sort the bounding box in the x direction
            sorted_grouped_items = sorted(grouped_items, key=lambda x: x[0][0])

            combined_item = (
                [
                    np.min([item[0][0] for item in sorted_grouped_items]),  # min x1
                    np.min([item[0][1] for item in sorted_grouped_items]),  # min y1
                    np.max([item[0][2] for item in sorted_grouped_items]),  # max x2
                    np.max([item[0][3] for item in sorted_grouped_items]),  # max y2
                ],
                " ".join(
                    [item[1] for item in sorted_grouped_items]
                ),  # combined labels with space
            )

            # print(combined_item)

            grouped.append(combined_item)

            if len(remaining_items) > 1:
                firstItem, *rest = remaining_items
                # print(len(rest))
                # print(firstItem, rest, grouped, threshold)
                return group_text_lines(firstItem, rest, grouped, threshold)
            else:
                return grouped

        try:
            firstItem, *rest = boxes_with_annotations
        except:
            return None
        boxes = group_text_lines(firstItem, rest, [], threshold)
        res = ""
        for line in boxes:
            print(line)
            res = res + " " + line[1]
        # basename, extension = os.path.splitext(result)
        # Remove extension by slicing
        # print("extension: ", extension)

        with open(cached_file_path, "w") as file:
            #     # Write the string to the file
            file.write(res)
        return cached_basename_path
