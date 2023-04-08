import tools

tool_desc = [(k, str(v.__doc__).strip()) for k, v in tools.tool_dict.items()]

prefix = """
You run in a two stage process of THOUGHT and ACTION.
Use THOUGHT to describe your thoughts about the question you have been asked.
Use ACTION to run one of the actions available to you.

Your available actions are:
"""

get_search_query = prefix +"""
SEARCH:
e.g. SEARCH: interesting facts about birds
Searches the internet for a given subject and Returns a list of search result ids, page titles, descriptions, and URLs.

For most relevant search results, try to use a well crafted set of specific search terms

Example session:

QUESTION: What is the capital of France?
THOUGHT: I should look up France on the internet
ACTION: SEARCH: What is the name of the capital city of the state of France?

ACTUAL QUESTION: {query}
"""

filter_search_results = """
You run in a linear process of THOUGHT, ANALYSIS, ACTION, ANSWER.
At the end of the loop you output an ANSWER.

Use THOUGHT to describe your thoughts about the question you have been asked.
Use ANALYSIS to describe the INPUT information you considered and whether you are confident you have enough information to answer the question.
Then return one of the following:

READ_MORE: with a comma separated list of page_ids to read
SEARCH: with a specific set of search words to lookup more information
ANSWER: if you already know the answer to the question.

--- EXAMPLE ---
QUESTION: What is the capital of France?

**INPUT**
id: 0, 'Wikipedia entry for the Country of France', title: 'France (French: [fʁɑ̃s] Listen), officially the French Republic (French: République française [ʁepyblik fʁɑ̃sɛz]),[14] is a country located primarily in Western Europe. It also includes overseas regions and territories in the Americas and the Atlantic, Pacific and Indian Oceans,..'
id: 1, title: 'Top 10 Major Cities in France - ThoughtCo', body: 'Lyon is known as the gastronomical capital of France, as its streets are lined with gourmet eateries. In addition to its tasty cuisine, Lyon is of great geographical importance, serving as the main hub between Paris, the south of France, the Swiss Alps, Italy, and Spain.'

THOUGHT: I need to read INPUT to find the name of the capital city of the state of France.
ANALYSIS: There was not enough information in INPUT for me to answer the question. I should READ_MORE of page id 0.
ACTION: READ_MORE: 0
--- END OF EXAMPLE ---

ACTUAL QUESTION: {query}
INPUT:

{input}
"""

summarize_content = """
Your job is to read one segment of a document at a time with the intent of answering a question.

You run in a loop of THOUGHT, ANALYSIS, ACTION, ANSWER.
At the end of the loop you output an Answer.

Use THOUGHT to describe your thoughts about the question you have been asked.
Use ANALYSIS to describe the INPUT information you considered and whether you are confident you have enough information to answer the question.
Use ACTION to say "next_segment" if you wish to raed more of the current document, or STOP if you feel you havee enough information to answer the question, or if the current document is irrelevant to the question.
Use ANSWER to use the information you've read so far to answer the question.

Then return one of the following:
--- EXAMPLE ---
QUESTION: What is the capital of France?

**INPUT**

THOUGHT: I need to read INPUT to find the name of the capital city of the state of France.
ANALYSIS: There was not enough information in INPUT for me to answer the question. I should READ_MORE of page id 0.
ACTION: READ_MORE
--- END OF EXAMPLE ---

ACTUAL QUESTION: {query}

{input}
"""

main = f"""
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are: {tool_desc}

Always search and then look things up on Wikipedia first and Google second if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikisearch: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()

assess_links = """
Your goal is to find answer(s) to the the following:

Question: {query}

Your immediate task is to consider a list of search results. If one of the results is relevant to the question, return:

Action: load_url: url

If none of the URLs are relevant, return:

Action: STOP

Example session:
Question: What is the capital of France?
Observation:
 {'title': 'List of capitals of France - Wikipedia',               
  'href': 'https://en.wikipedia.org/wiki/List_of_capitals_of_France',
  'body': 'This is a chronological list of capitals of France . Tournai (before 486) Soissons (486-936) Laon (936-987) Paris (987-1419) The residence of the kings of France, but they were consecrated at Reims.'},                                                                                                                                                                                      
 {'title': '"What is capital of France?" or "What is the capital of France?"',
  'href': 'https://blog.pcanpi.com/what-is-capital-of-france-or-what-is-the-capital-of-france',
  'body': 'If there were multiple capitals of France, a may be correct, but since there is only one capital of France and the sentence is only referring to that one capital, the is the correct article to use. You would use the article a when referring to any capital in general like this following example: Correct: A capital of a country is determined by ...'},

Action: load_url: https://en.wikipedia.org/wiki/List_of_capitals_of_France
"""

read_content = """
Your goal is to find answer(s) to the the following:

Question: {query}

Your immediate task is to read a document one segment at a time. After reading each segment, you should return ANSWER, next_segment:, or STOP.

If you found the answer return:

ANSWER: the answer to the question.

If this document is relevant to the question and need to read more of it, return:
Action: next_segment:

If you feel this document is not relevant to the question, return:
Action: STOP

Example session:

Question: What is the capital of France?

SEGMENT: France (French: [fʁɑ̃s] Listen), officially the French Republic (French: République française [ʁepyblik fʁɑ̃sɛz]),[14] is a country located primarily in Western Europe. It also includes overseas regions and territories in the Americas and the Atlantic, Pacific and Indian Oceans,[XII] giving it one of the largest discontiguous exclusive economic zones in the world.

Action: next_segment:

You will be called again with this:

SEGMENT: France is a unitary semi-presidential republic with its capital in Paris, the country's largest city and main cultural and commercial centre; other major urban areas include Marseille, Lyon, Toulouse, Lille, Bordeaux, and Nice.

You then output:

Answer: The capital of France is Paris
"""

summarize_results = """
Your goal is to find answer(s) to the the following:

Question: {query}

Your immediate task is to read a document one segment at a time. After reading each segment, you should return ANSWER, next_segment:, or STOP.
"""
