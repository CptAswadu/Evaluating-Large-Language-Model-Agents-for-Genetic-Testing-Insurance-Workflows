import os
from compare_md5 import compare_md5
from merge_results import merge_results
import pandas as pd

def main():
    TEST_MODE = True

    # set the base directory for results and existing PDFs
    existing_pdfs_base_dir = "../dataset/policy_ret"
    payer_mapping = {
        "United Healthcare": "United Healthcare",
        "Aetna": "Aetna",
        "Cigna": "Cigna",
        "Blue Cross and Blue Shield Federal Employee Program": "BCBS FEP"
    }

    if TEST_MODE:
        result_base_dir = "../results/policy_retrieval/test"
        run_payers = ['Blue Cross and Blue Shield Federal Employee Program']
        run_models = ['gpt-5-mini']
        run_prompt = ['verified']
        run_iterations = [1]
    else:
        result_base_dir = "../results/policy_retrieval/final"
        run_payers = ["United Healthcare", "Aetna", "Cigna", "Blue Cross and Blue Shield Federal Employee Program"]
        run_models = ["gpt-4o", "gpt-5-mini"]
        run_prompt = ["baseline", "keyword", "verified"]
        run_iterations = [1, 2, 3]
    

    for iteration in run_iterations:
        for model in run_models:
            for prompt_type in run_prompt:
                for payer in run_payers:
                    exp_dir = os.path.join(result_base_dir, f"iteration_{iteration}", model, prompt_type, payer.replace(" ", "_"))
                    downloaded_csv = os.path.join(exp_dir, "downloaded_pdfs.csv")
                    output_csv = os.path.join(exp_dir, "md5_comparison_results.csv")
                    
                    if os.path.exists(downloaded_csv):
                        try:
                            df_check = pd.read_csv(downloaded_csv)
                            if df_check.empty:
                                print(f"skipped (no data): {downloaded_csv}")
                            else:
                                compare_md5(downloaded_csv, existing_pdfs_base_dir, output_csv, payer_mapping)
                        except pd.errors.EmptyDataError:
                            print(f"skipped (empty): {downloaded_csv}")
                    else:
                        print(f"skipped (not found): {exp_dir}")
                        

    merge_results(result_base_dir, os.path.join(result_base_dir, "all_assessments.csv"), os.path.join(result_base_dir, "all_links.csv"), models=run_models, prompt_types=run_prompt, payers=run_payers, iterations=run_iterations)

if __name__ == "__main__":
    main()