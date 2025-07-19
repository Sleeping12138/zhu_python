import requests

# response = requests.get('http://localhost:5000/test')
# print(response.text)

response = requests.post('http://localhost:5000/test', json={'name': 'zhangsan', 'age': 18})
print(response.text)
