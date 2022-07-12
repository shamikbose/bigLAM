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

import csv
import json
import os
import pandas as pd
import datasets

_CITATION = """@article{DBLP:journals/corr/abs-2005-11140,
  author    = {Mariona Coll Ardanuy and
               Federico Nanni and
               Kaspar Beelen and
               Kasra Hosseini and
               Ruth Ahnert and
               Jon Lawrence and
               Katherine McDonough and
               Giorgia Tolfo and
               Daniel C. S. Wilson and
               Barbara McGillivray},
  title     = {Living Machines: {A} study of atypical animacy},
  journal   = {CoRR},
  volume    = {abs/2005.11140},
  year      = {2020},
  url       = {https://arxiv.org/abs/2005.11140},
  eprinttype = {arXiv},
  eprint    = {2005.11140},
  timestamp = {Sat, 23 Jan 2021 01:12:25 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2005-11140.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


_DESCRIPTION = """\
Atypical animacy detection dataset, based on nineteenth-century sentences in English extracted from an open dataset of nineteenth-century books digitized by the British Library (available via https://doi.org/10.21250/db14, British Library Labs, 2014). 
This dataset contains 598 sentences containing mentions of machines. Each sentence has been annotated according to the animacy and humanness of the machine in the sentence. 
"""

_HOMEPAGE = "https://bl.iro.bl.uk/concern/datasets/323177af-6081-4e93-8aaf-7932ca4a390a?locale=en"

_DATASETNAME = "atypical_animacy"

_LICENSE = "CC0 1.0 Universal Public Domain"

_URLS = {
    _DATASETNAME: "https://bl.iro.bl.uk/downloads/59a8c52f-e0a5-4432-9897-0db8c067627c?locale=en",
}


class AtypicalAnimacy(datasets.GeneratorBasedBuilder):
    """Living Machines: A study of atypical animacy. Each sentence has been annotated according to the animacy and humanness of the target in the sentence. Additionally, the context is also provided"""

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
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir, "LwM-nlp-animacy-annotations-machines19thC.tsv"
                    ),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        data = pd.read_csv(filepath, sep="\t", header=0)
        for id, row in data.iterrows():
            date = row.Date
            sentence = row.Sentence.replace("***", "")
            context = row.SentenceCtxt.replace("[SEP]", "").replace("***", "")
            target = row.TargetExpression
            animacy = float(row.animacy)
            humanness = float(row.humanness)
            target_start = row.Sentence.find("***")
            offsets = [target_start, target_start + len(target)]
            id = row.SentenceId
            yield id, {
                "id": id,
                "sentence": sentence,
                "context": context,
                "target": target,
                "animacy": animacy,
                "humanness": humanness,
                "date": date,
                "offsets": offsets,
            }
