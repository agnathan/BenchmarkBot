# Import system libraries
import os
import json

# Import 3d Party Spacy Libraries
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.lang.en import English  # Token normalization
from spacy.lang.de import German

# Import project classes
from botActions.action import Action


class NamedEntityRecognitionAction(Action):
    def run(self, config, result):
        print("\t\033[92mNamedEntityRecognitionAction running ...\033[0m")

        cached_dirname_path = os.path.dirname(result)
        cached_basename_path, _ = os.path.splitext(os.path.basename(result))

        # cached_results_path = os.path.join(cached_dirname_path, "all-ocr-results.json")
        # cached_target_path = os.path.join(cached_dirname_path, "all-excel-results.json")
        cached_file_path = os.path.join(
            cached_dirname_path, cached_basename_path + "-ner-results.json"
        )

        # Create 'cachedData' directory if it doesn't exist
        os.makedirs(cached_dirname_path, exist_ok=True)

        # Check if the video is already cached
        if os.path.exists(cached_file_path):
            print(
                f"\t NamedEntityRecognitionAction results already cached at {cached_file_path}"
            )
            return cached_file_path

        # Import the Spacy Trained model
        nlp = spacy.load(os.path.join("./nlptraining/models", "model-last"))
        print(f"\t Processing {cached_file_path}")
        with open(result, encoding="utf8") as f:
            text = f.read()

        matcher = Matcher(nlp.vocab)

        # Add Tokenization Matching Rules
        if "CPU" in matcher:
            matcher.remove("CPU")
        if "Benchmark" in matcher:
            matcher.remove("Benchmark")
        if "Score" in matcher:
            matcher.remove("Score")
        if "Product" in matcher:
            matcher.remove("Product")

        matcher.add("Benchmark", self.benchmarkRules())
        matcher.add("CPU", self.cpuRules())
        matcher.add("Product", self.productRules())
        matcher.add("Score", self.scoreRules())

        doc = nlp(text)

        def find_first_match(arr, value):
            for i, element in enumerate(arr):
                if element == value:
                    return i  # Return the index of the first match
            return -1  # Return -1 if no match is found

        def addDataPoint(data, benchmark, btype, metric, col, score):
            if "Benchmark" not in data:
                data["Benchmark"] = [benchmark]
                data["Type"] = [btype]
                data["Metric"] = [metric]
                data[col] = [score]
            elif benchmark not in data["Benchmark"] and col in data.keys():
                for k in data.keys():
                    if k == "Benchmark":
                        data["Benchmark"].append(benchmark)
                    elif k == "Type":
                        data["Type"].append(btype)
                    elif k == "Metric":
                        data["Metric"].append(metric)
                    elif k == col:
                        data[col].append(score)
                    else:
                        data[k].append("")
            elif benchmark in data["Benchmark"] and col not in data.keys():
                r = []
                for benchloop in data["Benchmark"]:
                    if benchmark == benchloop:
                        r.append(score)
                    else:
                        r.append("")
                data[col] = r
            elif benchmark not in data["Benchmark"] and col not in data.keys():
                for k in data.keys():
                    if k == "Benchmark":
                        data["Benchmark"].append(benchmark)
                    elif k == "Type":
                        data["Type"].append(btype)
                    elif k == "Metric":
                        data["Metric"].append(metric)
                    else:
                        data[k].append("")
                ar = []
                for b in data["Benchmark"]:
                    if b == benchmark:
                        ar.append(score)
                    else:
                        ar.append("")
                data[col] = ar

            elif benchmark in data["Benchmark"] and col in data.keys():
                for k in data.keys():
                    if k == col:
                        idx = find_first_match(data["Benchmark"], benchmark)
                        data[k][idx] = score

            return data

        matches = matcher(doc)
        data = {}
        benchmark = None
        btype = "CPU"
        metric = "Score"
        col = None
        processor = None
        product = None
        score = None

        results = []
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            if span.label_ == "Benchmark":
                benchmark = span.text
                col = None
                processor = None
                product = None
                score = None
            elif span.label_ == "CPU":
                processor = span.text
            elif span.label_ == "Product":
                product = span.text
            elif span.label_ == "Score":
                score = span.text.replace('"', "")

            # print((span.text, span.label_, benchmark, btype, metric, processor, product, score))
            if benchmark is not None and processor is not None and score is not None:
                if product is not None:
                    col = product + "\n" + processor
                else:
                    col = processor
                # results.append([benchmark, btype, metric, col, score])
                # print("--------------------------")
                # print(benchmark, btype, metric, col, score)
                # print("--------------------------")
                addDataPoint(data, benchmark, btype, metric, col, score)
                col = None
                score = None
                processor = None
                product = None

        # print(list(data.keys()))
        # print(list(data.values()))

        # Initialize an empty list for the result
        out = []
        row = []
        for k in data.keys():
            row.append(k)
        out.append(row)

        if len(list(data.values())) == 0:
            return None
        else:
            depth = len(list(data.values())[0])
            for i in range(0, depth):
                row = []

                for v in data.values():
                    row.append(v[i])
                out.append(row)
                row = []

            with open(cached_file_path, "w") as file:
                json.dump(out, file)

            # Serialize and save the OCR results to a JSON file
            print("\t Writing to file: ", cached_file_path)
            with open(cached_file_path, "w") as file:
                json.dump(out, file)

        return cached_file_path

    def benchmarkRules(self):
        return [
            [
                {"lower": "cinebench"},
                {"lower": "r23"},
                {"IS_PUNCT": True},
                {"lower": "single"},
                {"lower": "core"},
            ],
            [
                {"lower": "cinebench"},
                {"lower": "r23"},
                {"IS_PUNCT": True},
                {"lower": "multi"},
                {"lower": "core"},
            ],
            [
                {"lower": "cinebench"},
                {"lower": "2024"},
                {"IS_PUNCT": True},
                {"lower": "cpu"},
                {"lower": "single"},
                {"lower": "core"},
            ],
            [
                {"lower": "geekbench"},
                {"TEXT": {"REGEX": "\d+\.?\d*"}},
                {"IS_PUNCT": True},
                {"lower": "single"},
                {"IS_PUNCT": True},
                {"lower": "core"},
            ],
            [
                {"lower": "power"},
                {"lower": "consumption"},
                {"IS_PUNCT": True},
                {"lower": "cinebench"},
                {"lower": "r23"},
                {"lower": "single"},
                {"lower": "power"},
                {"lower": "efficiency"},
            ],
            [
                {"lower": "power"},
                {"lower": "consumption"},
                {"IS_PUNCT": True},
                {"lower": "cinebench"},
                {"lower": "r23"},
                {"lower": "single"},
            ],
            [{"lower": "davinci"}, {"lower": "resolve"}, {"lower": "18"}],
            [{"lower": "handbrake"}, {"lower": "video"}, {"lower": "conversion"}],
            [
                {"lower": "battery"},
                {"lower": "test"},
                {"lower": "chrome"},
                {"lower": "refresh"},
            ],
            [{"lower": "battery"}, {"lower": "test"}],
        ]

    def cpuRules(self):
        return [
            [{"lower": "i7"}, {"IS_PUNCT": True}, {"lower": "1360p"}],
            [{"lower": "i7"}, {"IS_PUNCT": True}, {"lower": "13700h"}],
            [{"lower": "ryzen"}, {"lower": "7"}, {"lower": "6800u"}],
            [
                {"lower": "intel"},
                {"lower": "core"},
                {"lower": "i7"},
                {"IS_PUNCT": True},
                {"TEXT": {"FUZZY2": "1370p"}},
            ],
            [
                {"lower": "apple"},
                {"lower": "m3"},
                {"lower": "pro"},
                {"IS_DIGIT": True},
                {"IS_PUNCT": True},
                {"lower": "core"},
            ],
            [
                {"lower": "intel", "OP": "?"},
                {"lower": "core"},
                {"lower": "ultra"},
                {"lower": "7"},
                {"lower": "155h"},
            ],
            [
                {"lower": "amd", "OP": "?"},
                {"lower": "ryzen"},
                {"lower": "7"},
                {"TEXT": {"REGEX": "7840[SU5]"}},
            ],
            [
                {"lower": "amd", "OP": "?"},
                {"lower": "ryzen"},
                {"lower": "9"},
                {"lower": "pro"},
                {"lower": "7940hs"},
            ],
            [
                {"lower": "qualcomm"},
                {"lower": "snapdragon"},
                {"lower": "x"},
                {"lower": "elite"},
            ],
            [{"lower": " "}, {"lower": "ryzen"}, {"lower": "7"}, {"lower": "6800u"}],
        ]

    def productRules(self):
        return [
            [
                {"lower": "apple"},
                {"lower": "macbook"},
                {"lower": "pro"},
                {"lower": "16"},
                {"lower": "2023"},
                {"lower": "m3"},
                {"TEXT": {"REGEX": "[Pro|Max]"}},
            ],
            [
                {"lower": "schenker"},
                {"lower": "vision"},
                {"lower": "14"},
                {"lower": "2023"},
            ],
            [
                {"lower": "sd"},
                {"lower": "x"},
                {"lower": "elite"},
                {"lower": "reference"},
                {"lower": "80w"},
            ],
            [
                {"lower": "microsoft"},
                {"lower": "surface"},
                {"lower": "laptop"},
                {"lower": "studio"},
                {"lower": "2"},
                {"lower": "rtx"},
                {"lower": "4060"},
            ],
            [{"lower": "lenovo"}, {"lower": "yoga"}, {"lower": "slim"}],
            [{"lower": "lenovo"}, {"lower": "slim"}, {"lower": "7i"}],
            [
                {"lower": "lenovo"},
                {"lower": "yoga"},
                {"lower": "9"},
                {"lower": "14irp"},
                {"lower": "g8"},
            ],
            [
                {"lower": "asus"},
                {"lower": "zenbook"},
                {"lower": "14"},
                {"lower": "ux3405ma", "OP": "?"},
            ],
            [{"lower": "zenbook"}, {"lower": "14x"}],
            [{"lower": "zenbook"}, {"lower": "13"}, {"lower": "$"}, {"lower": "oled"}],
            [{"lower": "acer"}, {"lower": "swift"}, {"lower": "edge"}, {"lower": "16"}],
            [
                {"lower": "acer"},
                {"lower": "swift"},
                {"lower": "go"},
                {"lower": "14"},
                {"lower": "sfg14"},
                {"IS_PUNCT": True},
                {"lower": "72"},
            ],
            [
                {"lower": "lenovo"},
                {"lower": "yoga"},
                {"lower": "slim"},
                {"lower": "7"},
                {"lower": "14apu"},
                {"lower": "g8"},
            ],
            [
                {"lower": "hp"},
                {"lower": "elitebook"},
                {"lower": "845"},
                {"lower": "g10"},
                {"lower": "5z4x0es"},
            ],
            [
                {"lower": "hp"},
                {"lower": "elitebook"},
                {"lower": "845"},
                {"lower": "g10"},
                {"lower": "818n0ea"},
            ],
            [
                {"lower": "framework"},
                {"lower": "laptop"},
                {"lower": "13.5"},
                {"lower": "13th"},
                {"lower": "gen"},
                {"lower": "intel"},
            ],
            [{"lower": "lenovo"}, {"lower": "yoga"}, {"lower": "slim"}, {"lower": "7"}],
        ]

    def scoreRules(self):
        return [
            [{"TEXT": {"REGEX": "\d{1,4}"}}, {"IS_SPACE": True}, {"lower": "points"}],
            [
                {"TEXT": '"'},
                {"TEXT": {"REGEX": "\d[,\.:]\d+"}},
                {"TEXT": '"'},
            ],  # Get times of the format 4:30 or 12:02
        ]
