import matplotlib.pyplot as plt

# Names of the quantization levels
quantization_levels = ['Q8_0', 'Q5_K_M', 'Q4_K_M', 'Q4_K_S', 'Q3_K_M', 'Q2_K']

# KL Divergence average values for each quantization level
kl_divergence_values = [
    0.0002930254327219267,
    0.0038851341733119322,
    0.008572168991862165,
    0.011575304550243755,
    0.03123956228343069,
    0.05843567209743689
]

# Creating a bar chart with light red bars
light_red = '#FF9999'  # You can use a hexadecimal color code for a specific shade
plt.figure(figsize=(10, 6))
plt.bar(quantization_levels, kl_divergence_values, color=light_red)

# Adding labels and title
plt.xlabel('Quantization Level')
plt.ylabel('KL Token Divergences')
plt.title('13b - Average KL Divergence for token probabilities between different quantizations')

# Adding value labels on top of each bar
for i, value in enumerate(kl_divergence_values):
    plt.text(i, value + 0.001, f'{value:.6f}', ha='center')

# Show grid and the plot
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.show()