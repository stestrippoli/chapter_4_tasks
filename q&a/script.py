import sys,openai,json, os
sys.path.append('..\\capitolo 4')
from utils import *

task = "q&a"
filename = "zetamicin"
openai.api_key = "<YOUR_API_KEY>"


# Text extraction from PDF and cleaning
if not os.path.exists(f"./{task}/{filename}_cleaned.txt"):
  full_text = pdf_to_text(f"./{task}/{filename}.pdf")
  full_text = clean_qa(full_text)
  save(full_text, f"./{task}/{filename}")

else:
   f = open(f"./{task}/{filename}_cleaned.txt", "r", encoding="utf-8")
   full_text = ""
   for line in f:
      full_text+=line
   
# Question Extraction
payload = {"question" : "Extract 3 questions about previous text. Write only the questions, one in each line", "answers":[]}

if not os.path.exists(f"./{task}/output_q.json"):  
  request = f"Extract 3 questions about the previous text. Write only the questions, one in each line."

  for i in range(5):
    completion = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo-16k", #16k since the document contains 12 pages.
      temperature = 0.9,
      max_tokens = 300,
      messages = [
        {"role": "system", "content": "You should be able to produce question or answers of textual input given by the user"},
        {"role": "user", "content": full_text},
        {"role": "user", "content": request},
      ]
    )

    # Export the generated questions
    
    answers = completion.choices[0].message['content'].split("\n")
    payload["answers"].append(answers)
  # Export payload
  with open(f"./{task}/output_q.json", 'w') as f:
      json.dump(payload, f,indent=1)



# Question Answering
qa = []
f2 = open(f"./{task}/output_q.json")
questions = json.load(f2)['answers']
f2.close()

for i in range(5):

  request = f"Given the previous text, answer the following 3 questions:{questions[i]}. Give short answers and be short\n"

  payload = {}
          
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-16k",
    temperature = 0.8,
    max_tokens = 300,
    messages = [
      {"role": "system", "content": "You should be able to produce question or answers of textual input given by the user"},
      {"role": "user", "content": full_text},
      {"role": "user", "content": request}
    ]
  )

  answers = completion.choices[0].message['content'].split("\n")
  for i,q in enumerate(questions[i]):
      payload[f"q{i+1}"] = {"question":q, "answer": answers[i]}
  qa.append(payload)
with open(f"./{task}/output_a.json", 'w') as f:
    json.dump(qa, f, indent=1)
