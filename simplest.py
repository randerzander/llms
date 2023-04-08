import openai
key = open("apikey.txt").read().strip()
openai.api_key = key

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize the LLM wrapper with a high temperature for more random outputs
llm = OpenAI(temperature=0.9)

# Define the prompt template with an input variable for the product
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

# Create an LLMChain that combines the LLM and the prompt template
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain with the specified product (colorful socks)
result = chain.run("colorful socks")

# Print the result
print(result)
