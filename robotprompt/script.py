import sys,openai,json
sys.path.append('..\\capitolo 4')
from utils import *

task = "robotprompt"
#openai.api_key = "<YOUR_API_KEY>"

openai.api_key = "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"

def gpt(context, request):
    completion = openai.ChatCompletion.create(
          model = "gpt-3.5-turbo-16k", 
          temperature = 0.8,
          max_tokens = 1000,
          messages = [
            {"role": "system", "content": "You are Spot, a robotic agent that translate command from Natural Language to list of tasks"},
            {"role": "user", "content": context},
            {"role": "user", "content": request},
          ]
        )
    return completion.choices[0].message['content']

def get_data(output):
  true_output = []
  request_list = []
  for i in range(15): 
      with open(f"./robotprompt/requests/{output}/{i}.json", "r") as f:
         data = json.load(f)
         true_output.append(data['answer'])
         request_list.append(data['question'])
  return true_output, request_list

def prompt_evaluation(n, ver):
  """
  Create the ver-th evaluation of the n-th context.
  """
  outputs = ["closed", "open", "temporal"]
  context_list = json.load(open("./robotprompt/context_list.json", "r"))
  context = context_list[n]
  context_results = {'context': context, "closed" : {}, "open" : {}}
  print(f"\t\tCONTEXT {n}")
  print("_____________\n"+context+"\n_____________")
  for output in outputs:
    print(f"_____________\nCATEGORY: {output}\n_____________")
    
    truth_list, request_list = get_data(output)   
    output_results = {"positive" : 0, "percentage" : 0.0, "trials" : []}
    
    for idx in range(15):
      request = request_list[idx]
      answer = gpt(context, request)
      truth = truth_list[idx]
      
      result = {'request_id':idx, 'request':request, 'answer':answer, 'truth':truth, 'result': check_results(truth, answer)}
      output_results['trials'].append(result)

      print(f"- Request {idx} done. ", end="")
      if check_results(truth, answer):
        output_results['positive'] += 1
        print("🗸")
      else:
       print("X")
       print(f"\t{answer}\n\t{truth}")
      output_results["percentage"] = (output_results["positive"]/15) *100
      context_results[output] = output_results
  print("Context evaluation completed!")
  for o in outputs:
    print(f"\t\t\t ## {o.upper()} ## \nSUCCESS:{context_results[o]['positive']}/15 \t\t PERCENTAGE:{context_results[o]['percentage']}%")
  fp = open(f"./robotprompt/results/general/context_{n}/v{ver}.json", "w")
  json.dump(context_results, fp, indent=1)
  fp.close()
  
def check_results(truth, answer):
   """
   Compare truth and answer (in lower case) without unwanted punctuation.
   """
   truth = truth.strip(".").lower()
   answer = answer.strip(".").lower()
   return truth == answer

def single_context_evaluation(category, n):
  """
  Evaluate a specific category using the n-context from the list of context.
  """
  context_list = json.load(open("/robotprompt/context_list.json", "r"))
  truth_list, request_list = get_data(category)   
  context = context_list[n]
  context_results = {'context': context, "positive" : 0, "percentage" : 0.0, "trials" : []}
  print(f"\t\tCONTEXT {n}")
  print(context)
  for idx in range(15):
    request = request_list[idx]
    answer = gpt(context, request)
    truth = truth_list[idx]
    result = {'request_id':idx, 'request':request, 'answer':answer, 'truth':truth, 'result': check_results(truth, answer)}
    context_results['trials'].append(result)
    print(f"- Request {idx} done. ", end="")
    if check_results(truth, answer):
        context_results['positive'] += 1
        print("🗸")
    else:
       print("X")
       print(f"\t{answer}\n\t{truth}")
    fp = open(f"./robotprompt/results/{category}/context_{n}.json", "w")
    context_results["percentage"] = (context_results["positive"]/15) *100
    json.dump(context_results, fp, indent=1)
    fp.close()
  
def custom_context_evaluation(category, context):
  truth_list, request_list = get_data(category)   
  context_results = {'context': context, "positive" : 0, "percentage" : 0.0, "trials" : []}
  print(context)
  for idx in range(15):
    request = request_list[idx]
    answer = gpt(context, request)
    truth = truth_list[idx]
    result = {'request_id':idx, 'request':request, 'answer':answer, 'truth':truth, 'result': check_results(truth, answer)}
    context_results['trials'].append(result)
    print(f"- Request {idx} done. ", end="")
    if check_results(truth, answer):
        context_results['positive'] += 1
        print("🗸")
    else:
       print("X")
       print(f"{request}\n\t{answer}\n\t{truth}")
  print(f"{context_results['positive']}/15")  


def stats():
  stats = []
  for i in range(7):
      stats.append({"closed": 0, "open": 0, "temporal":0})
      for j in range(5):
        with open(f"{task}/results/general/context_{i}/v{j}.json") as f:
           data = json.load(f)
           for o in ["closed", "open", "temporal"]:
            stats[i][o] += data[o]["positive"]

  f = open("./robotprompt/results/summary.txt", "w")    
  for idx, s in enumerate(stats):
    f.write(f"CONTEXT {idx}\n")
    for key,value in s.items():
       f.write(f"\t{key} : {round((value/75)*100, 2)}% ({value}/75)\n")

if __name__ == "__main__":
  
  
  #prompt_evaluation(6,0)
  stats()
  