import datetime
import os
from jinja2 import Template


def read_mapping_file():
    date = datetime.datetime.today().strftime("%d-%m-%Y")
    dir_name = os.path.join("docs", date)
    mapping_file_path = os.path.join(dir_name, "mapping")
    images_dir = os.path.join(dir_name, "images")

    mapping = {}
    with open(mapping_file_path, "r") as file:
        contents = file.read().split("\n")

    image_paths = os.listdir(images_dir)

    for content_line in contents:
        ranap_word, english_word = content_line.split(":")
        ranap_word = ranap_word.strip()
        english_word = english_word.strip()
        specific_image_paths = [path for path in image_paths if os.path.basename(path).startswith(english_word)]
        mapping[ranap_word] = [english_word] + specific_image_paths

    return mapping, date

def get_template_contents(template_path):
    with open(template_path, "r") as file:
        return file.read()

def generate_new_html(path, contents):
    with open(path, "w") as file:
        file.write(contents)

mapping, date = read_mapping_file()
index_contents = get_template_contents("templates/index.html")
class_contents = get_template_contents("templates/word.html")

index_template = Template(index_contents)
index_contents_filled = index_template.render(date=date, ranap_words=list(mapping.keys()))
generate_new_html(os.path.join("docs", os.path.join(date, "index.html")), index_contents_filled)

for ranap_word, list_value in mapping.items():
    class_template = Template(class_contents)
    image_paths = list_value[1:]
    class_contented_filled = class_template.render(ranap_word=ranap_word, image_paths=image_paths)
    generate_new_html(os.path.join("docs", os.path.join(date, ranap_word + ".html")), class_contented_filled)