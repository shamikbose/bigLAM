from xml.dom import minidom
from bs4 import BeautifulSoup


def is_tag(line):
    if line.startswith("<") and line.endswith(">"):
        return True
    else:
        return False


def decode_tag(tag):
    tag = BeautifulSoup(line, "lxml")
    return tag


filename = r"C:\Users\Shamik Bose\Downloads\Royal_Society_Corpus_v2.0.2_final\Royal_Society_Corpus_v2.0.2_final.vrt"
with open(filename, "r", encoding="utf-8") as f:
    data = f.readlines()

for line in data:
    line = line.strip()
    if is_tag(line):
        tag = decode_tag(line)
        print(tag.name)
        input()
