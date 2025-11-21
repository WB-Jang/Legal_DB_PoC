from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# llama-server.exe -m "path/model.gguf" --top-p 0.9 --repeat-penalty 1.15 --host 127.0.0.1 --port 8080
BASE_URL = "http://127.0.0.1:8080/v1" #generation mode

llm = ChatOpenAI(
  model = "model_name",
  api_key = "sk-local-any",
  base_url = BASE_URL,
  temperature = 0.0
)

prompt = ChatPromptTemplate.from_messages([
  ("system","""
  You are AI assistant to extract keywords which are helpful to understand user`s query.
  While extracting the keywords, AI assistant should consider what keyword might be essential to intention of [질문] in the form of JSON

  <example>
   json
   {
   'keywords' : ['keyword1','keyword2','keyword3',...]
   }),
  ("human", "[질문]\n{user_query}\n")
])

chain = prompt | llm | StrOutputParser()

def keywords_extractor(query):
  generation = chain.invoke({"user_query": query})
  print(generation)
