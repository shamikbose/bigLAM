import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

filename = r"C:\Users\Shamik Bose\Downloads\3193.xml"
with open(filename, "r", encoding="UTF-8") as f:
    soup=BeautifulSoup(f, features='xml')
    for entry in soup.find_all("TEI"):
        text_parts = []
        title_with_id = entry.teiHeader.fileDesc.titleStmt.title.text
        id, title = title_with_id.split(":", maxsplit=1)
        id = id.strip()
        title=title.strip()
        date=id[-4:]
        content = entry.find("text")
        head=content.find("body").find("head")
        if head:
            head=head.text
        else:
            head=""
        body_parts=content.find("body").find_all("p")
        for body_part in body_parts:
            text_parts.append(body_part.text)
        full_text = " ".join(text_parts)
        print(f'ID:{id}, Date: {date}')
        # input()



