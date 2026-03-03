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

    result_base_dir = "../results/policy_retrieval/final"
    os.makedirs(result_base_dir, exist_ok=True)

    # Define the payers, model, and prompt types for the whole experiment
    # payers = ["United Healthcare", "Aetna", "Cigna", "Blue Cross and Blue Shield Federal Employee Program"]
    model = "openai"
    openai_model = "gpt-4o"
    # prompt_type = ["baseline", "keyword", "verified"]
    
    # sample execution for one iteration, one prompt type, and one payer
    prompt_type = "verified"
    payer = "Blue Cross and Blue Shield Federal Employee Program"
    iteration = 3

    query_llm_for_payers(
        payer_name=payer,
        prompt_type=prompt_type,
        model=model,
        openai_model=openai_model,
        iteration=iteration,
        base_output_dir=result_base_dir,
        openai_client=chatgpt_agent
    )

    result_file = os.path.join(result_base_dir, f"iteration_{iteration}", openai_model, prompt_type, payer.replace(" ", "_"), f"{payer}_result.json")
    count_links(result_file)

    save_dir = os.path.dirname(result_file)
    process_pdf(result_file, os.path.join(save_dir, "downloaded"), os.path.join(save_dir, "downloaded_pdfs.csv"))
    print(f"Iteration {iteration}, {prompt_type}, {payer} completed!")

    # Whole experiment execution (uncomment to run the full experiment)
    # for iteration in range(1, 4):
    #     for pt in prompt_type:
    #         for payer in payers:
    #             result = query_llm_for_payers(
    #                 payer_name=payer,
    #                 prompt_type=pt,
    #                 model=model,
    #                 openai_model=openai_model,
    #                 iteration=iteration,
    #                 base_output_dir=result_base_dir,
    #                 openai_client=chatgpt_agent
    #             )

    #             result_file = os.path.join(result_base_dir, f"iteration_{iteration}", openai_model, pt, payer.replace(" ", "_"), f"{payer}_result.json")
    #             count_links(result_file)
                
    #             save_dir = os.path.dirname(result_file)
    #             process_pdf(result_file, os.path.join(save_dir, "downloaded"), os.path.join(save_dir, "downloaded_pdfs.csv"))

    #             print(f"Iteration {iteration}, {pt}, {payer} completed!")

if __name__ == "__main__":
    main()