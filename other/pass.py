import random
import string
import sys
import os

class PasswordGenerator:
    def generate_random_password(length=int(random.randint(18, 25))):
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
        # Make sure to include at least one character from each set
        shuffled_characters.extend([random.choice(uppercase_letters), random.choice(lowercase_letters), random.choice(digits), random.choice(special_characters)])
        # Create the final password by joining the shuffled characters
        password = ''.join(shuffled_characters)
        
        return password

    # Function to save the history of generated passwords to a file in the same directory as current script
    def save_password_to_file(password):
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        # Change the directory to the script directory
        os.chdir(script_dir)
        # Save the password to the file
        with open("passwords.txt", "a") as file:
            file.write(password + "\n")

    if __name__ == "__main__":
        # Generate a random password with a default length of 12 characters
        password = generate_random_password()
        print("Random Password:", password)
        # Save the generated password to a file
        save_password_to_file(password)
        print("Password saved to file.")

class PasswordGeneratorv2:
    def generate_random_password(length=12, include_uppercase=True, include_digits=True, include_special_chars=True):
        """
        Generate a random password.

        Parameters:
        - length (int): Length of the password. Default is 12.
        - include_uppercase (bool): Whether to include uppercase letters. Default is True.
        - include_digits (bool): Whether to include digits. Default is True.
        - include_special_chars (bool): Whether to include special characters. Default is True.

        Returns:
        - str: Generated password.
        """
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase if include_uppercase else ''
        digits = string.digits if include_digits else ''
        special = string.punctuation if include_special_chars else ''

        all_chars = lower + upper + digits + special

        if not all_chars:
            raise ValueError("At least one character set must be enabled")

        password = ''.join(random.choice(all_chars) for _ in range(length))
        return password
