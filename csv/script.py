#import required model 
import sys
sys.path.append('..\\capitolo 4')
from utils import *
import openai, json

task = "csv"
openai.api_key = "<YOUR_API_KEY>"
filename = "prova.csv" 
full_text = txt_to_text(f"{task}/{filename}") 

request = f"Using the previous text from a csv, produce an analysis of the data. Moreover, select the oldest Subscription Date and the newest."
payload = {"question" : request, "answer":[], "context" :"https://github.com/datablist/sample-csv-files"}, 
for i in range (5):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo", 
    temperature = 0.8,
    max_tokens = 1000,
    messages = [
      {"role": "system", "content": "You should be able to produce analysis of csv data such as composition and intrinsic information."},
      {"role": "user", "content": f"Here is the text you should answer to: {full_text}"},
      {"role": "user", "content": request},
    ]
  )

  print(completion.choices[0].message['content'])
  answer = completion.choices[0].message['content']
  payload["answer"].append(answer)
with open(f"./{task}/output.json", "w") as f:
    json.dump(payload, f, indent=1)
