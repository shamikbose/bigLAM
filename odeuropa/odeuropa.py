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
"""This dataset is released as part of the Odeuropa project. The annotations are identical to the training set of the ICPR2022-ODOR Challenge.
It contains bounding box annotations for smell-active objects in historical artworks gathered from various digital connections.
The smell-active objects annotated in the dataset either carry smells themselves or hint at the presence of smells.
The dataset provides 15484 bounding boxes on 2116 artworks in 87 object categories.
An additional csv file contains further image-level metadata such as artist, collection, or year of creation."""


import pandas as pd
import json, os
import datasets

_CITATION = """\
@dataset{zinnen_mathias_2022_6367776,
  author       = {Zinnen, Mathias and
                  Madhu, Prathmesh and
                  Kosti, Ronak and
                  Bell, Peter and
                  Maier, Andreas and
                  Christlein, Vincent},
  title        = {Odeuropa Dataset of Smell-Related Objects},
  month        = mar,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {1.0.3},
  doi          = {10.5281/zenodo.6367776},
  url          = {https://doi.org/10.5281/zenodo.6367776}
}
"""

_DESCRIPTION = """\
This dataset is released as part of the Odeuropa project. The annotations are identical to the training set of the ICPR2022-ODOR Challenge.
It contains bounding box annotations for smell-active objects in historical artworks gathered from various digital connections.
The smell-active objects annotated in the dataset either carry smells themselves or hint at the presence of smells.
The dataset provides 15484 bounding boxes on 2116 artworks in 87 object categories.
An additional csv file contains further image-level metadata such as artist, collection, or year of creation.
"""

_HOMEPAGE = "https://zenodo.org/record/6367776"

_LICENSE = "CC BY 4.0"

_URL = "https://zenodo.org/record/6367776/files/odor-dataset.zip?download=1"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Odeuropa(datasets.GeneratorBasedBuilder):
    """It contains bounding box annotations for smell-active objects in historical artworks gathered from various digital connections."""

    VERSION = datasets.Version("1.0.3")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="image_classification",
            version=VERSION,
            description="This dataset contains labels for image classification",
        ),
        datasets.BuilderConfig(
            name="image_segmentation",
            version=VERSION,
            description="This dataset contains annotations in a COCO format",
        ),
        datasets.BuilderConfig(
            name="all",
            version=VERSION,
            description="This dataset contains annotations and classification labels",
        ),
    ]
    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        if self.config.name == "image_segmentation":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "width": datasets.Value("int32"),
                    "height": datasets.Value("int32"),
                    "image_url": datasets.Value("string"),
                    "annotations": datasets.Value("string"),
                    "categories": datasets.Value("string"),                    
                }
                )
                object_dict = {
                    "category_id": datasets.Value("string"),
                    "area": datasets.Value("float32"),
                    "bbox" = 
                }
        elif self.config.name == "image_classification":
            features = datasets.Features()
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "file_name": datasets.Value("string"),
                    "width": datasets.Value("int32"),
                    "height": datasets.Value("int32"),
                    "image_url": datasets.Value("string"),
                    "annotations": datasets.Value("string"),
                    "metadata": {
                        "artist": datasets.Value("string"),
                        "title": datasets.Value("string"),
                        "query": datasets.Value("string"),
                        "part": datasets.Value("string"),
                        "earliest_date": datasets.Value("string"),
                        "latest_date": datasets.Value("string"),
                        "margin_years": datasets.Value("string"),
                        "genre": datasets.Value("string"),
                        "material": datasets.Value("string"),
                        "medium": datasets.Value("string"),
                        "height_of_image_field": datasets.Value("string"),
                        "width_of_image_field": datasets.Value("string"),
                        "type_of_object": datasets.Value("string"),
                        "height_of_object": datasets.Value("string"),
                        "width_of_object": datasets.Value("string"),
                        "diameter_of_object": datasets.Value("string"),
                        "position_of_depiction_on_object": datasets.Value("string"),
                        "current_location": datasets.Value("string"),
                        "repository_number": datasets.Value("string"),
                        "original_location": datasets.Value("string"),
                        "original_place": datasets.Value("string"),
                        "original_position": datasets.Value("string"),
                        "context": datasets.Value("string"),
                        "place_of_discovery": datasets.Value("string"),
                        "place_of_manufacture": datasets.Value("string"),
                        "associated_scenes": datasets.Value("string"),
                        "object_categories": datasets.Value("string"),
                        "related_works_of_art": datasets.Value("string"),
                        "type_of_similarity": datasets.Value("string"),
                        "inscription": datasets.Value("string"),
                        "text_source": datasets.Value("string"),
                        "bibliography": datasets.Value("string"),
                        "photo_archive": datasets.Value("string"),
                        "details_url": datasets.Value("string"),
                        "additional_information": datasets.Value("string"),
                    },
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
        urls = _URL[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "ann_filepath": os.path.join(data_dir, "annotations.json"),
                    "metadata_filepath": os.path.join(data_dir, "metadata.csv"),
                },
            ),
        ]

    def _generate_examples(self, ann_filepath, metadata_filepath):
        annotation_data = json.load(ann_filepath)
        images = annotation_data["images"]
        annotations = annotation_data["annotations"]
        metadata = pd.read_csv(metadata_filepath, dtype="object")
        with open(ann, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    # Yields examples as (key, example) tuples
                    yield key, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield key, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": ""
                        if split == "test"
                        else data["second_domain_answer"],
                    }
