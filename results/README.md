# 📊 Insurance Workflow Experiment Results

This folder contains experimental outputs for the evaluating LLM agents for genetic testing insurance workflow.
Raw experiment outputs are organized by iteration for retrieval tasks (name & policy), and QA task while patient-policy matching task stored in configurations.

---

# name_retrieval

Contains results for **insurance payer (in-network provider) retrieval experiments**.

## 📂 Structure
```bash
name_retrieval/
├── final/
│   ├── iteration_1/
│   ├── iteration_2/
│   └── iteration_3/
└── evaluation_results/
```

## 🔹 final/iteration_{#}/

Raw outputs for each experimental iteration.

Each iteration stores:
- Model-specific outputs
  - Prompt-specific results (e.g., baseline, explicit_source)
- Retrieved provider names

These represent the direct outputs of LLM-based payer name generation experiments.

### Directory hierarchy

- **Model level**  
'perplexity', `gpt-4o`, 'gpt-4o-oct', `gpt-5-mini`

- **Prompt level**  
`baseline`, `explicit`

## 🔹 evaluation_results/

Processed evaluation outputs for **payer name retrieval** experiments.
This directory contains analysis-ready tables that summarize performance by
(model × prompt × iteration) and include GPT-4o matching criteria.

---

# policy_retrieval

Contains outputs of **insurance policy document retrieval experiments**.

These experiments evaluate whether LLMs can correctly retrieve official
genetic testing coverage policy documents.

## 📂 Structure
```bash
policy_retrieval/
└── final/
    ├── iteration_1/
    ├── iteration_2/
    ├── iteration_3/
    ├── all_assessments.csv
    ├── all_links.csv
    ├── payer_results.csv
    └── policy_experiment_result.csv
```
---

## 🔹 final/iteration_{#}/

Raw policy retrieval outputs for each independent experiment run.
Each iteration follows a hierarchical structure of model_prompt_payer.


### Directory hierarchy

- **Model level**  
`gpt-4o`, `gpt-5-mini`

- **Prompt level**  
`baseline`, `keyword`, `verified`

- **Insurance provider level**  
`Aetna`, `Blue_Cross_and_Blue_Shield_Federal_Employee_Program`, `Cigna`, `United_Healthcare`

---

### Files within each provider folder

Each provider folder typically contains:

- `*_raw_response.txt`  
  Full raw LLM output for the retrieval query.

- `*_result.json`  
  Structured extraction of the LLM response, including identified links and metadata.

- `downloaded/`  
  Downloaded policy files (PDF or HTML) retrieved during the experiment.

- `downloaded_pdfs.csv`  
  List of downloaded documents with metadata (file name, source URL, status).

- `links_summary.csv`  
  Summary of all retrieved candidate links before filtering or verification.

- `md5_comparison_results.csv` (if applicable)  
  MD5 hash comparison results used to verify document uniqueness and match with ground truth.

---

## 🔹 Aggregated Result Files

The following CSV files summarize results across all iterations:

### all_assessments.csv
Contains detailed assessment records for every experiment run,
including prompt, model, insurance provider, and retrieval outcome.

### all_links.csv
Comprehensive list of all retrieved links across experiments.

### policy_experiment_result.csv
Overall retrieval experiment summary statistics,
used for reporting and manuscript figures.

---

# patient_policy_match

Contains results for **patient-policy matching**.

## 📂 Structure
```bash
results/patient_policy_match/
└── full/
    ├── openai/
    │   ├── header/
    │   │   ├── top1_10retrieve_gpt_5_mini_header_openai_small/
    |   │   │    └── retrieval/
    │   │   │       └── gpt_5_mini/
    │   │   │            └── top1/
    │   │   │                ├── matching_summary.csv
    │   │   │                ├── rank_change_detail.csv
    │   │   │                ├── rerank_orders.csv
    │   │   │                ├── top1_matched_docs.csv
    │   │   │                └── top1_unmatched_docs.csv
    │   │   ├── top3_10retrieve_gpt_5_mini_header_openai_small/
    │   │   ├── top1_30retrieve_gpt_5_mini_header_openai_small/
    │   │   └── top3_30retrieve_gpt_5_mini_header_openai_small/
    │   │
    │   └── policy/
    │       ├── top1_10retrieve_gpt_5_mini_policy_openai_small/
    │       └── top3_10retrieve_gpt_5_mini_policy_openai_small/
    │
    └── ST/
        ├── header/
        │   ├── top1_10retrieve_gpt_5_mini_gpt_5_mini_update/
        │   ├── top3_10retrieve_gpt_5_mini_gpt_5_mini_update/
        │   ├── top1_30retrieve_gpt_5_mini_gpt_5_mini_update/
        │   └── top3_30retrieve_gpt_5_mini_gpt_5_mini_update/
        │
        └── policy/

```

## 🔹 Experimental configurations

Each subfolder corresponds to a **patient–policy matching** run under a specific retrieval + embedding + input setting.

### Naming pattern and Organization

Patient–policy matching results are organized by:

1. **Run mode**: `test/` vs `full/`
2. **Embedding backbone**: `openai/` vs `ST/`
3. **Policy input type**: `header/` (summary) vs `policy/` (full text)

#### 1) SentenceTransformer embedding (baseline embedding backbone)
- `top{k}_{c}retrieve_{rerank_model}_{QA_model}_update`  
  Uses **SentenceTransformer embeddings** with **header (policy summarization) input**.

#### 2) OpenAI embedding (text-embedding-3-small)
- `top{k}_{c}retrieve_{rerank_model}_{input}_openai_small`  
  Uses **OpenAI text-embedding-3-small** with **header (policy summarization) input**.


### Folder contents

Within each configuration, outputs are stored under:

- `retrieval/{rerank_model}/top{k}/`  
  Matching artifacts for the given `top{k}` setting, including:
  - `matching_summary.csv`: aggregate match statistics for the run
  - `rank_change_detail.csv`: rank-change comparison between cosine similarity based ranking and LLM reranking
  - `rerank_orders.csv`: raw results of LLM reranking
  - `top{k}_matched_docs.csv`, `top{k}_unmatched_docs.csv`: matched vs unmatched document selections
  - (optional) `correct_cases.csv`, `incorrect_cases.csv`: case lists for downstream QA (when generated)
  - (optional) `rerank_failed_cases.json`: rerank failure diagnostics

In addition, `whole_policy/` includes:
- `rank_change_summary.csv`: summary of reranking stability across top-k settings
---

# LLM_QnA

Contains results for **insurance coverage Question Answering**.

## 📂 Structure
```bash
LLM_QnA/
└── RAG/
│   └── final/
│   │   └── final_qna_results/
│   │   │   ├── open_ai/
│   │   │   │   ├── gpt_5_mini_gpt_5_mini/
│   │   │   │   │   ├── baseline/
│   │   │   │   │   │   ├── iter1/
│   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   ├── iter2/
│   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   └── iter3/
│   │   │   │   │   │       ├── qna_raw/
│   │   │   │   │   │       ├── batch_id.txt
│   │   │   │   │   │       ├── batch_qna_requests.jsonl
│   │   │   │   │   │       └── results.csv
│   │   │   │   │   ├── rag/
│   │   │   │   │   │   ├── iter1/
│   │   │   │   │   │   │   ├── all_correct/
│   │   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   │   ├── all_incorrect/
│   │   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   ├── iter2/
│   │   │   │   │   │   │   ├── all_correct/
│   │   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   │   ├── all_incorrect/
│   │   │   │   │   │   │   │   ├── qna_raw/
│   │   │   │   │   │   │   │   ├── batch_id.txt
│   │   │   │   │   │   │   │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │   │   │   └── results.csv
│   │   │   │   │   │   └── iter3/
│   │   │   │   │   │      ├── all_correct/
│   │   │   │   │   │      │   ├── qna_raw/
│   │   │   │   │   │      │   ├── batch_id.txt
│   │   │   │   │   │      │   ├── batch_qna_requests.jsonl
│   │   │   │   │   │      │   └── results.csv
│   │   │   │   │   │      └── all_incorrect/
│   │   │   │   │   │         ├── qna_raw/
│   │   │   │   │   │         ├── batch_id.txt
│   │   │   │   │   │         ├── batch_qna_requests.jsonl
│   │   │   │   │   │         └── results.csv
│   │   │   │   │   ├── batch_summary_all_correct_openai.json
│   │   │   │   │   └── batch_summary_all_incorrect_openai.json
│   │   │   ├── ST/
│   │   │   ├── final_all_results_combined.csv
│   │   │   ├── final_file_updated.csv
│   │   │   └── final_results_with_accuracy_updated.csv
```

## 🔹 LLM_QnA Experimental Structure

The `LLM_QnA` module evaluates downstream question-answering performance under different retrieval conditions and embedding backbones.

### Embedding backbones

- `open_ai/`  
  Uses **OpenAI text-embedding-3-small** for patient–policy matching.

- `ST/`  
  Uses **SentenceTransformer embeddings** for patient–policy matching.

For both backbones, the downstream **QnA model remains fixed** (e.g., `gpt-5-mini`).

---
### Experimental modes
Within each model configuration:

#### 1️⃣ Baseline
- No policy document provided.
- The LLM answers based solely on the patient case narrative.
- Represents an LLM-only condition.

Each configuration is repeated:
- iter1
- iter2
- iter3

Each iteration contains:
- `qna_raw/` – raw JSON responses
- `batch_id.txt` – OpenAI batch job identifier
- `batch_qna_requests.jsonl` – submitted requests
- `results.csv` – structured answer extraction

#### 2️⃣ RAG (Documented)
Conducted under two controlled document conditions:

- `all_correct/`  
  Every sample is paired with its **ground-truth policy document**.

- `all_incorrect/`  
  Every sample is paired with a **mismatch policy document** (top-ranked by cosine similarity excluding the ground-truth).

Each configuration is repeated:
- iter1
- iter2
- iter3

Each iteration contains:
- `qna_raw/` – raw JSON responses
- `batch_id.txt` – OpenAI batch job identifier
- `batch_qna_requests.jsonl` – submitted requests
- `results.csv` – structured answer extraction
---

### Batch summaries

- `batch_summary_all_correct_openai.json`
- `batch_summary_all_incorrect_openai.json`

These store metadata for submitted batch jobs across iterations.

---


### Final aggregated outputs

- `final_all_results_combined.csv`  
  Aggregates all iteration-level results across baseline and RAG settings.

- `final_file_updated.csv`  
  Adds count-based summary statistics derived from the combined file.

- `final_results_with_accuracy_updated.csv`  
  Used for final statistical analysis and manuscript tables. Includes computed performance metrics:
  - Accuracy
  - Adjusted Accuracy  

Each row corresponds to **one patient case × QA mode × iteration**.

Key fields include:

| Column | Description |
|------|-------------|
| `case_id` | Unique identifier of the patient case |
| `mode` | QA mode (`baseline` or `rag`) |
| `case_type` | Document condition (`without_policy`, `all_correct`, `all_incorrect`) |
| `iteration` | Experiment iteration (`iter1`, `iter2`, `iter3`) |

For each question **Q0–Q8**, the table stores:

- `Qx_answer` – model prediction  
- `Qx_reasoning` – LLM explanation

Evaluation metrics include:

- `correct`, `total`, `accuracy` – overall QA performance
- `adjusted_correct`, `adjusted_total`, `adjusted_accuracy` – metrics excluding questions where the ground-truth answer is **Not Specified**

Additional diagnostic fields record:

- `wrong_questions`
- `wrong_predictions`
- `ground_truth`
- `unclear_count`
- `not_answerable_count`

These outputs are used for the statistical analysis and figures reported in the manuscript.
---  
@misc{kim2026evaluating,
  title        = {Evaluating Large Language Model Agents for Genetic Testing Insurance Workflows: An End-to-End Assessment of Retrieval and Reliability},
  author       = {Kim, Junyoung and Ravi, Kamalakkannan and Liu, Cong},
  year         = {2026},
  eprint       = {arXiv:XXXX.XXXXX},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  institution  = {Boston Children's Hospital and Harvard Medical School}
}
