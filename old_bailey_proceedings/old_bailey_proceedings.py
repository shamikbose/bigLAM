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

import os
import datasets
import glob
import xml.etree.ElementTree as ET

_CITATION = """@article{Howard2017,
author = "Sharon Howard",
title = "{Old Bailey Online XML Data}",
year = "2017",
month = "4",
url = "https://figshare.shef.ac.uk/articles/dataset/Old_Bailey_Online_XML_Data/4775434",
doi = "10.15131/shef.data.4775434.v2"
}
"""


_DESCRIPTION = """The dataset consists of 2,163 transcriptions of the Proceedings and 475 Ordinary's Accounts marked up in TEI-XML, 
and contains some documentation covering the data structure and variables. Each Proceedings file represents one session of the court (1674-1913), 
and each Ordinary's Account file represents a single pamphlet (1676-1772)
"""

_HOMEPAGE = "https://www.dhi.ac.uk/projects/old-bailey/"

_DATASETNAME = "old_bailey_proceedings"

_LICENSE = "Creative Commons Attribution 4.0 International"

_URL = "https://www.dhi.ac.uk/san/data/oldbailey/oldbailey.zip"

logger = datasets.utils.logging.get_logger(__name__)


class OldBaileyProceedings(datasets.GeneratorBasedBuilder):
    """The dataset consists of 2,163 transcriptions of the Proceedings and 475 Ordinary's Accounts marked up in TEI-XML,
    and contains some documentation covering the data structure and variables. Each Proceedings file represents one session of the court (1674-1913),
     and each Ordinary's Account file represents a single pamphlet (1676-1772)"""

    VERSION = datasets.Version("7.2.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "places": datasets.Sequence(datasets.Value("string")),
                "type": datasets.Value("string"),
                "persons": datasets.Sequence(datasets.Value("string")),
                "date": datasets.Value("string"),
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
        data_dir = dl_manager.download_and_extract(_URL)
        oa_dir = "ordinarysAccounts"
        obp_dir = "sessionsPapers"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dirs": {
                        "OA": os.path.join(data_dir, oa_dir),
                        "OBP": os.path.join(data_dir, obp_dir),
                    },
                },
            ),
        ]

    def convert_text_to_features(self, file, key):
        if key == "OA":
            root_tag = "p"
        else:
            root_tag = "div1/p"
        try:
            xml_data = ET.parse(file)
            root = xml_data.getroot()
            start = root.find("./text/body/div0")
            id = start.attrib["id"]
            date = start.find("interp[@type='date']").attrib["value"]
            text_parts = []
            places, persons = [], []
            for content in start.findall(root_tag):
                for place in content.findall("placeName"):
                    if place.text:
                        place_name = place.text.replace("\n", "").strip()
                    if place_name:
                        places.append(place.text)
                for person in content.findall("persName"):
                    full_name = []
                    for name_part in person.itertext():
                        name_part = (
                            name_part.replace("\n", "").replace("\t", "").strip()
                        )
                        if name_part:
                            full_name.append(name_part)
                    if full_name:
                        persons.append(" ".join(full_name))
                for text_snippet in content.itertext():
                    text_snippet = (
                        text_snippet.replace("\n", "").replace("\t", "").strip()
                    )
                    if text_snippet:
                        text_parts.append(text_snippet)
            full_text = " ".join(text_parts)
            return (
                0,
                {
                    "id": id,
                    "date": date,
                    "type": key,
                    "places": places,
                    "persons": persons,
                    "text": full_text,
                },
            )
        except Exception as e:
            return -1, repr(e)

    def _generate_examples(self, data_dirs):
        for key, data_dir in data_dirs.items():
            for file in glob.glob(os.path.join(data_dir, "*.xml")):
                status_code, ret_val = self.convert_text_to_features(file, key)
                if status_code:
                    logger.exception(
                        f"{os.path.basename(file)} could not be parsed properly"
                    )
                    continue
                else:
                    yield ret_val["id"], ret_val
