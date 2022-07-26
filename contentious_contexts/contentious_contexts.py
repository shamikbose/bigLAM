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
"""This dataset contains extracts from historical Dutch newspapers which have been containing keywords of potentially contentious words (according to present-day sensibilities). 
The dataset contains multiple annotations per instance, given the option to quantify agreement scores for annotations."""

import pandas as pd
import datasets


_CITATION = """@misc{ContentiousContextsCorpus2021,
  author = {Cultural AI},
  title = {Contentious Contexts Corpus},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\\url{https://github.com/cultural-ai/ConConCor}},
}
"""

_DESCRIPTION = """This dataset contains extracts from historical Dutch newspapers which have been containing keywords of potentially contentious words (according to present-day sensibilities). 
The dataset contains multiple annotations per instance, given the option to quantify agreement scores for annotations. This dataset can be used to track how words and their meanings have changed over time
"""


_HOMEPAGE = "https://github.com/cultural-ai/ConConCor"


_LICENSE = "CC-BY"

_URLS = [
    "https://raw.githubusercontent.com/cultural-ai/ConConCor/main/Dataset/Annotations.csv",
    "https://raw.githubusercontent.com/cultural-ai/ConConCor/main/Dataset/Extracts.csv",
]
response_mapping = {
    "Omstreden naar huidige maatstaven": "Contentious according to current standards",
    "Niet omstreden": "Not contentious",
    "Weet ik niet": "I don't know",
    "Onleesbare OCR": "Illegible OCR",
}

logger = datasets.utils.logging.get_logger(__name__)


class ContentiousContexts(datasets.GeneratorBasedBuilder):
    """This dataset contains extracts from historical Dutch newspapers which have been containing keywords of potentially contentious words"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "extract_id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "target": datasets.Value("string"),
                "annotator_responses_english": [
                    {
                        "id": datasets.Value("string"),
                        "response": datasets.Value("string"),
                    }
                ],
                "annotator_responses_dutch": [
                    {
                        "id": datasets.Value("string"),
                        "response": datasets.Value("string"),
                    }
                ],
                "annotator_suggestions": [
                    {
                        "id": datasets.Value("string"),
                        "suggestion": datasets.Value("string"),
                    }
                ],
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
        ann_file = dl_manager.download(_URLS[0])
        text_file = dl_manager.download(_URLS[1])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepaths": [ann_file, text_file], "split": "train",},
            ),
        ]

    def _generate_examples(self, filepaths, split):
        annotations = pd.read_csv(filepaths[0], dtype="object")
        texts = pd.read_csv(filepaths[1], dtype="object")
        annotations.fillna("", inplace=True)
        texts.fillna("", inplace=True)
        for _, row in texts.iterrows():
            data_point = {}
            data_point["extract_id"] = row["extract_id"]
            data_point["target"] = row["target_compound_bolded"]
            data_point["text"] = row["text"]
            annotator_responses = annotations[
                annotations["extract_id"] == row["extract_id"]
            ]
            resp_en_list = []
            resp_nl_list = []
            sugg_list = []
            for _, ann_row in annotator_responses.iterrows():
                ann_id = ann_row["anonymised_participant_id"]
                response_dutch = ann_row["response"]
                response_english = response_mapping[response_dutch]
                suggestion = ann_row["suggestion"]
                resp_en_list.append({"id": ann_id, "response": response_english})
                resp_nl_list.append({"id": ann_id, "response": response_dutch})
                sugg_list.append({"id": ann_id, "suggestion": suggestion})

            data_point["annotator_responses_english"] = resp_en_list
            data_point["annotator_responses_dutch"] = resp_nl_list
            data_point["annotator_suggestions"] = sugg_list
            yield data_point["extract_id"], data_point
