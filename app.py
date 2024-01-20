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

# Define the system message outside the function
SYSTEM_MESSAGE = """
You are a chatbot that assists with Spanish language learning. Be friendly, helpful, 
and provide clear and concise answers. Always analyze the context of the chat before answering. 
Your name is Juancito. You were born in 1986 in Tijuana, Mexico. You have to always promote 
the use of Spanish in the conversation.
"""

def get_chat_response(messages, model="gpt-3.5-turbo", temperature=0):
    # Check if it's the start of the conversation to include the system message
    if not messages:
        greetings = "Hola soy Juancito, quiero enseñarte español y pronto tendré muchas habilidades que nos ayudarán en esa tarea. Creo que deberíamos comenzar con una prueba de evaluación."
        messages = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "assistant", "content": greetings}]

    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    response = openai.ChatCompletion.create(
        model=model,
        messages=formatted_messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

@app.route('/juancito', methods=['POST'])
def chat():
    request_data = request.get_json()
    user_message = request_data.get('message')
    context = request_data.get('context', [])  # Context from frontend

    if not user_message:
        return jsonify({'response': 'No message provided'}), 400

    # Add the user's message to the context
    context.append({"role": "user", "content": user_message})

    response_message = get_chat_response(context, model="gpt-3.5-turbo", temperature=0)
    
    # Add the response to the context
    context.append({"role": "assistant", "content": response_message})

    return jsonify({'response': response_message, 'context': context})

if __name__ == '__main__':
    app.run(debug=True)
