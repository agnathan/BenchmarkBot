Training the Spacy Named Entity Recogizer requires the following steps

1. Annotate the data using https://tecoholic.github.io/ner-annotator/
2. Merge the new annotated data with annotations.json
3. Go to the training directory and run
   python .\train-create-ner-training-and-validation-data.py
   python -m spacy train .\config.cfg --output ./models --paths.train .\train_data.spacy --paths.dev .\test_data.spacy

4.Test the results
python .\text-ner-inference.py
