import math

# Function to apply temperature to probabilities and normalize them
def apply_temperature(probs, temperature):
    if temperature == 1.0:  # If temperature is 1, return original probabilities
        return probs
    else:
        # Adjust the probabilities using the temperature
        adjusted_probs = [math.pow(p, 1 / temperature) for p in probs]
        # Normalize the adjusted probabilities so they sum up to 1
        sum_adjusted_probs = sum(adjusted_probs)
        normalized_probs = [p / sum_adjusted_probs for p in adjusted_probs]
        return normalized_probs

# Function to read probabilities from file
def read_probabilities_from_file(file_path):
    probabilities = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Extract the probability value and convert to a float
                percentage = float(line.split(': ')[1].replace('%', ''))
                probabilities.append(percentage / 100)  # Convert from percentage to a fraction
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
    return probabilities

# Main function
def main():
    # Read original probabilities from file
    probs = read_probabilities_from_file('prob.txt')
    
    if not probs:
        print('No probabilities found. Exiting.')
        return

    # Ask the user for the temperature
    try:
        temperature = float(input('Please enter a "temperature": '))
    except ValueError:
        print('Invalid input. Please enter a numerical value for temperature.')
        return

    # Apply the temperature to the probabilities
    temp_probs = apply_temperature(probs, temperature)

    # Print the adjusted probabilities
    print('Adjusted Probabilities with Temperature {}:'.format(temperature))
    for i, temp_prob in enumerate(temp_probs, start=1):
        print('Token {}: {:.2f}%'.format(i, temp_prob * 100))

if __name__ == "__main__":
    main()