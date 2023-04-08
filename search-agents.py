from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI

from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

import os
import tools


lc_tools = [
    Tool(
        name="Intermediate Answer",
        func=tools.search,
        description="useful for when you need to ask with search"
    ),
]

#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = OpenAI(temperature=0)
#llm=ChatOpenAI(temperature=0)
#chat_react = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

react = initialize_agent(lc_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
#one = agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

sas = initialize_agent(lc_tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
#two = self_ask_with_search.run("What is the hometown of the reigning men's U.S. Open champion?")
