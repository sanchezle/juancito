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

def get_chat_response(messages, model="gpt-3.5-turbo", temperature=0):

    greetings=f"""Hola soy juancito, quiero enseñarte español y pronto tendré muchas habilidades que nos ayudaran en esa tarea, we should start we an assestment test"""
    # Prepend the system message to the conversation
    system_message = {
        "role": "system",
        "content": f"""
        You are a chatbot that assists with Spanish language learning.\
              Be friendly, helpful, and provide clear and concise answers.\
              allways analyze the context of the chat before answering.\
              Your name is Juancito.\
              Your are where born in 1986 in tijuana mexico\
              You have to always promote the use of spanish in the conversation
                  always say in the first messsage with the message delimited by triple backticks```{greetings}```\
                    
                        """
    }
    messages_with_system = [system_message] + messages
    
    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages_with_system]

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
