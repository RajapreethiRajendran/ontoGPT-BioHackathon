# OntoGPT Habitat Ontology Extraction

## Overview
This project enhances [OntoGPT](https://github.com/monarch-initiative/ontogpt) by creating templates to extract ontologies of habitat information from the Senckenberg database. The work was done as part of [BioHackathon Germany 2024](https://www.denbi.de/de-nbi-events/1757-3rd-biohackathon-germany-building-on-top-of-ontogpt).

## Installation & Setup
### 1. Fork and Install OntoGPT
Fork the [OntoGPT repository](https://github.com/monarch-initiative/ontogpt) and follow the [installation guide](https://monarch-initiative.github.io/ontogpt/) to set it up.

### 2. Set Up Ollama and LLMs
To run OntoGPT locally with **Llama 3** and **Mistral**, install [Ollama](https://github.com/ollama/ollama) by following the provided instructions. Once OntoGPT and Ollama are correctly configured with Llama 3 and Mistral, the system is ready to run.

## Running OntoGPT with Habitat Extraction Templates
### 1. Using Custom Templates
- Sample templates are available within OntoGPT.
- Custom templates for this use case are available in the `templates` folder of this repository.
- Additional templates from [bh24de_ontogpt](https://github.com/dnlbauer/bh24de_ontogpt) can also be used. These templates need to be placed in the OntoGPT project directory.

### 2. Extracting Habitat Information
This project includes extracted habitat information from senckenberg collections in the `habitat_records.xlsx`. The script `extract_ontology_from_excel.py` can be used to process this data using OntoGPT.

## Contributions
We experimented with habitat ontology extraction using **Llama 3** and **Mistral AI** models during the BioHackathon. We analyzed the importance of prompt engineering and its impact on results, as small changes in the prompt or even the order of extracted attributes significantly influenced the output. 

The choice of model proved crucial, requiring template adjustments to match each model's strengths. In general, Mistral outperformed Llama for this specific task. Additionally, the output was language-dependent, showing improved results when the input was first translated into English. 

Most LLMs are trained on commonly used terms, which presents challenges when working with specialized scientific data. It would be interesting to investigate whether a model trained on a domain-specific scientific dataset would yield better results.



