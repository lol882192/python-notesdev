import requests

headers = {
    'Authorization': 'Bearer secret_7tip6FK2ekcTqIIxHJSW5qXJLQboachrtoNRhxQwPgT',
    'Notion-Version': '2022-06-28',
}

response = requests.get('https://api.notion.com/v1/pages/0308e538-3ee9-43ab-8149-47bfddc249ed', headers=headers)
print (response)