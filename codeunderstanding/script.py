import sys,openai,json
sys.path.append('..\\capitolo 4')
from utils import *

task = "codeunderstanding"
openai.api_key = "<YOUR_API_KEY>"
filename="env.py"
    
context = py_to_text(f"./{task}/{filename}")
request = f"Explain the python code given before. \
  Describe all the classes and relative methods. \
    Explain in detail the first 3 function of the class Env."

payload = {"question" : request, "answer":[], "context":context}

for i in range(5):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-16k", 
    temperature = 0.8,
    max_tokens = 2000,
    messages = [
      {"role": "system", "content": "You should be able to explain python code"},
      {"role": "user", "content": context},
      {"role": "user", "content": request},

    ]
  )
  answer = completion.choices[0].message['content']
  payload["answer"].append(answer)
with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)





with open(f"./{task}/output.txt", "w") as f:
  f.write(completion.choices[0].message['content'])