import os
import json
import re

import numpy as np
from fuzzywuzzy import process

from spacy.matcher import Matcher
from spacy.tokens import Span

from botActions.action import Action
from botActions.rules.lemma import lemmas


class LemmatizationAction(Action):
    """
    This class should probably be called a token normalization class, as its not a true lemmatizer
    """

    def run(self, configs, result):
        print("\t\033[92m LemmatizationAction running ...\033[0m")
        # Determine the directory and base filename of the result path
        cached_dirname_path = os.path.dirname(result)
        cached_basename_path, _ = os.path.splitext(os.path.basename(result))

        # Construct the path for the cached JSON file by replacing the original extension with '.json'
        cached_file_path = os.path.join(
            cached_dirname_path, cached_basename_path + "-lemmatized" + ".json"
        )

        # Ensure the directory for the cached file exists; create it if not
        os.makedirs(cached_dirname_path, exist_ok=True)

        # If a cached file already exists, avoid reprocessing and return its path
        if os.path.exists(cached_file_path):
            print(f"Inference Text Extraction already cached at {cached_file_path}")
            return cached_file_path

        with open(result, "r") as file:
            data = json.load(file)

        regexes = lemmas

        # Define as an inner function to provide encapsulation
        def levenshtein_distance(s1, s2):
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            # print(
            #     "-------> ",
            #     s1,
            #     s2,
            #     previous_row,
            #     1 - (previous_row[-1] / max(len(s1), len(s2))),
            # )
            return previous_row[-1]

        def matches_any_regex(self, data, text, regexes):
            return any(compiled_pattern.search(text) for compiled_pattern in regexes)

        def normalizeTokens(self, matches):
            spans = []
            h = None
            for token in data:
                # Create the matched span and assign the match_id as a label
                for token_hint in regexes.keys():
                    if matches_any_regex(token, regexes[token_hint]["hint_regexes"]):
                        h = token_hint
                        break
                    else:
                        h = None
                if h is not None:
                    spans.append(
                        [
                            process.extractOne(token, regexes[h]["standard_entities"])[
                                0
                            ],
                            h,
                        ]
                    )
                else:
                    spans.append([span.text, h])
            return spans

        def substitute_standard_names_with_threshold(
            input_array, standard_names, threshold=90
        ):
            substituted_array = []
            for name in input_array:
                # Find the best match and its score
                best_match, score = process.extractOne(name, standard_names)

                # Only substitute if the score is above the threshold
                if score > threshold:
                    print(score, ":", name, ":", best_match)
                    substituted_array.append(best_match)
                else:
                    substituted_array.append(
                        name
                    )  # Keep the original name if no match is good enough
            return substituted_array

        standard_names = [
            "Ryzen 7 7840S",
            "i7-13700H",
            "Ryzen 7 7840U",
            "Core Ultra 7 155H",
            "i7-1360P",
            "Ryzen 7 6800U",
        ]

        substituted_array = substitute_standard_names_with_threshold(
            data, standard_names, 90
        )

        with open(cached_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return cached_file_path

    def regexHints(self):
        return {
            "Intel": {
                "hint_regexes": [
                    re.compile(r"[Ii]ntel"),
                    re.compile(r"[Cc]ore"),
                    re.compile(r"i[357]"),
                ],
                "standard_entities": [
                    "Intel Core i7-1370P",
                    "Intel Core i7-13700H",
                    "Intel Core Ultra 7 155H",
                ],
            },
            "AMD": {
                "hint_regexes": [
                    re.compile(r"AMD", re.IGNORECASE),
                    re.compile(r"Ryzen", re.IGNORECASE),
                ],
                "standard_entities": [
                    "AMD Ryzen 7 7840S",
                    "AMD Ryzen 7 7840U",
                    "AMD Ryzen 9 PRO 7940HS",
                ],
            },
            "Benchmarks": {
                "hint_regexes": [
                    re.compile(r"DaVinci", re.IGNORECASE),
                    re.compile(r"Procyon", re.IGNORECASE),
                ],
                "standard_entities": [
                    "DaVinci Resolve 18",
                    "UL Procyon AI (Integer)",
                ],
            },
            "Products": {
                "hint_regexes": [
                    re.compile(r"Zenbook", re.IGNORECASE),
                    re.compile(r"Lenovo", re.IGNORECASE),
                    re.compile(r"ASUS", re.IGNORECASE),
                    re.compile(r"Acer", re.IGNORECASE),
                ],
                "standard_entities": [
                    "ASUS Zenbook 13 S OLED",
                    "Lenovo Slim 7i",
                    "Lenovo Yoga Slim 7",
                    "ASUS Zenbook 14X",
                    "ASUS Zenbook 14",
                    "Acer Swift Edge 16",
                ],
            },
        }
