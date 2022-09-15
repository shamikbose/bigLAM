# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Lampeter Corpus of Early Modern English Tracts is a collection of texts 
on various subject matter published between 1640 and 1740 – a time that is marked 
by the rise of mass publication, the development of a public discourse in many 
areas of everyday life and, last but not least, the standardisation of British English."""

from bs4 import BeautifulSoup
import datasets
from datetime import datetime

_CITATION = """ @misc{20.500.12024/3193,
 title = {The Lampeter Corpus of Early Modern English Tracts},
 url = {http://hdl.handle.net/20.500.12024/3193},
 note = {Oxford Text Archive},
 copyright = {Distributed by the University of Oxford under a Creative Commons Attribution-{ShareAlike} 3.0 Unported License},
"""

_DESCRIPTION = """The Lampeter Corpus of Early Modern English Tracts is a collection of texts on
 various subject matter published between 1640 and 1740 – a time that is marked by the rise of mass 
 publication, the development of a public discourse in many areas of everyday life 
 and, last but not least, the standardisation of British English.
"""

_HOMEPAGE = "https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/3193"

_LICENSE = "Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)"

_URL = "https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/3193/3193.xml?sequence=9&isAllowed=y"

_CLASS_MAP = {
    "L": "Law",
    "E": "Economy",
    "M": "Miscellaneous",
    "P": "Politics",
    "S": "Science",
    "R": "Religion",
}


class LampeterCorpus(datasets.GeneratorBasedBuilder):
    """ The Lampeter Corpus of Early Modern English Tracts is a collection of texts on
        various subject matter published between 1640 and 1740. Each text is associated with a year 
        and one of the following topics: Law, Economy, Religion, Poitics, Science, Miscellaneous
    """

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "date": datasets.Value("date64"),
                "genre": datasets.Value("string"),
                "head": datasets.Value("string"),
                "title": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_file = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_file, "split": "train",},
            ),
        ]

    def _generate_examples(self, filepath, split):
        dt_format = "%Y"
        with open(filepath, encoding="utf-8") as f:
            soup = BeautifulSoup(f, features="xml")
            for entry in soup.find_all("TEI"):
                text_parts = []
                title_with_id = entry.teiHeader.fileDesc.titleStmt.title.text
                id, title = title_with_id.split(":", maxsplit=1)
                id = id.strip()
                title = title.strip()
                date = datetime.strptime(id[-4:], dt_format)
                content = entry.find("text")
                head = content.find("body").find("head")
                if head:
                    head = head.text
                else:
                    head = ""
                body_parts = content.find("body").find_all("p")
                for body_part in body_parts:
                    text_parts.append(body_part.text)
                full_text = " ".join(text_parts)
                genre = _CLASS_MAP[id[0]]
                data_point = {
                    "id": id,
                    "text": full_text,
                    "genre": genre,
                    "date": date,
                    "head": head,
                    "title": title,
                }
                yield id, data_point
