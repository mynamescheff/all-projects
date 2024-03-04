from flask import Flask, request, jsonify

# Assuming ollama is accessible via HTTP locally
import requests

class Village:
    def __init__(self, name):
        self.name = name
        self.residents = []

    def add_resident(self, person):
        self.residents.append(person)
        print(f"{person.name} has moved into {self.name}.")

    def list_residents(self):
        return [person.name for person in self.residents]

class Person:
    def __init__(self, name, background):
        self.name = name
        self.background = background  # New attribute for background information

    def speak(self, words):
        # Function to simulate communication with ollama, simplified here
        return f"{self.name} says: '{words}'"
    
def print_dialogues(village):
    for person in village.residents:
        # Example dialogue generation (replace with actual model communication)
        dialogue = person.speak(f"Hello, I am {person.name}. {person.background}")
        print(dialogue)
        
        # Wait for user input to continue or quit
        print("\nPress Enter to continue to the next person, or type 'q' and press Enter to quit.")
        user_input = input()
        if user_input.lower() == 'q':
            print("Exiting dialogue.")
            break

# Function to communicate with the OLLaMa model
def communicate_with_ollama(name, words):
    url = 'http://127.0.0.1:11434' # OLLaMa model endpoint
    payload = {
        'name': name,
        'words': words,
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # Assuming the model returns a JSON with a 'response' key
            return response.json().get('response', "No response received")
        else:
            return f"Error from OLLaMa: {response.status_code}"
    except Exception as e:
        return f"Failed to communicate with OLLaMa: {e}"


    
app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    person_name = data.get("name")
    message = data.get("message")

    # Initialize the village and its residents with background information
    my_village = Village("Greenwood")
    alice = Person("Alice", "I'm a gardener and love to take care of plants.")
    bob = Person("Bob", "I enjoy crafting wooden furniture.")

    my_village.add_resident(alice)
    my_village.add_resident(bob)

    # Assuming this is called at some point to print dialogues
    print_dialogues(my_village)


if __name__ == '__main__':
    app.run(debug=True)
