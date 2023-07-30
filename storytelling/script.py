import sys,openai,json
sys.path.append('..\\capitolo 4')
from utils import *


task = "storytelling"
openai.api_key = "<YOUR_API_KEY>"

    
request = f"Write a children story in which you explain the relativity theory with terms comprehensible by children. Use witches, ogres and potions as element."
payload = {"question" : request, "answer":[]}

for i in range(5):
    completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo", 
  temperature = 0.8,
  max_tokens = 1000,
  messages = [
    {"role": "system", "content": "You should be able to create stories from input."},
    {"role": "user", "content": request},
  ]
)
    print(completion.choices[0].message['content'])
    
    answer = completion.choices[0].message['content']
    payload["answer"].append(answer)

with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)
