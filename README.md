# Evaluating LLM Agents for Genetic Testing Insurance Workflows 

## This repository is a standalone export of ```RESCUE-n8n/eval/insurance``` (insurance_agent branch from https://github.com/stormliucong/RESCUE-n8n/tree/main/eval/insurance) for reproducibility.

📁 This folder contains the source codes, experimental outputs, and evaluation files associated with our study: **Evaluating Large Language Model Agents for Genetic Testing Insurance Workflows: An End-to-End Assessment of Retrieval and Reliability**.

---

## Requirements & Reproducibility Notes
- Python 3.10+
- OpenAI API key
- Perplexity API key
- SentenceTransformer model (all-MiniLM-L6-v2)
- OpenAI text-embedding-3-small
- Publicly available insurance policy documents (see below section)

⚠️ Due to policy version updates over time, retrieval results may differ slightly if policies have been modified after the study period.
---

## Installation
1. Clone the repository
```bash
git clone https://github.com/CptAswadu/Evaluating-Large-Language-Model-Agents-for-Genetic-Testing-Insurance-Workflows.git
cd Evaluating-Large-Language-Model-Agents-for-Genetic-Testing-Insurance-Workflows
```

2. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Set API Keys
Create a `.env` file in the project root:

```bash
touch .env
OPEN_AI_API_KEY=<your_openai_key_here>
PERPLEXITY_API_KEY=<your_perplexity_key_here>
```

---

## 🧠 Purpose

This study systematically evaluates the reliability of web-search-enabled LLM agents in supporting insurance workflows for **genetic testing**.
We assess performance across four sequential tasks:

1. **In-Network Insurance Provider Retrieval** 
2. **Policy Document Retrieval**
3. **Patient-Policy Match**
4. **LLM Agent for Answering Relevant Questions**

The goal is to quantify retrieval sensitivity, ranking robustness, and downstream decision accuracy.

---

## 📂 Folder Descriptions

### `codes/`
- **Description**: Contains all the scripts and notebooks for this research.
### `dataset/`
- **Description**: Contains all data sources except insurance policies utilized for this research.
### `results/`
- **Description**: Contains all the experiment results for this research.


## 🧪 Experimental Tasks

1. **In-Network Provider Retrieval**  
- Objective: Evaluate whether LLM agents can correctly identify GeneDx in-network payers.  
- Input: Prompt-based queries (model × prompt × iteration).  
- Ground Truth: `dataset/In-Network_Providers_Update.csv`  
- Output: `results/name_retrieval/`  
- Evaluation: GPT-4o-based matching and computation ('codes/name_retrieval/execute_analysis.py').


2. **Policy Document Retrieval**  
- Objective: Assess whether LLM agents retrieve the correct genetic testing coverage policies.  
- Input: Insurance provider name + prompt configuration.  
- Output: Retrieved policy documents (PDF/HTML) + MD5 verification results.  
- Output Location: `results/policy_retrieval/`  
- Evaluation: MD5-based ground-truth comparison ('codes/policy_retrieval/assess.py').

3. **Patient-Policy match**  
- Objective: Retrieve the most relevant policy document for a given synthetic patient case.  
- Input: Synthetic patient case + policy embedding corpus (789 policies).  
- Output: Ranked policy candidates (Top-K) + reranking artifacts.  
- Output Location: `results/patient_policy_match/`  
- Evaluation: Match rate and reranking analysis ('codes/analysis_figures/match_rate_analysis.ipynb').


4. **LLM Agent for Answering Relevant Questions**  
- Objective: Evaluate downstream insurance QA accuracy under document conditioning.  
- Input: Patient case ± policy document.  
- Settings:
  - Baseline (no document)
  - All-Correct (ground-truth document)
  - All-Incorrect (high-similarity incorrect document)
- Output Location: `results/LLM_QnA/`
- Evaluation: Accuracy, Adjusted_Accuracy, case-level statistical analysis between settings, question-wise statistical analysis ('codes/analysis_figures/Analysis.ipynb').

⚠️ The **LLM Agent for Answering Relevant Questions** task depends on the outputs of the  **Patient–Policy Matching** task when running document-conditioned settings  (matched, unmatched, all_correct, all_incorrect).

Therefore, the Patient–Policy Matching task must be executed first 
to generate the required policy-document assignments.

The **Baseline** setting (patient narrative only, without policy documents) can be executed independently.
---

## 📄 Insurance Policy Documents

A total of 789 publicly available genetic testing policy documents  were used for embedding and retrieval experiments.

These documents are not redistributed in this repository 
due to size and licensing considerations.

All policy documents are publicly accessible via the official payer websites:
- Aetna
- Blue Cross Blue Shield Federal Employee Program (BCBS FEP)
- Cigna
- United Healthcare

The experiments were conducted using the policy snapshot available at the time of study.

To reproduce embedding-based experiments:
1. Download the relevant genetic testing policies from payer websites.
2. Place them under a local directory.

Ground-truth md5 mappings between synthetic cases and policy documents
are provided in `dataset/final_ground_truth.json`.

---

## 📊 Evaluation Datasets

All evaluation datasets are located in the `dataset/` folder
- 'In-Network_Providers_Update.csv' for **In-Network Provider Retrieval** task
- 'qna_free_text_sample.json' for patient narrative samples for **Patient-Policy match** and **LLM Agent for Answering Relevant Questions** tasks
- 'final_ground_truth.json' contains evaluation ground truth answer for **Patient-Policy match** and **LLM Agent for Answering Relevant Questions** tasks

---
## 📘 Related Manuscript

This project supports the manuscript titled:

**"Evaluating Large Language Model Agents for Genetic Testing Insurance Workflows: An End-to-End Assessment of Retrieval and Reliability"**

Key contributions:
- Evaluation of real-time LLM-based retrieval
- Task-specific prompting & evaluation metrics
- Assessing LLM agent performance on End-To-End genetic testing insurance workflow
- Quantify failure modes: retrieval sensitivity, abstention rate

---

