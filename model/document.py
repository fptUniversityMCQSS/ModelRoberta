import re
import os
from os import walk
import io

folder_txt = "data/txt"
folder_pt = "data/pt"


class Document:
    def __init__(self, filename):
        self.name = os.path.splitext(filename)[0]
        self.ex = os.path.splitext(filename)[1]
        self.paragraphs = None
        self.folder = folder_txt
        self.path_txt = folder_txt + "/" + self.name + '.txt'
        self.path_pt = folder_pt + "/" + self.name + '.pt'
        self.status = False

    def open(self):
        with open(self.path_txt, encoding="utf8") as txtFile:
            return [line.strip() for line in txtFile]


def load_documents():
    os.makedirs(folder_txt, exist_ok=True)
    os.makedirs(folder_pt, exist_ok=True)
    documents = []
    for (dir_path, dir_names, filenames) in walk(folder_txt):
        for filename in filenames:
            document = Document(filename)
            documents.append(document)
        break
    return documents


def rawtxt_to_document(file_stream, filename):
    data = file_stream.read().decode()
    document = Document(filename)
    paragraphs = to_paragraphs(data)

    with open(document.path_txt, mode="w", encoding="utf8") as txt_file:
        for line in paragraphs:
            txt_file.write(line + '\n')

    return document


def to_paragraphs(data: str):
    """
        Purpose: convert a string to paragraphs. Each paragraph's length is approximately 100 characters
        Return a list of string.

          data
            Input string
    """
    paragraphs = []
    new_line = ""
    for line in data.split("\n"):
        line = line.strip()
        if len(line) > 0:
            if re.match("[.?!]", line[-1]):
                new_line += line + ' '
                if len(new_line) > 100:
                    new_line = re.sub(r"\s+", " ", new_line).strip()
                    paragraphs.append(new_line)
                    new_line = ""
            elif line[-1] == '-':
                new_line += line[:-1]
            else:
                new_line += line + ' '
    if new_line.strip() != "":
        paragraphs.append(new_line)
    return paragraphs
