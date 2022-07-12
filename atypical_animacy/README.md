[Needs More Information]

# Dataset Card for atypical_animacy

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

- **Homepage:** https://bl.iro.bl.uk/concern/datasets/323177af-6081-4e93-8aaf-7932ca4a390a?locale=en
- **Repository:** https://github.com/Living-with-machines/AtypicalAnimacy
- **Paper:** https://arxiv.org/abs/2005.11140
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

Atypical animacy detection dataset, based on nineteenth-century sentences in English extracted from an open dataset of nineteenth-century books digitized by the British Library. This dataset contains 598 sentences containing mentions of machines. Each sentence has been annotated according to the animacy and humanness of the machine in the sentence. 

### Supported Tasks and Leaderboards

- `text-classification` - This dataset can be used to determine if a mention of an entity in a document was humanlike or not
- `entity-recognition` - The dataset can be used to fine tune large models for NER, albeit for a very specific use case

### Languages

The text in the dataset is in English, as written by authors of books digitized by the British Library. The associated BCP-47 code in `en`

## Dataset Structure

### Data Instances

{
'id': '002757962_01_184_16', 
'sentence': '100 shows a Cornish boiler improperly seated with one small side flue and a bottom flue.', 
'context': 'Fig.  100 shows a Cornish boiler improperly seated with one small side flue and a bottom flue.  The effect of this on a long boiler is to cause springing and leakage of the seams from the heat being applied to one side of the boiler only.', 
'target': 'boiler', 
'animacy': 0.0, 
'humanness': 1.0, 
'offsets': [20, 26], 
'date': '1893'
}

### Data Fields

- id: sentence identifier according to internal Living with Machines BL books indexing.
- sentence: sentence where target expression occurs.
- context: sentence where target expression occurs, plus one sentence to the left and one sentence to the right.
- target: target expression
- animacy: animacy of the target expression
- humanness: humanness of the target expression


### Data Splits

Train 598

## Dataset Creation

### Curation Rationale

The dataset was created by manually annotating books that had been digitized by the British Library. According to the paper's authors, "we provide a basis for examining how machines were imagined during the nineteenth century as everything from lifeless mechanical objects to living beings, or even human-like agents that feel, think, and love. We focus on texts from nineteenth-century Britain, a society being transformed by industrialization, as a good candidate for studying the broader issue"

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

[Needs More Information]