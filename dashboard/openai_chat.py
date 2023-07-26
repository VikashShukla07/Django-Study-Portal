import requests

def chat_with_gpt(message):
    api_key = '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'
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': message}]
    }
    response = requests.post(endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        choices = response_json['choices']
        
        if choices and 'message' in choices[0]:
            return choices[0]['message']['content']
        else:
            return 'Oops! Something went wrong.'
    else:
        return 'Oops! Unable to connect to the API.'