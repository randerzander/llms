from duckduckgo_search import ddg
import requests
import httpx
from bs4 import BeautifulSoup

import inspect


def wikisearch(q):
    """
    e.g. wikisearch: Django
    Searches wikipedia for entries matching a given subject and Returns a list of wikipedia entry summaries by page_id
    """
    return httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": q, "format": "json"},
    ).json()["query"]["search"]


def wikientrysubjects(q):
    """
    e.g. wikientrysubjects: 12345
    Returns list of subject subsections for a wikipedia entry by page_id
    """
    full_text = httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "explaintext": 1,
            "pageids": q,
        },
    ).json()["query"]["pages"][q]["extract"]
    full_text = "=== Overview ===" + full_text
    subjects = [x.split(" ===")[0] for x in full_text.split("=== ")][1:]
    return full_text, subjects


def wikientrysubject(q):
    """
    e.g. wikientrysubject: 12345 subject
    Returns full text content of a wikipedia entry by page_id and subject subsection
    """
    page_id = q.split()[0]
    subject = " ".join(q.split()[1:])
    full_text, subjects = wikientrysubjects(page_id)
    return (
        full_text.split(subject + " ===")[1].split(" ===")[0].split("\n===")[0].strip()
    )

def search(q):
  ddg_res = duckduckgo(q)
  return [x["body"] for x in ddg_res[0:5]]

def duckduckgo(q):
    """
    e.g. google: subject
    Returns a list of URLs which can be loaded with load_url
    """
    return ddg(q)


content = ""
offset = 0
max_len = 5000


def load_url(url):
    """
    e.g. load_url: https://news.ycombinator.com
    Returns partial text content for a webpage. The next segment of content can be fetched with next_segment:
    """
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    global content
    content = soup.get_text()

    global offset
    offset = max_len
    return (
        content[:max_len]
        #+ '\n ** This was the first segment of content. More is available with "next_segment:"'
    )


def next_segment(arg):
    """
    e.g. next_segment:
    Returns the next segment of text for a webpage previously passed to load_url
    """
    global offset
    res = content[offset : offset + max_len]
    offset = offset + max_len
    return (
        res
        #+ f'\n ** This was the {int(offset/max_len)} segment. More is available with "next_segment:"'
    )


def calculate(what):
    """
    e.g. calculate: 4 * 7 / 3
    Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary
    """
    return eval(what)

tool_dict = {name: obj for name, obj in globals().items() if inspect.isfunction(obj)}
