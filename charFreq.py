import string

# Define function to get character frequency
def get_char_frequency(text):
    # Create a dictionary to store the frequency of each character
    char_freq = {}
    
    # Iterate over each character in the text
    for char in text:
        # Ignore non-alphabetic characters
        if char.isalpha():
            # Convert character to lowercase
            char = char.lower()
            
            # Increment the frequency of the character in the dictionary
            char_freq[char] = char_freq.get(char, 0) + 1
    
    # Return the character frequency dictionary
    return char_freq

# Read text file and get character frequency
with open('actualTest.txt', 'r') as f:
    text = f.read()
    char_freq = get_char_frequency(text)

# Calculate total character count
total_chars = sum(char_freq.values())

# Normalize character frequency
norm_char_freq = {char: count/total_chars for char, count in char_freq.items()}

# Print normalized character frequency
for char in sorted(norm_char_freq):
    print(char, norm_char_freq[char])
