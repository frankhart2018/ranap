import os
import glob
import json
from simplpy.dict_ import dict_sort


DOCS_DIR = "docs"
DIRS = glob.glob(os.path.join(DOCS_DIR, "*/"))
MAPPING_FILE_PATHS = [os.path.join(DIR, "mapping") for DIR in DIRS]

def get_dictionary_from_mapping_file(mapping_file_path, dictionary):
    with open(mapping_file_path, "r") as file:
        mapping_file_contents = file.read().split("\n")

    for line in mapping_file_contents:
        if not line.startswith("-") and len(line) > 0:
            ranap_word, english_word = line.split(":")
            ranap_word = ranap_word.strip()
            english_word = english_word.strip()
            dictionary[ranap_word] = english_word

    return dictionary

dictionary = {}
for mapping_file_path in MAPPING_FILE_PATHS:
    dictionary = get_dictionary_from_mapping_file(mapping_file_path=mapping_file_path, dictionary=dictionary)

dictionary = dict_sort(dictionary, by="key")

with open("dictionary.json", "w") as file:
    json.dump(dictionary, file, indent=4)