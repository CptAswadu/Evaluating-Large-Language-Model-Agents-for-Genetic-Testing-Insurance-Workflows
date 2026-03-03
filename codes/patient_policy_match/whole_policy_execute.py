import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from load_policy import load_policies, calculate_pdf_md5
from embedding_policies import embed_policies_from_headers
from rerank_whole import rerank_whole_policies
from calculate_match_rate import calculate_match_rate
from md5_matching import md5_match_by_rerank_order
from retrieve_candidates import retrieve_candidates
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
    POLICY_FOLDER = f"{BASE_DIR}/insurance_policy"

    save_dir = "../results/patient_policy_match/whole_policy"
    os.makedirs(save_dir, exist_ok=True)

    if TEST_MODE:
        # only run the retrieval and reranking for a specific test case, to verify the correctness of the pipeline and debug if necessary
        K_RERANK_LIST = [1]
    else:
        # whole experiment parameters
        K_RERANK_LIST = [1, 3]

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

    policies, md5s, headers = load_policies(POLICY_FOLDER)

    embeddings, doc_names, embedding_matrix = embed_policies_from_headers(
        headers=policies,
        md5s=md5s,
        cache_dir= save_dir,
        embedder_id="all-MiniLM-L6-v2",
        cache_suffix="whole_policy"
    )

    # only 10 policies for reranking possible, since the whole policy text is much longer than header
    run_retrieval_evaluation_whole(
        dataset_path=TEST_DATASET_PATH,
        base_dir=save_dir,
        embedding_matrix=embedding_matrix,
        doc_names=doc_names,
        policies=policies,
        md5s=md5s,
        openai_client=chatgpt_agent, 
        perplexity_api_key=perplexity_api_key,
        llm_models=['gpt-5-mini'],
        top_k_values= K_RERANK_LIST,
        k_retrieval=10,
        embedder_id="all-MiniLM-L6-v2"
    )

if __name__ == "__main__":
    main()