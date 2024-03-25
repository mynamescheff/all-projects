from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
    <head><title>LLM Communication</title></head>
    <body>
        <h2>Enter text to send to the LLM:</h2>
        <form method="POST">
            <textarea name="text_input" rows="4" cols="50"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
        {% if response %}
            <h2>Response from LLM:</h2>
            <p>{{ response }}</p>
        {% endif %}
        {% if error %}
            <h2>Error:</h2>
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text_input = request.form['text_input']
        print(f"Text sent to LLM: {text_input}")  # Print to terminal

        url = "http://localhost:11434/api/generate"
        payload = {"text": text_input}  # Adjust based on your LLM's API
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # This will raise an exception for HTTP errors

            llm_response = response.text  # Or response.json() if JSON response
            print(f"Response from LLM: {llm_response}")  # Print to terminal
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Print to terminal
            llm_response = f"HTTP error occurred: {http_err}"
        except Exception as err:
            print(f"An error occurred: {err}")  # Print to terminal
            llm_response = f"An error occurred: {err}"

        return render_template_string(HTML_TEMPLATE, response=llm_response)
    
    return render_template_string(HTML_TEMPLATE, response=None)


if __name__ == '__main__':
    app.run(debug=True)
