import sys,openai,json
sys.path.append('..\\capitolo 4')
from utils import *

task = "robotprompt"
openai.api_key = "<YOUR_API_KEY>"
output = "output"


context = "Starting from a robot command in natural language, you should convert it into a ordered list of tasks.\
  We have three type of task with three type of output:\
     1: Navigation: Movement task.  output: [Navigation:destination_name].\n \
     2: Grasp: Grasp objects task.  output: [Grasp:object_to_be_grasped]\n \
     3: Place: Place object, output: [Place].\
     In the output include just the squared brackets format explained before.\
    Mind that after a Place, you don't possess the object. Moreover, you can't have a Place if there is no Grasp task. A Place belongs to one Grasp (and so to ONE OBJECT).\
    MOST IMPORTANT: be careful about the order of the navigations and target the place in which you have a Place. You can have MULTIPLE STOPS (so navigations) before a specific Place, so for first do a temporal analysis and find the right order.\
    Example: \with the prompt \
      \"take the bottle from the table, and take it to the chair after passing to the bathroom\" \
    you should produce:\
    [Navigation:table], [Grasp:Bottle], [Navigation:Bathroom], [Navigation:chair], [Place]."
  
request = "Take the bottle over the robotics desk after passing through the Area42-entrance, and place it to the metaverse desk after stopping to the mobility desk. Then from the mobility desk where you are, grasp the bottle again and take it back to the starting point."
payload = {"question" : request, "answer":[], "context":context}


for i in range(5):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo", 
    temperature = 0.8,
    max_tokens = 1000,
    messages = [
      {"role": "system", "content": "You are Spot, a robotic agent that translate command from Natural Language to list of tasks"},
      {"role": "user", "content": context},
      {"role": "user", "content": request},
    ]
  )

  print(completion.choices[0].message['content'])
  answer = completion.choices[0].message['content']
  payload["answer"].append(answer)

with open(f"./{task}/{output}.json", "w") as f:
    json.dump(payload, f, indent=1)

