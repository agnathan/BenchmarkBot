"""
    This script takes an annotations.json file from a labelling tool such as 
    
    https://tecoholic.github.io/ner-annotator/
    
    and uses scikit-learn to generate the training data and validation data.

    Usage: python ./train-create-ner-training-and-validation-data.py
"""

# Import the JSON library for working with JSON data
import json

# Import the OS library for interacting with the operating system
import os

# Import the spaCy library for NLP tasks
import spacy

# Import the tqdm library dividing the annotations
from tqdm import tqdm

# Import the train_test_split function for splitting data
from sklearn.model_selection import train_test_split

# Import the DocBin class for creating binary document representations
from spacy.tokens import DocBin


# Open the annotations file and read it into a variable named "data"
with open(os.path.join("annotations", "annotations.json"), encoding="utf8") as f:
    data = json.loads(f.read())

# Create the Scapy blank pipeline
nlp = spacy.blank("en")

# Create a DocBin to store the training data
db = DocBin()


def get_spacy_doc(file, data):
    print(data)
    # Iterate through the annotations
    for text, annot in tqdm(data):
        doc = nlp.make_doc(text)
        print(
            "==================================================================================="
        )
        print("text: ", text)
        print("annotations: ", annot)
        annot = annot["entities"]
        print("Number of annotations: ", len(annot))
        ents = []
        entity_indices = []

        # Extract entities from the annotations
        for start, end, label in annot:
            # print("----------------------", start, end, label)
            skip_entity = False
            for idx in range(start, end):
                if idx in entity_indices:
                    skip_entity = True
                    break
            if skip_entity:
                continue

            entity_indices = entity_indices + list(range(start, end))
            try:
                print("Adding Span: ", start, end, label)
                span = doc.char_span(start, end, label=label, alignment_mode="strict")
            except:
                continue

            if span is None:
                # Log errors for annotations that couldn't be processed
                err_data = str([start, end]) + "    " + str(text) + "\n"
                # print(err_data)
            else:
                ents.append(span)

            try:
                doc.ents = ents
                db.add(doc)
            except:
                pass

    return db


# Use 80% of the annotations for training and 20% for validation
# train, test = train_test_split(data, test_size=0.5)

# print("+++++++++++++++++++++++++++++++++++++++", len(train), len(test))

# Open a file to log errors during annotation processing
file = open("./training.log", "w")

# Create spaCy DocBin objects for training and testing data
db = get_spacy_doc(file, data)
# db = get_spacy_doc(file, train)
db.to_disk("./train_data-model2.spacy")

# db = get_spacy_doc(file, test)
# db = get_spacy_doc(file, data)
db.to_disk("./test_data-model2.spacy")

# Close the error log file
file.close()
