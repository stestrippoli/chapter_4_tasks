
import openai,json,sys
sys.path.append('..\\capitolo 4')
from utils import *



task = "codeopt"
openai.api_key = "<YOUR_API_KEY>"
filename="main.rs"


context = rs_to_text(f"./{task}/{filename}")
request = f"Try to optimize the Rust code given before with time optimization, variable names refractoring and other optimization techniques." # da promptizzare meglio
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

