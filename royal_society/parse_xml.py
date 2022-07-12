from cgitb import text
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup

filename = r"C:\Users\Shamik Bose\Downloads\Royal_Society_Corpus_v2.0.2_final\Royal_Society_Corpus_v2.0.2_final.vrt"
with open(filename, "r") as f:
    data = f.read()
for line in data:
    print(line)
    input()
