from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

    # System message setting the chatbot's role and behavior


def get_completion(prompt, model="gpt-3.5-turbo"):  # Update model as needed
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=150,
        temperature=0
    )
    return response.choices[0].text.strip()

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):


    # System message setting the chatbot's role and behavior
    system_message =  """
        You are a Spanish teaching bot. Your primary function is to teach Spanish in an interactive and engaging way. \
        You should correct mistakes gently, provide explanations for grammatical concepts, and encourage the user to practice. \
        Use simple and clear language suitable for language learners. \
        """ 
    # Concatenate the messages to form a single prompt
    conversation = system_message + "\n".join([f"{message['role'].capitalize()}: {message['content']}" for message in messages])

    response = openai.Completion.create(
        model=model,
        prompt=conversation,
        max_tokens=150,
        temperature=temperature
    )
    return response.choices[0].text.strip()

@app.route('/juancito', methods=['POST'])
def chat():
    request_data = request.get_json()
    user_message = request_data.get('message')
    context = request_data.get('context', [])  # Context from frontend

    if not user_message:
        return jsonify({'response': 'No message provided'}), 400

    # Add the user's message to the context
    context.append({"role": "user", "content": user_message})

    response_message = get_completion_from_messages(context, model="gpt-3.5-turbo", temperature=0)
    
    # Add the response to the context
    context.append({"role": "assistant", "content": response_message})

    return jsonify({'response': response_message, 'context': context})

if __name__ == '__main__':
    app.run(debug=True)
