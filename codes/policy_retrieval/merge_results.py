import os
import pandas as pd

def merge_results(result_base_dir, assessment_output, links_output, models=None, prompt_types=None, payers=None, iterations=None):
    '''Merge results from multiple iterations, models, prompt types, and payers into consolidated CSV files'''

    models = models or ["gpt-4o", "gpt-5-mini"]
    prompt_types = prompt_types or ["baseline", "keyword", "verified"]
    payers = payers or ["United Healthcare", "Aetna", "Cigna", "Blue Cross and Blue Shield Federal Employee Program"]
    iterations = iterations or range(1, 4)

    assessment_results = []
    links_results = []
    
    for iteration in iterations:
        for model in models:
            for prompt_type in prompt_types:
                for payer in payers:
                    exp_dir = os.path.join(result_base_dir, f"iteration_{iteration}", model, prompt_type, payer.replace(" ", "_"))
                    
                    assessment_csv = os.path.join(exp_dir, "md5_comparison_results.csv")
                    if os.path.exists(assessment_csv):
                        df = pd.read_csv(assessment_csv)
                        df['model'] = model
                        df['prompt_type'] = prompt_type
                        df['iteration'] = iteration
                        assessment_results.append(df)
                    
                    links_csv = os.path.join(exp_dir, "links_summary.csv")
                    if os.path.exists(links_csv):
                        df = pd.read_csv(links_csv)
                        df['model'] = model
                        df['prompt_type'] = prompt_type
                        df['iteration'] = iteration
                        links_results.append(df)
    
    if assessment_results:
        pd.concat(assessment_results, ignore_index=True).to_csv(assessment_output, index=False)
        print(f"Merged assessment results saved to {assessment_output}")
    else:
        print("No assessment results found to merge.")

    if links_results:
        pd.concat(links_results, ignore_index=True).to_csv(links_output, index=False)
        print(f"Merged links results saved to {links_output}")
    else:
        print("No links results found to merge.")