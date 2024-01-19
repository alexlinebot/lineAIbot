import requests
def chatpdf(content):
    headers = {
        'x-api-key': 'sec_kCiJSOE8kK4zhtmFwx2a4i5WwUQSjOcr',
        "Content-Type": "application/json",
    }

    data = {
        'sourceId': "cha_7uP1QS1vID0X0YhqHK2IH",
        'messages': [
            {
                'role': "user",
                'content': content+", 用繁體中文回答",
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        print('Result:', response.json()['content'])
        return response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return response.text