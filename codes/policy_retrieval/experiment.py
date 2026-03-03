import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from download_pdf import download_pdf, calculate_md5
from prompt import prompt_functions
from policy_retrieval import clean_json_response, query_llm_for_payers
from process_pdf import count_links, process_pdf

def main():
    DOTENV_PATH = '../'
    load_dotenv(dotenv_path=os.path.join(DOTENV_PATH, ".env"))
    openai_api_key = os.getenv("OPEN_AI_API_KEY")
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    chatgpt_agent = OpenAI(api_key=openai_api_key)

    # Test mode with only one case to verify the pipeline, set to False for full experiment
    TEST_MODE = True

    payers = ["United Healthcare", "Aetna", "Cigna", "Blue Cross and Blue Shield Federal Employee Program"]
    models = ["gpt-4o", "gpt-5-mini"]
    prompt_types = ["baseline", "keyword", "verified"]

    # test mode
    if TEST_MODE:
        result_base_dir = "../results/policy_retrieval/test" 
        run_iterations = [1]
        run_payers = ['Blue Cross and Blue Shield Federal Employee Program']
        run_models = ['gpt-5-mini']
        run_prompt = ['verified']
        
    else:
        result_base_dir = "../results/policy_retrieval/final"
        run_iterations = [1, 2, 3]
        run_payers = payers
        run_models = models
        run_prompt = prompt_types

    os.makedirs(result_base_dir, exist_ok=True)
    
    for iteration in run_iterations:
        for openai_model in run_models:
            for pt in run_prompt:
                for payer in run_payers:
                    print(f"Running: iter={iteration}, model={openai_model}, prompt={pt}, payer={payer}")
                    query_llm_for_payers(
                        payer_name=payer,
                        prompt_type=pt,
                        model="openai",
                        openai_model=openai_model,
                        iteration=iteration,
                        base_output_dir=result_base_dir,
                        openai_client=chatgpt_agent
                    )

                    result_file = os.path.join(result_base_dir, f"iteration_{iteration}", openai_model, pt, payer.replace(" ", "_"), f"{payer}_result.json")
                    count_links(result_file)
                
                    save_dir = os.path.dirname(result_file)
                    process_pdf(result_file, os.path.join(save_dir, "downloaded"), os.path.join(save_dir, "downloaded_pdfs.csv"))

                    print(f"Iteration {iteration}, {pt}, {payer} completed!")

if __name__ == "__main__":
    main()