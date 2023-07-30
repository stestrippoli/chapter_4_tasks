import sys,openai,json
sys.path.append('..\\capitolo 4')
from utils import *

task = "ner"
openai.api_key = "<YOUR_API_KEY>"
filename = "limiti_velocita_cleaned.txt"

context = txt_to_text(f"{task}/{filename}")
request = f"Please perform named entity recognition on the previous text fo the entities of fines and relative crime, limits and roads tipologies. Don't explain anything that was not asked."

payload = {"question" : request, "answer":[], "context":context}

# Da promptizzare altrimenti utilizza versioni obsolete
for i in range(5):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-16k", 
    temperature = 0.8,
    max_tokens = 1000,
    messages = [
      {"role": "system", "content": "You should be able to produce named entity recognition"},
      {"role": "user", "content": f"Here is the text you should answer to: {context}"},
      {"role": "user", "content": request},
    ]
  )

  print(completion.choices[0].message['content'])
  answer = completion.choices[0].message['content']
  payload["answer"].append(answer)

with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)
