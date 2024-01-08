import random
import string

def generate_random_password(length=12):
    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*()_+[]{}|;:,.<>?'

    # Create a list containing characters from all sets
    all_characters = list(uppercase_letters + lowercase_letters + digits + special_characters)

    # Shuffle the characters in a custom way
    random.shuffle(all_characters)
    shuffled_characters = all_characters[:length]

    # Create the final password by joining the shuffled characters
    password = ''.join(shuffled_characters)
    
    return password

if __name__ == "__main__":
    # Generate a random password with a default length of 12 characters
    password = generate_random_password()
    print("Random Password:", password)
