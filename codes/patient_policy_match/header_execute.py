import json
import os
import pandas as pd
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from load_policy import load_policies, calculate_pdf_md5
from embedding_policies import embed_policies_from_headers
from retrieve_candidates import retrieve_candidates, cosine_topk
from rerank_policies import rerank_policies
from md5_matching import md5_match_by_rerank_order
from run_retrieval import run_retrieval_evaluation
from run_retrieval_whole import run_retrieval_evaluation_whole

def main():
    # Test mode with only one case to verify the pipeline, set to False for full experiment
    TEST_MODE = True
    TEST_CASE_ID = "Case10917"

    DOTENV_PATH = '../'
    load_dotenv(dotenv_path=os.path.join(DOTENV_PATH, ".env"))
    openai_api_key = os.getenv("OPEN_AI_API_KEY")
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    chatgpt_agent = OpenAI(api_key=openai_api_key)

# set the directory paths for dataset and results
    BASE_DIR = "../dataset"
    DATASET_PATH = f"{BASE_DIR}/qna_free_text_sample.json"
    POLICY_FOLDER = f"{BASE_DIR}/policy_answer" if TEST_MODE else f"{BASE_DIR}/insurance_policy"
    RESULTS_BASE = "../results/patient_policy_match/test/ST/header" if TEST_MODE else "../results/patient_policy_match/full/ST/header"
    os.makedirs(RESULTS_BASE, exist_ok=True)


    if TEST_MODE:
        # only run the retrieval and reranking for a specific test case, to verify the correctness of the pipeline and debug if necessary
        K_RETRIEVAL_HEADER = [10]
        K_RERANK_LIST = [1]
        RETRIEVAL_MODELS = ["gpt-5-mini"]
    else:
        # whole experiment parameters
        K_RETRIEVAL_HEADER = [10, 30]
        K_RERANK_LIST = [1, 3]
        RETRIEVAL_MODELS = ["gpt-5-mini"]

    if TEST_MODE:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            full_dataset = json.load(f)

        test_dataset = [c for c in full_dataset if str(c["id"]) == TEST_CASE_ID]
        TEST_DATASET_PATH = f"{BASE_DIR}/_test_single_case.json"

        with open(TEST_DATASET_PATH, "w", encoding="utf-8") as f:
            json.dump(test_dataset, f, indent=2, ensure_ascii=False)

        print(f"TEST MODE: Using single case {TEST_CASE_ID}")
    else:
        TEST_DATASET_PATH = DATASET_PATH

    cache_suffix = "ST_header_test" if TEST_MODE else "ST_header"

    policies, md5s, headers = load_policies(POLICY_FOLDER)

    embeddings_header, doc_names_header, embedding_matrix_header = embed_policies_from_headers(
        headers=headers,
        md5s=md5s,
        cache_dir= BASE_DIR,
        embedder_id="all-MiniLM-L6-v2",
        cache_suffix=cache_suffix
    )
    
    for K_RETRIEVAL in K_RETRIEVAL_HEADER:
        for K_RERANK in K_RERANK_LIST:

            # Define save directory for this configuration, the model before _update is for model for QA task
            SAVE_BASE_DIR = (
                f"{RESULTS_BASE}/"
                f"top{K_RERANK}_{K_RETRIEVAL}retrieve_"
                f"{RETRIEVAL_MODELS[0].replace('-','_')}_gpt_5_mini_update"
            )
            os.makedirs(SAVE_BASE_DIR, exist_ok=True)
            os.makedirs(f"{SAVE_BASE_DIR}/retrieval", exist_ok=True)

            run_retrieval_evaluation(
                dataset_path=TEST_DATASET_PATH,
                base_dir=SAVE_BASE_DIR,
                embedding_matrix=embedding_matrix_header,
                doc_names=doc_names_header,
                headers=headers,
                md5s=md5s,
                llm_models=RETRIEVAL_MODELS,
                openai_client=chatgpt_agent,
                perplexity_api_key=perplexity_api_key,
                top_k_values=[K_RERANK],
                k_retrieval=K_RETRIEVAL,
                embedder_id="all-MiniLM-L6-v2"
            )

if __name__ == "__main__":
    main()



