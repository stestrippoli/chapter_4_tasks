import sys,openai,json, os
sys.path.append('..\\capitolo 4')
from utils import *


# Env definition
task = "summarization"
filename = "limiti_velocita"
openai.api_key = "<YOUR_API_KEY>"

# Document preprocessing
if not os.path.exists(f"./{task}/{filename}_cleaned.txt"):
  context = pdf_to_text(f"./{task}/{filename}.pdf")
  context = clean_summarization(context)
  save(context, f"./{task}/{filename}")

else:
   f = open(f"./{task}/{filename}_cleaned.txt", "r", encoding="utf-8")
   context = ""
   for line in f:
      context+=line
       

request = f"Write a summarization of the previous text."
payload = {"question" : request, "answer":[], "context":context}

for i in range(5):
    completion = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo-16k",
      temperature = 0.8,
      max_tokens = 1000,
      messages = [
        {"role": "system", "content": "You should be able to produce summarizations of textual input given by the user"},
        {"role": "user", "content": context},
        {"role": "user", "content": request},
      ]
    )

    print(completion.choices[0].message['content'])
    print()
    
    answer = completion.choices[0].message['content']
    payload["answer"].append(answer)

with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)
