from langchain import OpenAI

from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain

from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool

from langchain.prompts import PromptTemplate

import tools
import prompts
import utils

llm = OpenAI(temperature=0, model_name="text-davinci-003")

search_prompt = PromptTemplate(
    input_variables=["query"],
    template=prompts.get_search_query
)
search_chain = LLMChain(llm=llm, prompt=search_prompt)
question = "Did the President of the United States from Arkansas have children? If so, where and when were they born?"
#question = "Which segments of the economy are most likely to see job losses due to the advent of AI?"
#question = "Why aren’t large language models (LLMs) massively bearish for software valuations as marginal cost of building software approaches zero?"
#question = "What beverage is triple hops brewed?"
search_query = utils.clean(search_chain.run(question))
print(search_query)

# add ordered id for referencing hrefs
search_results = utils.add_ordered_identifier(tools.ddg(search_query), "id")
# remove href to save tokens
simplified_results = [{key: value for key, value in x.items() if key not in ["href"]} for x in search_results]

filter_prompt = PromptTemplate(
    input_variables=["input"],
    template=prompts.filter_search_results.replace("{query}", question)
)
filter_chain = LLMChain(llm=llm, prompt=filter_prompt)
filter_chain_results = filter_chain.run(simplified_results)
relevant_results = utils.clean(filter_chain_results).split("READ_MORE:")[1].split(",")
print(relevant_results)

document_prompt = PromptTemplate(
    input_variables=["input"],
    template=prompts.summarize_content.replace("{query}", question)
)
search_results = {dictionary["id"]: dictionary for dictionary in search_results}
document_chain = LLMChain(llm=llm, prompt=document_prompt)
max_len = 10000
results = []
for relevant_result in relevant_results:
  url = search_results[relevant_result.strip()]["href"]
  print(f"Loading {url}")
  content = tools.load_url(url)
  segment = content[0:max_len]
  offset = max_len
  #print(segment)
  result = document_chain.run(segment)
  print(f"first: {result}")
  while "READ_MORE" in result and offset <= len(content) and "STOP" not in result:
    segment = content[offset:offset+max_len]
    offset = offset + max_len
    print(f"{url}: {offset}: {len(segment)}")
    result = document_chain.run(segment)
    print(result)
  if "ANSWER:" in result:
    results.append({"url": url, "answer": result})
