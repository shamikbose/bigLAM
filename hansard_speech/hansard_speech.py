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
"""
A dataset containing every speech in the House of Commons from May 1979-July 2020.
"""

import os
import pandas as pd

import datasets

_CITATION = """@misc{odell, evan_2021, 
title={Hansard Speeches 1979-2021: Version 3.1.0}, 
DOI={10.5281/zenodo.4843485}, 
abstractNote={<p>Full details are available at <a href="https://evanodell.com/projects/datasets/hansard-data">https://evanodell.com/projects/datasets/hansard-data</a></p> <p><strong>Version 3.1.0 contains the following changes:</strong></p> <p>- Coverage up to the end of April 2021</p>}, 
note={This release is an update of previously released datasets. See full documentation for details.}, 
publisher={Zenodo}, 
author={Odell, Evan}, 
year={2021}, 
month={May} }
"""

_DESCRIPTION = """
A dataset containing every speech in the House of Commons from May 1979-July 2020.
"""

_HOMEPAGE = "https://evanodell.com/projects/datasets/hansard-data/"

_LICENSE = "Creative Commons Attribution 4.0 International License"

_URLS = {
    "csv": "https://zenodo.org/record/4843485/files/hansard-speeches-v310.csv.zip?download=1",
    "json": "https://zenodo.org/record/4843485/files/parliamentary_posts.json?download=1",
}

fields = [
    "id",
    "speech",
    "display_as",
    "party",
    "constituency",
    "mnis_id",
    "date",
    "time",
    "colnum",
    "speech_class",
    "major_heading",
    "minor_heading",
    "oral_heading",
    "year",
    "hansard_membership_id",
    "speakerid",
    "person_id",
    "speakername",
    "url",
    "parliamentary_posts",
    "opposition_posts",
    "government_posts",
]

logger = datasets.utils.logging.get_logger(__name__)


class HansardSpeech(datasets.GeneratorBasedBuilder):
    """A dataset containing every speech in the House of Commons from May 1979-July 2020."""

    VERSION = datasets.Version("3.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "speech": datasets.Value("string"),
                "display_as": datasets.Value("string"),
                "party": datasets.Value("string"),
                "constituency": datasets.Value("string"),
                "mnis_id": datasets.Value("string"),
                "date": datasets.Value("string"),
                "time": datasets.Value("string"),
                "colnum": datasets.Value("string"),
                "speech_class": datasets.Value("string"),
                "major_heading": datasets.Value("string"),
                "minor_heading": datasets.Value("string"),
                "oral_heading": datasets.Value("string"),
                "year": datasets.Value("string"),
                "hansard_membership_id": datasets.Value("string"),
                "speakerid": datasets.Value("string"),
                "person_id": datasets.Value("string"),
                "speakername": datasets.Value("string"),
                "url": datasets.Value("string"),
                "government_posts": datasets.Sequence(datasets.Value("string")),
                "opposition_posts": datasets.Sequence(datasets.Value("string")),
                "parliamentary_posts": datasets.Sequence(datasets.Value("string")),
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        temp_dir = dl_manager.download_and_extract(_URLS["csv"])
        csv_file = os.path.join(temp_dir, "hansard-speeches-v310.csv")
        json_file = dl_manager.download(_URLS["json"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepaths": [csv_file, json_file], "split": "train",},
            ),
        ]

    def _generate_examples(self, filepaths, split):
        logger.warn("\nThis is a large dataset. Please be patient")
        json_data = pd.read_json(filepaths[1])
        csv_data_chunks = pd.read_csv(filepaths[0], chunksize=50000, dtype="object")
        for data_chunk in csv_data_chunks:
            for _, row in data_chunk.iterrows():
                data_point = {}
                for field in fields[:-3]:
                    data_point[field] = row[field]
                parl_post = json_data.loc[
                    (json_data["mnis_id"] == data_point["mnis_id"])
                    & (json_data["date"] == data_point["date"])
                ]
                opp_post = []
                gov_post = []
                data_point["government_posts"] = gov_post
                data_point["opposition_posts"] = opp_post
                data_point["parliamentary_posts"] = parl_post
                yield data_point["id"], data_point
            break
