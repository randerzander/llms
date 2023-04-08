# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0
# based on https://til.simonwillison.net/llms/python-react-pattern
import openai
import re
import time

import tools
import prompts


openai.api_key = open("apikey.txt").read().strip()


class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        #print(completion.usage)
        return completion.choices[0].message.content

action_re = re.compile("^Action: (\w+): (.*)$")
def evaluate_actions(result):
    if "ction:" in result:
      action = [x.split("ction:")[1] for x in result.split("\n") if "ction:" in x][0].strip()
      action_input = " ".join(action.split()[1:])
      action = action.split()[0].strip(":").strip()
    #actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
    #print(actions)
    #if actions:
      # There is an action to run
      #action, action_input = actions[0].groups()
      if action in ["STOP", "stop"]:
        return None, None, None
      if action not in tools.tool_dict:
          raise Exception("Unknown action: {}: {}".format(action, action_input))
      print(" -- locally running {} {}".format(action, action_input))
      return action, action_input, tools.tool_dict[action](action_input)
    else:
      return None, None, None

def links(links, q):
    print(f"Consuming {len(links)} links")
    results = []
    for link in links:
      url = link["href"]
      read_bot = ChatBot(prompts.read_content.replace("{query}", q))
      llm_response = read_bot(tools.load_url(url))
      print(f"From link {url}: {llm_response}")
      action, action_input, tool_result = evaluate_actions(llm_response)
      print(action)
      print(action_input)
      print(tool_result)
      while action != None:
          llm_response = read_bot(tool_result)
          print(f"From link {url}: {llm_response}")
          action, action_input, tool_result = evaluate_actions(llm_response)
      results.append({url: llm_response})
    return results


def query(q, max_turns=25):
    i = 0
    bot = ChatBot(prompts.main)
    next_prompt = q
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        action, action_input, tool_result = evaluate_actions(result)
        if tool_result:
            if action == "ddg" and type(tool_result) == list:
                links(tool_result, q)
            elif type(tool_result) == str:
                print(f"Tool Result of {action}", str(tool_result)[:100])
                next_prompt = "Observation: {}".format(tool_result)
            elif type(tool_result) == int:
                next_prompt = "Observation: {}".format(tool_result)
        else:
            return
