import subprocess
import ollama

response = ollama.chat(model="tinyllama", messages=[
    {"role": "user", "content": "tell me about love in a single line"}
])
print(response["message"]["content"])

