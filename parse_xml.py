from cgitb import text
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup

filename = r"C:\Users\Shamik Bose\Downloads\Royal_Society_Corpus_v2.0.2_final\Royal_Society_Corpus_v2.0.2_final.vrt"
with open(filename, "r") as f:
    data = f.read()
bs_data = BeautifulSoup(data, "xml")
b_text = bs_data.find_all("text")
for text in b_text:
    print(text.get("title"))
    break
