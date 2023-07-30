#import required model 
import sys
sys.path.append('..\\capitolo 4')
from utils import *
import json, os, openai

task = "codegen"
openai.api_key = "<YOUR_API_KEY>"

request = f"Create a python function able to extract textual information from a pdf file called pdf_to_txt. Make sure to answer with the function only without example or other textual informations, to use latest versions of external modules and without giving recomendations"
payload = {"question" : request, "answer":[]}

for i in range(5):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo", 
    temperature = 0.8,
    max_tokens = 1000,
    messages = [
      {"role": "system", "content": "You should be able to produce python code"},
      {"role": "user", "content": request},
    ]
  )

# Export the generated questions

  answer = completion.choices[0].message['content']
  payload["answer"].append(answer)

with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)


# Testing functions
'''

f = open(f"{task}/output_code.py", "w") 
print(answer)
f.write(answer)
f.close()

from output_code import pdf_to_txt

text = pdf_to_txt(f"./{task}/example.pdf")
with open(f"{task}/output.txt", "w", encoding="utf-8") as f:
    f.write(text)

 # Il modello funziona a tratti, implementa certe volte delle funzioni deprecate rispetto alle ultime rilasciate.
 '''