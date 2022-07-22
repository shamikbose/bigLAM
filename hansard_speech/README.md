---
annotations_creators:
- no-annotation
language:
- '`en:GB`'
language_creators:
- expert-generated
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Hansard Speeches
size_categories:
- 1M<n<10M
source_datasets:
- original
tags:
- speeches
- politics
- parliament
- british
task_categories:
- text-classification
task_ids:
- multi-class-classification
---

# Dataset Card for hansard_speech

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://evanodell.com/projects/datasets/hansard-data/
- **Repository:** https://github.com/evanodell/hansard-data3
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Evan Odell](https://github.com/evanodell)

### Dataset Summary

A dataset containing every speech in the House of Commons from May 1979-July 2020. Quoted from the dataset homepage

> Please contact me if you find any errors in the dataset. The integrity of the public Hansard record is questionable at times, and while I have improved it, the data is presented "as is".

### Supported Tasks and Leaderboards

- `text-classification`: This dataset can be used to clasify various texts (transcribed from speeches) as different time periods or as different types

### Languages

`en:GB`

## Dataset Structure

### Data Instances

```
{
'id': 'uk.org.publicwhip/debate/1979-05-10a.23.4', 
'speech': 'Malcolm Leslie Rifkind, esquire, Edinburgh, Pentlands.', 
'display_as': 'Unknown', 
'party': nan, 
'constituency': nan, 
'mnis_id': nan, 
'date': '1979-05-10', 
'time': nan, 
'colnum': '23', 
'speech_class': 'Procedural', 
'major_heading': 'MEMBERS SWORN', 
'minor_heading': nan, 
'oral_heading': nan, 
'year': 1979, 
'hansard_membership_id': nan, 
'speakerid': nan, 
'person_id': nan, 
'speakername': 'Unknown', 
'url': nan
}
```

### Data Fields

|Variable|Description|
|---|---|
|id|The ID as assigned by mysociety|
|speech|The text of the speech|
|display_as|	The standardised name of the MP.|
|party|The party an MP is member of at time of speech|
|constituency|	Constituency represented by MP at time of speech|
|mnis_id|	The MP's Members Name Information Service number|
|date|Date of speech|
|time|Time of speech|
|colnum	|Column number in hansard record|
|speech_class	|Type of speech|
|major_heading|	Major debate heading|
|minor_heading|	Minor debate heading|
|oral_heading|	Oral debate heading|
|year	|Year of speech|
|hansard_membership_id|	ID used by mysociety|
|speakerid	|ID used by mysociety|
|person_id	|ID used by mysociety|
|speakername|	MP name as appeared in Hansard record for speech|
|url| link to speech|
|government_posts|	Government posts held by MP (list-column)|
|opposition_posts	|Opposition posts held by MP (list-column)|
|parliamentary_posts|	Parliamentary posts held by MP (list-column)|

### Data Splits

Train: 2694375

## Dataset Creation

### Curation Rationale

This dataset contains all the speeches made in the House of Commons and can be used for a number of deep learning tasks like detecting how language and societal views have changed over the >40 years this dataset encompasses

### Source Data

#### Initial Data Collection and Normalization

The dataset is created by getting the data from [data.parliament.uk](http://data.parliament.uk/membersdataplatform/memberquery.aspx). There is no normalization

#### Who are the source language producers?

[N/A]

### Annotations

#### Annotation process

None

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

This is public information, so there should not be any personal and sensitive information

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to understand how language use and society's views have changed over time. 

### Discussion of Biases

Because of the long time period this dataset spans, it might contain language and opinions that are unacceptable in modern society

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

This dataset was built on top of [parlparse](https://github.com/mysociety/parlparse) by [Evan Odell](https://github.com/evanodell)

### Licensing Information

Creative Commons Attribution 4.0 International License

### Citation Information

```
@misc{odell, evan_2021, 
title={Hansard Speeches 1979-2021: Version 3.1.0}, 
DOI={10.5281/zenodo.4843485}, 
abstractNote={<p>Full details are available at <a href="https://evanodell.com/projects/datasets/hansard-data">https://evanodell.com/projects/datasets/hansard-data</a></p> <p><strong>Version 3.1.0 contains the following changes:</strong></p> <p>- Coverage up to the end of April 2021</p>}, 
note={This release is an update of previously released datasets. See full documentation for details.}, 
publisher={Zenodo}, 
author={Odell, Evan}, 
year={2021}, 
month={May} }
```