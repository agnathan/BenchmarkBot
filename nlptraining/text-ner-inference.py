import os
import sys

# Import the spaCy library
import spacy
from spacy.tokens import DocBin

# Check if a filename is provided
if len(sys.argv) != 2:
    print("Usage: python my_script.py filename")
    exit(1)

# Get the filename from the command line argument
filename = sys.argv[1]

# Open the file and read its contents
with open(filename, "r", encoding="utf-8") as f:
    file_contents = f.read()
# nlp = spacy.load("en_core_web_sm")
# docbin_loaded = DocBin().from_disk(os.path.join("training", "train_data.spacy"))
# docs_loaded = list(docbin_loaded.get_docs(nlp.vocab))
# print(docs_loaded)

# Load the trained spaCy NER model from the specified path
nlp = spacy.load(os.path.join("models2", "model-last"))
# # nlp = spacy.load("en_core_web_sm")

# # Process the extracted text using the loaded spaCy NER model
doc = nlp(file_contents)

# # Iterate through the named entities (entities) recognized by the model
for ent in doc.ents:
    # Print the recognized text and its corresponding label
    print(ent.text, "  ->>>>  ", ent.label_)


# Cinebench R23 / Single Core   ->>>>   BENCHMARK
# Intel Core i7-1370P   ->>>>   CPU
# 1995
# Points   ->>>>   SCORE
# Apple M3 Pro 12-Core   ->>>>   CPU
# Apple MacBook Pro 16 2023 M3 Pro   ->>>>   PRODUCT
# 1977
# Points   ->>>>   SCORE
# Intel Core i7-13700H   ->>>>   CPU
# SCHENKER Vision 14 2023   ->>>>   PRODUCT
# 1912
# Points   ->>>>   SCORE
# Intel Core i7-13700H   ->>>>   CPU
# Microsoft Surface Laptop Studio 2 RTX 4060   ->>>>   PRODUCT
# Intel Core i7-1360P   ->>>>   CPU
