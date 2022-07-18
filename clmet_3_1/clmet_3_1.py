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
"""The Corpus of Late Modern English Texts, version 3.1 (CLMET3.1) has been created by Hendrik De Smet, 
Susanne Flach, Hans-Jürgen Diller and Jukka Tyrkkö, as an offshoot of a bigger project developing a database
 of text descriptors (Diller, De Smet & Tyrkkö 2011). CLMET3.1 is a principled collection of public domain 
 texts drawn from various online archiving projects. """

import os
import xml.etree.ElementTree as ET
import datasets
from bs4 import BeautifulSoup


_CITATION = """@article{de2015corpus,
  title={Corpus of Late Modern English texts (version 3.1)},
  author={De Smet, Hendrik and Flach, Susanne and Tyrkk{\"o}, Jukka and Diller, Hans-J{\"u}rgen},
  year={2015}
}
"""

_DESCRIPTION = """The Corpus of Late Modern English Texts, version 3.1 (CLMET3.1) has been created by Hendrik De Smet, 
Susanne Flach, Hans-Jürgen Diller and Jukka Tyrkkö, as an offshoot of a bigger project developing a database of text 
descriptors (Diller, De Smet & Tyrkkö 2011). CLMET3.1 is a principled collection of public domain texts drawn from 
various online archiving projects. This dataset can be used for part-of-speech tagging, NER and text classification
"""

_HOMEPAGE = "http://fedora.clarin-d.uni-saarland.de/clmet/clmet.html"

_LICENSE = "Creative Commons Attribution Non Commercial Share Alike 4.0 International"

_DATASETNAME = "clmet"

_URLS = {
    _DATASETNAME: "http://fedora.clarin-d.uni-saarland.de/clmet/clmet3_1.zip",
}

_POS_LIST = [
    "CC",
    "CD",
    "DT",
    "EX",
    "FW",
    "IN",
    "JJ",
    "JJR",
    "JJS",
    "MD",
    "NN",
    "NNS",
    "NP",
    "NPS",
    "PDT",
    "POS",
    "PP",
    "PP$",
    "RB",
    "RBR",
    "RBS",
    "RP",
    "SENT",
    "SYM",
    "TO",
    "UH",
    "VB",
    "VBD",
    "VBG",
    "VBN",
    "VBZ",
    "VBP",
    "WDT",
    "WP",
    "WP$",
    "WRB",
    "XX0",
    "CURR",
    "PUN",
    "LQUO",
    "RQUO",
    "BRL",
    "BRR",
    "LS",
]
_POS_LOOKUP = {tag: idx for idx, tag in enumerate(_POS_LIST)}
_CLASS_LIST = [
    "ADJ",
    "ADV",
    "ART",
    "CONJ",
    "INTJ",
    "PREP",
    "PRON",
    "PUNC",
    "SUBST",
    "SYM",
    "UNC",
    "VERB",
    "QUOT"
]
_CLASS_LOOKUP = {tag: idx for idx, tag in enumerate(_CLASS_LIST)}
logger = datasets.utils.logging.get_logger(__name__)


class CLMET_3_1(datasets.GeneratorBasedBuilder):
    """"""

    VERSION = datasets.Version("3.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain",
            version=VERSION,
            description="This format contains text as single string and the classifications",
        ),
        datasets.BuilderConfig(
            name="class",
            version=VERSION,
            description="This format contains the text as a list of tokens, annotated according to the simplified Oxford wordclass tags",
        ),
        datasets.BuilderConfig(
            name="pos",
            version=VERSION,
            description="This format contains the text as a list of tokens, annotated according to the Penn Treebank POS tags",
        ),
    ]

    DEFAULT_CONFIG_NAME = "plain"

    def _info(self):
        if self.config.name == "plain":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "genre": datasets.Value("string"),
                    "subgenre": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "quarter_cent": datasets.Value("string"),
                    "decade": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "notes": datasets.Value("string"),
                    "comments": datasets.Value("string"),
                    "period": datasets.Value("string"),
                    "id": datasets.Value("string"),
                }
            )
        elif self.config.name == "class":
            logger.warn(f"CLASS tags are as follows: {_CLASS_LIST}")
            features = datasets.Features(
                {
                    "text": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.Value("int32")),
                    "genre": datasets.Value("string"),
                    "subgenre": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "quarter_cent": datasets.Value("string"),
                    "decade": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "notes": datasets.Value("string"),
                    "comments": datasets.Value("string"),
                    "period": datasets.Value("string"),
                    "id": datasets.Value("string"),
                }
            )
        elif self.config.name == "pos":
            logger.warn(f"POS tags are as follows: {_POS_LIST}")
            features = datasets.Features(
                {
                    "text": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.Value("int32")),
                    "genre": datasets.Value("string"),
                    "subgenre": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "quarter_cent": datasets.Value("string"),
                    "decade": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "notes": datasets.Value("string"),
                    "comments": datasets.Value("string"),
                    "period": datasets.Value("string"),
                    "id": datasets.Value("string"),
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
        urls = _URLS[_DATASETNAME]
        data_dir = dl_manager.download_and_extract(urls)
        data_dir = os.path.join(data_dir, "clmet", "corpus", "txt")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_dir": data_dir,
                    "split": "train",
                },
            ),
        ]

    def parse_pos_text(self, content_parts, pos_type):
        tokens = []
        pos_tags = []
        unknown_tag = False
        malformed_token = False
        for content_part in content_parts:
            text = content_part.text.strip()
            for text_part in text.split():
                try:
                    token, pos_tag = text_part.split("_")
                    pos_tag = pos_tag.replace("\n", "").strip().upper()
                    if pos_type == "pos":
                        pos_tag_idx = _POS_LOOKUP.get(pos_tag,-1)
                    else:
                        pos_tag_idx = _CLASS_LOOKUP.get(pos_tag,-1)
                    if pos_tag_idx==-1:
                        unknown_tag = True
                    tokens.append(token)
                    pos_tags.append(pos_tag_idx)
                except Exception as e:
                    malformed_token = True
        return tokens, pos_tags, unknown_tag, malformed_token

    def parse_file(self, file, pos_type):
        with open(file, "r", encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, features="html.parser")
            id = soup.id.text
            period = soup.period.text
            quarter_cent = soup.quartcent.text
            decade = soup.decade.text
            year = soup.year.text
            genre = soup.genre.text
            subgenre = soup.subgenre.text
            title = soup.title.text
            notes = soup.notes.text
            comments = soup.comments.text
            author = soup.author.text
            data_point = {
                "id": id,
                "period": period,
                "genre": genre,
                "subgenre": subgenre,
                "decade": decade,
                "quarter_cent": quarter_cent,
                "title": title,
                "notes": notes if notes else "",
                "comments": comments if comments else "",
                "author": author,
                "year": year,
            }
            content_parts = soup.find("text").find_all("p")

            if pos_type in ["pos", "class"]:
                content = self.parse_pos_text(content_parts, pos_type)
                if content[2]:
                    logger.warn(f'Unknown tag in sample {id}')
                if content[3]:
                    logger.warn(f'Malformed token in sample {id}')
                data_point["text"] = content[0]
                data_point["pos_tags"] = content[1]
            else:
                content = []
                for content_part in content_parts:
                    content.append(content_part.text)
                content = " ".join(content)
                data_point["text"] = content
            return (id, data_point)

    def _generate_examples(self, data_dir, split):
        final_data_dir = os.path.join(data_dir, self.config.name)
        for file in os.listdir(final_data_dir):
            id, data = self.parse_file(
                os.path.join(final_data_dir, file), self.config.name
            )
            yield id, data
