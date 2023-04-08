from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

import pinecone 

loader = DirectoryLoader('dask_docs/', glob="*/*.html")
documents = loader.load()
print(len(documents))

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
# initialize pinecone
pinecone.init(
  api_key="8efdff52-3a39-43d7-9902-5ce6b82d93d8",
  environment="us-east4-gcp"  # next to api key in console
)

index_name = "langchain"
docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

query = "Can I use SQL with Dask?"
docs = docsearch.similarity_search(query)
print(docs)
