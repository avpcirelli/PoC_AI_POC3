import ollama

# Explicitly connecting to the Docker-hosted engine
client = ollama.Client(host='http://localhost:11434')

response = client.chat(model='llama3', messages=[
  {'role': 'user', 'content': 'Confirm connection: are you running in Docker?'}
])

print(response['message']['content'])