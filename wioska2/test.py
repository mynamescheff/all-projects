import random
import time

# Load the pre-trained model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Define some villagers with their names, personalities, and initial topics
villagers = [
    {"name": "Jan", "personality": "curious", "topic": "weather"},
    {"name": "Maria", "personality": "outgoing", "topic": "gossip"},
    {"name": "Piotr", "personality": " analytical", "topic": "science"}
]

# Define a function to generate a response from a villager
def generate_response(villager):
    input_text = f"{villager['name']} is talking about {villager['topic']}."
    output_text = model.generate(input_text, max_length=50)
    return output_text.strip()

# Define a function to advance the conversation between two villagers
def advance_conversation(villager1, villager2):
    # Get the current topics of the two villagers
    topic1 = villager1["topic"]
    topic2 = villager2["topic"]

    # Generate responses from each villager based on their current topic
    response1 = generate_response(villager1)
    response2 = generate_response(villager2)

    # Update the topics of the two villagers based on their responses
    if "weather" in response1 and "science" in response2:
        villager1["topic"] = "environmental science"
        villager2["topic"] = "atmospheric studies"
    elif "gossip" in response1 and "curiosity" in response2:
        villager1["topic"] = "sociology"
        villager2["topic"] = "anthropology"

    # Print the responses and update the conversation state
    print(f"{villager1['name']}: {response1}")
    print(f"{villager2['name']}: {response2}")

# Initialize the conversation state
current_villagers = random.sample(villagers, 2)
print("Initial Conversation:")
for villager in current_villagers:
    print(f"{villager['name']}: {generate_response(villager)}")

# Define a button press event handler to advance or stop the conversation
def button_press(event):
    if event == "advance":
        advance_conversation(*current_villagers)
    elif event == "stop":
        print("Conversation stopped.")

# Start the conversation loop
while True:
    user_input = input("Press 'advance' to continue the conversation, or 'stop' to stop it: ")
    button_press(user_input)

    if user_input == "stop":
        break

print("Conversation ended.")