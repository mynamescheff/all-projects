from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    person_name = data.get("name")
    message = data.get("message")

    # Find the person in the village
    person = next((p for p in my_village.residents if p.name == person_name), None)

    if person:
        # In a real application, here you'd integrate with the language model
        response = person.speak(message)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Person not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
