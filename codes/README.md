# Code Structure

This directory contains modular implementations of the experimental components used in the LLM-based insurance workflow study for genetic testing.

Each task is executed via a dedicated entry script.  
All other Python files within each module serve as internal utilities (data loading, parsing, scoring, aggregation, etc.).

For policy retrieval task assessment, patient-policy match and QA task with document settings please store policy document first and set the directory.

---

## 🔹 Entry Scripts (One per Task)

| Stage | Task | Entry Script | Description | Outputs |
|-------|------|--------------|-------------|---------|
| Stage 1 | Payer name retrieval | `name_retrieval/experiment.py` | LLM-based payer identification experiments | `results/name_retrieval/` |
| Stage 2 | Policy document retrieval | `policy_retrieval/experiment.py` | Policy link retrieval + MD5 verification | `results/policy_retrieval/` |
| Stage 3 | Patient–policy matching (ST + header) | `patient_policy_match/header_execute.py` | SentenceTransformer embedding + summarized policy input | `results/patient_policy_match/full/ST/header` |
| Stage 3 | Patient–policy matching (ST + whole policy) | `patient_policy_match/whole_policy_execute.py` | SentenceTransformer embedding + full policy text | `results/patient_policy_match/full/ST/policy` |
| Stage 3 | Patient–policy matching (OpenAI embedding) | `patient_policy_match/policy_openai.py` | OpenAI text-embedding-3-small + header/whole-policy input | `results/patient_policy_match/full/openai` |
| Stage 4 | Insurance QA Evaluation (OpenAI backbone) | `rag_qna/openai_embedding.py` | Executes structured insurance QA (Q0–Q8) under document-conditioning settings (Baseline (no document), all_correct, all_incorrect) using Text-embedding-3-small embedding based patient-policy matching (match/unmatch) results. This configuration is used in the manuscript. | `results/LLM_QnA/RAG/final/final_qna_results/open_ai` |
| Stage 4 | Insurance QA Evaluation (ST backbone) | `rag_qna/ST_embedding_qna.py` |Executes structured insurance QA (Q0–Q8) under document-conditioning settings (Baseline (no document), all_correct, all_incorrect) using SentenceTransformer embedding based patient-policy matching (match/unmatch) results.  | `results/LLM_QnA/RAG/final/final_qna_results/ST` |

### QA Document Conditioning Strategy

The QA module does not perform retrieval itself.  
Instead, it consumes previously generated patient–policy matching results and evaluates downstream QA performance under controlled document-conditioning scenarios: 

- **Baseline**  
  Patient narrative only (no policy document).

- **Matched**  
  The policy document retrieved by the patient–policy matching pipeline
  when the retrieved document matches the ground-truth policy.  

- **Unmatched**  
  The policy document retrieved by the patient–policy matching pipeline
  when the retrieved document does not match the ground-truth policy.  

- **All Correct**  
  Oracle condition where the ground-truth policy document is always provided.  

- **All Incorrect**  
  Adversarial condition where a high-similarity but incorrect policy document is provided for every case (excluding the ground truth).  

---
## 🔹 Configuration (Policy Document Directory)

For tasks that require policy documents (Policy Retrieval Assessment, Patient–Policy Matching, and QA with document conditioning), policy documents must be stored locally and the directory path must be set correctly before running the scripts.

- The scripts expect a local directory containing the policy documents.
- Please update the policy document directory path in the corresponding scripts before execution.  
---  

## 🔹 SentenceTransformer Model Download

The patient–policy matching module uses SentenceTransformer models
(`all-MiniLM-L6-v2`) from Hugging Face.  

⚠️ **Important**

- During the **first execution**, the model files must be downloaded
  from the Hugging Face Hub.  
- Therefore, the following offline settings **must NOT be enabled** during the first run.  

```python
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
```  
Once the model has been downloaded and cached locally, the experiments
can be executed in offline mode by enabling these variables if desired.

This ensures that subsequent runs rely only on locally cached models
without accessing external servers.  
---  
## 🔹 Test Mode (Execution Setting)

Several entry scripts are configured with a **test mode**.  
```python
TEST_MODE = True
```  
If the setting is test mode, the script runs only a single sample case to verify that the pipeline works correctly.  

To run the full experiment used in the manuscript, this setting must be changed to:  
```python
TEST_MODE = False
```  
---  

> ⚠️ **Note**
>
> - Tasks **3 (Patient–Policy Match)** and **4 (LLM QA)** were executed using **GPT-5-Mini** in the experiments reported in the manuscript.
> - Some paths and configurations are **hardcoded for the GPT-5-Mini setup**.
> - If you use a different LLM or modify the experiment configuration, please adjust the relevant paths and model settings accordingly.
---

## 🔹 Run Examples

From the repository root:
```bash
cd codes
```

### 1️⃣ In-network provider retrieval
Experiment
```bash
python name_retrieval/experiment.py
```
Assessment (LLM (GPT-4o) Judge)
```bash
python name_retrieval/execute_analysis.py
```

### 2️⃣ Policy document retrieval
```bash
python policy_retrieval/experiment.py
```
Assessment  
(Please store policy documents first and set the directory.)
```bash
python policy_retrieval/assess.py
```

### 3️⃣ Patient–policy matching
Experiment and Assessment  
(Please store policy documents first and set the directory.)

Each file contains both experiment and assessment.  



SentenceTransformer (header input):
```bash
python patient_policy_match/header_execute.py
```

SentenceTransformer (whole-policy input):
```bash
python patient_policy_match/whole_policy_execute.py
```

OpenAI embedding (text-embedding-3-small):
```bash
python patient_policy_match/policy_openai.py
```

### 4️⃣ LLM QA (used in manuscript)
Experiment 
```bash
python rag_qna/openai_embedding.py
```
Assessment
1. Aggregate results
```bash
python rag_qna/aggregate.py
```

2. Calculate accuracy
```bash
python rag_qna/final_accuracy_calculation.py
```
---

## 🔹 Module Overview

### 1️⃣ name_retrieval/

Implements payer identification experiments.

Responsibilities include:
- Provider name extraction
- GPT-4o Judge
- Log parsing and preprocessing
- Experimental execution scripts

This module evaluates whether LLM agents can correctly identify in-network insurance providers.

---

### 2️⃣ policy_retrieval/

Implements policy document retrieval pipelines.

Core components:
- Policy document acquisition (PDF download and loading)
- Prompt-based retrieval experiments
- Experimental execution control
- Retrieval result aggregation and merging
- MD5-based document comparison and verification
- Retrieval performance assessment

This module evaluates retrieval correctness and document alignment.

---

### 3️⃣ patient_policy_matching/

Implements the policy–patient alignment and retrieval evaluation (RAG).

This module performs:
- Candidate policy retrieval
- Embedding-based ranking
- LLM-based reranking
- Whole-policy/Summarized (Header) input execution
- Retrieval result aggregation
- MD5-based document verification
- Match-rate computation and analysis


It quantifies retrieval correctness under different configurations
(e.g., Top-K, Top-C, LLM reranked rank, cosine similarity rank, whole-policy execution).

---

### 4️⃣ rag_qna/

Implements the full structured Q0–Q8 evaluation pipeline.

This module includes:
- Baseline QA execution (patient narrative only)
- Documented QA (patient narrative + policy documents)
- Batch execution and result management
- JSON-to-CSV merging utilities
- Final accuracy and adjusted accuracy calculation

This module evaluates downstream decision quality under different document-conditioning settings.

---

### 5️⃣ analysis_figures/

Contains statistical analysis (QA only), patient-policy match analysis and figure generation scripts used in manuscript preparation.
- `Analysis.ipynb`  
  QA task statistical anlysis

- `final_figures.ipynb`  
  Figures for the manuscript

- `match_rate_analysis.ipynb`  
  patient-policy match task statistical anlysis

---

## 🔹 Utility Scripts

- `qna_sample_generation.py`  
  Generates synthetic QA patient samples and ground-truth annotations.

- `batch_check.py`  
  Performs batch checks across experimental outputs and download the results.

- `benchmark_update.ipynb`  
  Used to update patient samples and ground-truth annotations from the initial generation.  
  Additional manual modifications were performed based on this notebook.

---
