import numpy as np

def read_probabilities(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split("\n\n")
    
    distributions = []
    for block in content:
        lines = block.strip().split("\n")[1:]
        distribution = {}
        for line in lines:
            if ":" not in line:
                continue

            token_id_str, prob_str = line.split(':')
            token_id = int(token_id_str.split(' ')[2])
            prob = float(prob_str.replace('%', ''))
            distribution[token_id] = prob/100  # Convert percentage to probability
        distributions.append(distribution)

    return distributions

def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def normalize(distribution):
    total = sum(distribution.values())
    return {k: v / total for k, v in distribution.items()}

def get_top_n_tokens(distribution, n=32000):
    return dict(sorted(distribution.items(), key=lambda item: item[1], reverse=True)[:n])

def compute_kl_divergence_for_top_tokens(fp16_distribution, other_distribution):
    top_fp16_tokens = get_top_n_tokens(fp16_distribution)  
    matched_other_tokens = {token_id: other_distribution.get(token_id, 0) for token_id in top_fp16_tokens.keys()}
    
    top_fp16_probabilities = normalize(top_fp16_tokens)
    matched_other_probabilities = normalize(matched_other_tokens)

    p_fp16 = np.array(list(top_fp16_probabilities.values()), dtype=np.float64)
    q_other = np.array([matched_other_probabilities[token_id] for token_id in top_fp16_probabilities.keys()], dtype=np.float64)
    
    kl_div = kl_divergence(p_fp16, q_other)
    return kl_div

def main():
    fp16_filename = '13b_redux_logit_analysis_fp16_32000.txt'
    fp16_probs = read_probabilities(fp16_filename)
    
    other_filenames = [
        '13b_redux_logit_analysis_q8_0_32000.txt',
        '13b_redux_logit_analysis_q5_K_M_32000.txt',
        '13b_redux_logit_analysis_q4_K_M_32000.txt',
        '13b_redux_logit_analysis_q4_K_S_32000.txt',
        '13b_redux_logit_analysis_q3_K_M_32000.txt',
        '13b_redux_logit_analysis_q2_K_32000.txt'
    ]
    
    for other_filename in other_filenames:
        other_probs = read_probabilities(other_filename)

        if len(fp16_probs) != len(other_probs):
            print(f"Mismatch in number of distributions between {fp16_filename} and {other_filename}")
            continue

        kl_divs = [compute_kl_divergence_for_top_tokens(d_fp16, d_other) for d_fp16, d_other in zip(fp16_probs, other_probs)]
        max_kl_divs = sorted(kl_divs, reverse=True)[:4]  # Sort in descending order and take the top 19 KL divergences
        avg_top_19_kl_div = np.mean(max_kl_divs)  # Average of the top 19 highest KL divergences
        
        avg_kl_div = np.mean(kl_divs)

        print(f"Average KL divergence between {fp16_filename} and {other_filename}: {avg_kl_div}")
        print(f"Average of top 19 highest KL divergences between {fp16_filename} and {other_filename}: {avg_top_19_kl_div}")

if __name__ == '__main__':
    main()