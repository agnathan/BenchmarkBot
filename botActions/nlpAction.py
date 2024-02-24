import os
import re
import json
import logging

import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.matcher import Matcher
from spacy.tokens import Span
from pydantic import StrictStr
from fuzzywuzzy import process

from botActions.action import Action
from botActions.rules.all import (
    benchmarkRules,
    cpuRules,
    gpuRules,
    productRules,
    scoreRules,
)
from botActions.rules.tokenHint import regexes


@Language.factory("debug", default_config={"log_level": "DEBUG"})
class DebugComponent:
    def __init__(self, nlp: Language, name: str, log_level: StrictStr):
        self.logger = logging.getLogger(f"spacy.{name}")
        self.logger.setLevel(log_level)
        self.logger.info(f"Pipeline: {nlp.pipe_names}")

    def __call__(self, doc: Doc) -> Doc:
        is_tagged = doc.has_annotation("TAG")
        self.logger.debug(f"mtokens: {len(doc._.mtokens)} tokens")
        return doc


@Language.factory("matchedtoken", default_config={"case_sensitive": False})
def create_matchedtoken_component(nlp: Language, name: str, case_sensitive: bool):
    return MatchedTokenComponent(nlp, case_sensitive)


class MatchedTokenComponent:
    def __init__(self, nlp: Language, case_sensitive: bool):
        self.matcher = Matcher(nlp.vocab)
        # Add Tokenization Matching Rules
        if "CPU" in self.matcher:
            self.matcher.remove("CPU")
        if "Benchmark" in self.matcher:
            self.matcher.remove("Benchmark")
        if "Score" in self.matcher:
            self.matcher.remove("Score")
        if "Product" in self.matcher:
            self.matcher.remove("Product")

        self.matcher.add("Benchmark", benchmarkRules)
        self.matcher.add("CPU", cpuRules)
        self.matcher.add("GPU", gpuRules)
        self.matcher.add("Product", productRules)
        self.matcher.add("Score", scoreRules)

        if not Doc.has_extension("mtokens"):
            Doc.set_extension("mtokens", default=[])

    def __call__(self, doc: Doc) -> Doc:
        # Add the matched spans when doc is processed
        for match_id, start, end in self.matcher(doc):
            span = Span(doc, start, end, label=match_id)
            mtoken = span.text
            doc._.mtokens.append((mtoken, span.label_))
        return doc


@Language.factory("mlemmatizer", default_config={"case_sensitive": False})
def create_mlemmatizer_component(nlp: Language, name: str, case_sensitive: bool):
    return MLemmatizerComponent(nlp, case_sensitive)


class MLemmatizerComponent:
    def __init__(self, nlp: Language, case_sensitive: bool):
        if not Doc.has_extension("mltokens"):
            Doc.set_extension("mltokens", default=[])

    def __call__(self, doc: Doc) -> Doc:
        def matches_any_regex(text, regexes):
            return any(compiled_pattern.search(text) for compiled_pattern in regexes)

        def normalizeToken(token):
            found_hint = None
            for token_hint in regexes.keys():
                if matches_any_regex(token, regexes[token_hint]["hint_regexes"]):
                    found_hint = token_hint
                    break
            if found_hint is not None:
                return process.extractOne(
                    token, regexes[found_hint]["standard_entities"]
                )[0]
            else:
                return token

        # Add the matched spans when doc is processed
        for mtoken, label in doc._.mtokens:
            # print(mtoken, label)
            mlt = normalizeToken(mtoken)
            doc._.mltokens.append((normalizeToken(mtoken), label))
        return doc


class NLPAction(Action):
    def run(self, configs, result):

        print("\t\033[92mNLPAction running ...\033[0m")

        def handleCPUToken(token, label, dataPoint, depth):
            # The type refers to the processor type and can only be "CPU" or "GPU"
            dataPoint["Type"] = label

            if (
                depth < 1
                and "Processor" in dataPoint
                and dataPoint["Processor"] != token
            ):
                # Find the match and extract everything up to the right of the matched pattern
                match = re.search(r"\d+[Ww]", token)
                if match:
                    dataPoint["Processor"] = dataPoint["Processor"] + " " + token
            else:
                item = token
                if "Processor" in dataPoint:
                    if len(dataPoint["Processor"]) > len(token):
                        item = dataPoint["Processor"]
                dataPoint["Processor"] = token

            return dataPoint

        def handleBenchmarkToken(token, label, dataPoint, depth):
            # if 'Benchmark' in dataPoint and (token.lower() == 'single' or token.lower() == "multi"):
            if depth < 1:
                if "Benchmark" in dataPoint and dataPoint["Benchmark"] != token:
                    # Find the match and extract everything up to the right of the matched pattern
                    match = re.search(r"\s*\d{4}x\d{4}", dataPoint["Benchmark"])
                    if match:
                        # Extract everything up to the end of the match
                        output_string = dataPoint["Benchmark"][: match.start()]
                    else:
                        # If no match is found, return the original string or handle as needed
                        output_string = dataPoint["Benchmark"]
                    dataPoint[label] = output_string + " " + token.capitalize()
                    depth = depth + 1
                else:
                    dataPoint = {}
                    if depth < 1:
                        dataPoint[label] = token
            return dataPoint, depth

        def handleProductToken(token, label, dataPoint):
            item = token
            if "Product" in dataPoint:
                if len(dataPoint["Product"]) < len(token):
                    dataPoint["Product"] = token
            else:
                dataPoint[label] = item
            return dataPoint

        def handleScoreToken(token, label, dataPoint):
            dataPoint[label] = token.replace('"', "")
            return dataPoint

        def collectDataPoints(mltokens, debug=False):
            # Initialize scoped variables
            dataPoint = {"Metric": "Score"}
            points = []
            # Every Data Point should have these
            keys_to_check = ["Benchmark", "Type", "Metric", "Product", "Score"]
            prevTokens = {
                "Benchmark": None,
                "Type": None,
                "Metric": None,
                "Product": None,
                "Processor": None,
                "Score": None,
            }
            tokenDepth = {
                "Benchmark": 0,
                "Type": 0,
                "Metric": 0,
                "Product": 0,
                "Processor": 0,
                "Score": 0,
            }
            prevLabel = []

            for token, label in mltokens:
                # Skip unless second label is a Benchmark or CPU
                if label == prevLabel and (label != "Benchmark" and label != "CPU"):
                    continue

                # Set the current label to the previous label
                prevLabel = label

                # When we get a benchmark label then reset the data point
                if label == "Benchmark":
                    dataPoint, tokenDepth["Benchmark"] = handleBenchmarkToken(
                        token, label, dataPoint, tokenDepth["Benchmark"]
                    )
                elif label == "CPU" or label == "GPU":
                    dataPoint = handleCPUToken(
                        token, label, dataPoint, tokenDepth["Processor"]
                    )
                elif label == "Product":
                    dataPoint = handleProductToken(token, label, dataPoint)
                elif label == "Score":
                    dataPoint = handleScoreToken(token, label, dataPoint)
                else:
                    dataPoint[label] = token

                # All metrics are scores ... this should be parsed and not simply set
                dataPoint["Metric"] = "Score"

                # Check if all keys exist in the dictionary
                all_keys_exist = all(key in dataPoint for key in keys_to_check)

                # If a dataPoint has created dependencies between the tokens for
                # all necessary properties then append the dataPoint to points
                if all_keys_exist:
                    # Append the dataPoint to the points array
                    points.append(dataPoint)

                    # Reset dataPoint and tokenDepth
                    dataPoint = {"Benchmark": dataPoint["Benchmark"]}
                    tokenDepth = {
                        "Benchmark": 0,
                        "Type": 0,
                        "Metric": 0,
                        "Product": 0,
                        "Processor": 0,
                        "Score": 0,
                    }
                    prevTokens = {
                        "Benchmark": None,
                        "Type": None,
                        "Metric": None,
                        "Product": None,
                        "Processor": None,
                        "Score": None,
                    }

            return points

        print("\t Result in NLPAction: ", result)
        # Determine the directory and base filename of the result path
        cached_dirname_path = os.path.dirname(result)
        cached_basename_path, _ = os.path.splitext(os.path.basename(result))

        # Construct the path for the cached JSON file by replacing the original extension with '.json'
        cached_file_path = os.path.join(
            cached_dirname_path, cached_basename_path + "-nlp.json"
        )

        # Ensure the directory for the cached file exists; create it if not
        os.makedirs(cached_dirname_path, exist_ok=True)

        # # If a cached file already exists, avoid reprocessing and return its path
        if os.path.exists(cached_file_path):
            print(
                f"\tTokenization, Lemmatization, and Named Entity Recognition already cached at {cached_file_path}"
            )
            return cached_file_path

        with open(result, encoding="utf8") as f:
            text = f.read()

        # Import the Spacy Trained model
        # We will be using a trained model and rules to identify entities
        nlp = spacy.load(os.path.join("./nlptraining/models", "model-last"))

        # Disable spaCy pipelines that we don't need
        # [
        #     nlp.disable_pipe(pipe_name)
        #     for pipe_name in [
        #         "tok2vec",
        #         "tagger",
        #         "parser",
        #         "attribute_ruler",
        #         "lemmatizer",
        #     ]
        # ]

        # Add the matchtoken pipe
        if nlp.has_pipe("matchedtoken"):
            nlp.remove_pipe("matchedtoken")
        nlp.add_pipe("matchedtoken", before="ner", config={"case_sensitive": False})

        if nlp.has_pipe("mlemmatizer"):
            nlp.remove_pipe("mlemmatizer")
        nlp.add_pipe("mlemmatizer", before="ner", config={"case_sensitive": False})

        # if nlp.has_pipe("debug"):
        #     nlp.remove_pipe("debug")
        # nlp.add_pipe("debug", config={"log_level": "DEBUG"})

        doc = nlp(text)

        r = collectDataPoints(doc._.mltokens)
        # Serialize and save the OCR results to a JSON file
        with open(cached_file_path, "w") as file:
            json.dump(r, file)

        return cached_file_path
