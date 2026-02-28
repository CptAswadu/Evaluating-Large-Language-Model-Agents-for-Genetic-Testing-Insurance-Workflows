# Evaluating LLM Agents for Genetic Testing Insurance Workflows 

This folder contains structured evaluation datasets used in the LLM-based insurance workflow study.

⚠️ Insurance policy documents used for embedding and retrieval experiments are not included in this repository.

---

## 🔁 Reproducibility Notes for Dataset Files

- All ground-truth mappings correspond to the policy snapshot available at the time of study.
- Insurance policy documents are publicly available but are not redistributed in this repository.
- MD5-based verification files (`policy_md5.csv`, `policy_retrieval_md5.csv`) ensure document identity consistency during retrieval evaluation.
- QA document-conditioning files (e.g., `match_qa.csv`) must be generated after running the Patient–Policy Matching task.
- No protected health information (PHI) is included.

The files in this folder support two core evaluation components:

1. **Payer Identification**
   - Benchmarking LLM agent ability to retrieve in-network insurance providers.

2. **QA Evaluation**
   - Structured Q0–Q8 evaluation over synthetic patient cases.

---

## 📊 Core Evaluation Datasets

### 🔹 final_ground_truth.json
Final validated ground-truth annotations used for patient-policy match and LLM insurance QA evaluation.

### 🔹 filtered_ground_truth.json
Initial downsampling version of the ground truth.

### 🔹 filtered_llm_samples.json
LLM-generated synthetic patient narrative samples based on filtered_ground_truth.

---

## 🧬 Patient Case Datasets

### 🔹 Insurance_Genetic_Testing_QA_Updated.json
Structured evaluation schema defining the nine-question (Q0–Q8) framework used for policy-grounded insurance coverage assessment.

This file specifies:
- Question identifiers (Q0–Q8)
- Full question text
- Standardized answer options for each question

It serves as the evaluation template for structured QA experiments.

### 🔹 qna_free_text_sample.json
Final synthetic patient narratives used for patient-policy match and LLM insurance QA experiment.

---

## 🏥 Payer Dataset

### 🔹 In-Network_Providers_Update.csv
Curated list of in-network insurance providers for GeneDx.

Used as a ground-truth for benchmarking name retrieval accuracy.

---

## 📑 Policy document information

### 🔹 policy_md5.csv
Contains file name and md5 information for all policy documents.

### 🔹 policy_retrieval_md5.csv
Contains the initial ground-truth records for the policy document retrieval task, including payer name, file name, and MD5 hash information. For Aetna, HTML content information is provided instead of an MD5 hash.

### 🔹 match_qa.csv
Contains document assignment information for each synthetic case, including case_id, payer, genetic_test, file name, and MD5 hash. This file is used for both the Patient–Policy Match and the LLM insurance QA tasks.

---

## 🧩 Category Harmonization and Stratified Evaluation

Due to heterogeneous terminology across insurance policies, 
clinical indication (Q3) and family history criteria (Q5) were 
normalized into standardized high-level categories.

To achieve this:

1. Insurance-specific criteria were mapped into unified categories.
2. Category mappings were aligned across:
   - Insurance provider
   - Genetic test type
   - Clinical indication group

### Intermediate Category Files

- `cat_ind_q3.csv`
- `cat_test_ins_q3.csv`
- `cat_ind_q5.csv`
- `cat_test_ins_q5.csv`

These files contain normalized category mappings prior to integration.

### Final Merged Files

- `q3_merged.csv`
- `q5_merged.csv`

These files were generated via outer joins between:
- Retrieval outputs
- Ground-truth annotations
- Standardized category mappings

The merged datasets serve as canonical master tables used for:

- QA sample generation
- Structured Q0–Q8 ground-truth construction

---