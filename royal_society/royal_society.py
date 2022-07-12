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
import xml.etree.ElementTree as et

_CITATION = """@inproceedings{kermes-etal-2016-royal,
    title = "The Royal Society Corpus: From Uncharted Data to Corpus",
    author = {Kermes, Hannah  and
      Degaetano-Ortlieb, Stefania  and
      Khamis, Ashraf  and
      Knappen, J{\"o}rg  and
      Teich, Elke},
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://aclanthology.org/L16-1305",
    pages = "1928--1931",
    abstract = "We present the Royal Society Corpus (RSC) built from the Philosophical Transactions and Proceedings of the Royal Society of London. At present, the corpus contains articles from the first two centuries of the journal (1665―1869) and amounts to around 35 million tokens. The motivation for building the RSC is to investigate the diachronic linguistic development of scientific English. Specifically, we assume that due to specialization, linguistic encodings become more compact over time (Halliday, 1988; Halliday and Martin, 1993), thus creating a specific discourse type characterized by high information density that is functional for expert communication. When building corpora from uncharted material, typically not all relevant meta-data (e.g. author, time, genre) or linguistic data (e.g. sentence/word boundaries, words, parts of speech) is readily available. We present an approach to obtain good quality meta-data and base text data adopting the concept of Agile Software Development.",
}
"""


_DESCRIPTION = """\
The Royal Society Corpus (RSC) is based on the first two centuries of the Philosophical Transactions of the Royal Society of London from its beginning in 1665 to 1869. 
It includes all publications of the journal written mainly in English and containing running text. The Philosophical Transactions was the first periodical of scientific 
writing in England. Founded in 1665 by Henry Oldenburg, the first secretary of the Royal Society, it initially contained excerpts of letters of his scientific 
correspondence, reviews and summaries of recently-published books, and accounts of observations and experiments.
"""

_HOMEPAGE = "https://fedora.clarin-d.uni-saarland.de/rsc/"

_DATASETNAME = "royal_society"

_LICENSE = "Creative Commons Attribution Non Commercial Share Alike 4.0 International"

_URLS = {
    _DATASETNAME: "https://fedora.clarin-d.uni-saarland.de/rsc/data/Royal_Society_Corpus_v2.0.2_final.zip",
}


class AtypicalAnimacy(datasets.GeneratorBasedBuilder):
    """The Royal Society Corpus (RSC) is based on the first two centuries of the Philosophical Transactions of the Royal Society of London from its beginning in 1665 to 1869."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "sentence": datasets.Value("string"),
                "context": datasets.Value("string"),
                "target": datasets.Value("string"),
                "animacy": datasets.Value("float"),
                "humanness": datasets.Value("float"),
                "offsets": [datasets.Value("int32")],
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
        urls = _URLS[_DATASETNAME]
        data_dir = dl_manager.download_and_extract(urls)
        filename = "Royal_Society_Corpus_v2.0.2_final.vrt"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir, filename
                    ),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        data = et.parse(filepath)
        root = data.getroot()
