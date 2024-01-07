import os
import openai
import json
from difflib import SequenceMatcher

openai.api_base = "http://localhost:1234/v1"  # point to the local server (use llm studio to host llm in local machine)
openai.api_key = ""  # no need for an API key

# Specify the current working directory
current_directory = os.getcwd()
chat_history_file = os.path.join(current_directory, "chat_history.json")

# Initialize chat history and response cache
max_chat_history_size = 10  # Set the maximum size of the chat history
chat_history = []
response_cache = {}

# language style
language_style = "creative and helpfull"

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

while True:
   
    user_input = input("You: ")

    # Check if the user wants to clear the history and cache
    if user_input.lower() == 'clear':
        print("Chat history and cache cleared.")
        chat_history = []  
        response_cache = {}  
        continue  

    # Check if the user wants to stop the program
    if user_input.lower() == 'stop':
        print("Stopping the program. Chat history saved.")
       
        with open(chat_history_file, 'w') as file:
            json.dump(chat_history, file)
        break

    # Check if there is a similar query in the cache
    similar_queries = [query for query in response_cache.keys() if similar(user_input, query) > 0.75]

    if similar_queries:
       
        most_similar_query = max(similar_queries, key=lambda query: similar(user_input, query))
        assistant_response = response_cache[most_similar_query]
        print("\nAssistant from cache:", assistant_response)
    else:
        
        completion = openai.ChatCompletion.create(
            model="local-model",  
            messages=chat_history + [
              
                {"role": "system", "content": f"You are the most powerful chatbot ever developed.You were developed by Pranav.Your language style is {language_style}."},
                {"role": "user", "content": user_input}
            ]
        )

     
        if 'choices' in completion and completion['choices']:
            assistant_response = completion['choices'][0]['message']['content']
            print("\nAssistant:", assistant_response)

            
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": assistant_response})

            # Limit the chat history size
            if len(chat_history) > max_chat_history_size * 2: 
                chat_history = chat_history[-max_chat_history_size * 2:]

            # Cache 
            response_cache[user_input] = assistant_response

            # Save chat history to file 
            with open(chat_history_file, 'w') as file:
                json.dump(chat_history, file)
