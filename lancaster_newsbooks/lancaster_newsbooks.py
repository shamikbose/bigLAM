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

"""This corpus consists of two collections of seventeenth-century English "newsbooks". Both were drawn from the Thomason Tracts collection, which is held at the British Library and available in graphical form via Early English Books Online (EEBO). The construction of these keyboarded versions were in both cases funded by the British Academy.
The FIRST collection (1654_newsbooks) consists of every newsbook published in London and still surviving in the Thomason Tracts from the first half of 1654 (to be precise, for the second half of December 1653 to the end of May 1654, with one or two additions from the first week in June, 1654). This was constructed for the project "Looking at text re-use in a corpus of seventeenth-century news reportage", funded by the British Academy, grant reference SG-33825. 
The SECOND collection (mercurius_fumigosus) consists of every surviving issue published of the highly idiosyncratic newsbook "Mercurius Fumigosus", written by John Crouch between summer 1654 and early autumn 1655. This was constructed for the project "Decoding the news - Mercurius Fumigosus as a source of news in the interregnum, 1654-1655", funded by the British Academy, grant reference LRG-35423. 
"""


import os
import glob
import datasets
from bs4 import BeautifulSoup

_CITATION = """  @misc{20.500.12024/2531,
 title = {The Lancaster Newsbooks Corpus},
 author = {Thomason, George, d. 1666},
 url = {http://hdl.handle.net/20.500.12024/2531},
 note = {Oxford Text Archive},
 copyright = {Distributed by the University of Oxford under a Creative Commons Attribution-{NonCommercial}-{ShareAlike} 3.0 Unported License.},
 year = {2005} }
"""

_DESCRIPTION = """This corpus consists of two collections of seventeenth-century English "newsbooks". Both were drawn from the Thomason Tracts collection, which is held at the British Library and available in graphical form via Early English Books Online (EEBO). The construction of these keyboarded versions were in both cases funded by the British Academy.
The FIRST collection (1654_newsbooks) consists of every newsbook published in London and still surviving in the Thomason Tracts from the first half of 1654 (to be precise, for the second half of December 1653 to the end of May 1654, with one or two additions from the first week in June, 1654). This was constructed for the project "Looking at text re-use in a corpus of seventeenth-century news reportage", funded by the British Academy, grant reference SG-33825. 
The SECOND collection (mercurius_fumigosus) consists of every surviving issue published of the highly idiosyncratic newsbook "Mercurius Fumigosus", written by John Crouch between summer 1654 and early autumn 1655. This was constructed for the project "Decoding the news - Mercurius Fumigosus as a source of news in the interregnum, 1654-1655", funded by the British Academy, grant reference LRG-35423. 
This is version 1.0 of the corpus, released April 2007; it supercedes earlier versions circulated informally.
For more information about the corpus, see www.ling.lancs.ac.uk/newsbooks
"""

_HOMEPAGE = "https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2531"

_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"

_FOLDERS = ["1654_newsbooks", "mercurius_fumigosus"]
_URLS = [
    "https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/2531/1654_newsbooks.zip?sequence=3&isAllowed=y",
    "https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/2531/mercurius_fumigosus.zip?sequence=6&isAllowed=y",
]

logger = datasets.utils.logging.get_logger(__name__)


class LancasterNewsbooks(datasets.GeneratorBasedBuilder):
    """ This corpus consists of two collections of seventeenth-century English "newsbooks" stored as a set of 303 XML files
    """

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
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
        data_dirs = dl_manager.download_and_extract(_URLS)
        data_dirs = [
            os.path.join(data_dir, folder)
            for data_dir, folder in zip(data_dirs, _FOLDERS)
        ]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dirs": data_dirs, "split": "train"},
            ),
        ]

    def _generate_examples(self, data_dirs, split):
        for subdir in data_dirs:
            for file in glob.glob(os.path.join(subdir, "*.xml")):
                text_parts = []
                with open(file, "r", encoding="latin-1") as fp:
                    soup = BeautifulSoup(fp, features="xml")
                    title = soup.find("title").text
                    id = soup.newsbookDoc.attrs["id"]
                    for text_part in soup.find_all("p"):
                        text_parts.append(text_part.text)
                    full_text = " ".join(text_parts)
                data_point = {"id": id, "title": title, "text": full_text}
                yield id, data_point

