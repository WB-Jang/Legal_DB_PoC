from __future__ import annotations
from typing import Literal, Dict, Any
from pydantic import BaseModel
from functools import lru_cache
import json

from langgraph.graph import StateGraph, START, END

from llm_keyword_extractor import keywords_extractor as extractor
from Tools import rerank_by_api

class AgentState(BaseModel):
  user_input: str
  keywords: list[Any]|None=None
  result: list[Any]|None=None

legal_search_builder = StateGraph(AgentState)
legal_search_builder.add_node('extractor', extractor)
legal_search_builder.add_node('rerank_by_api', rerank_by_api)

legal_search_builder.add_edge(START, 'extractor')
legal_search_builder.add_edge('extractor', 'rerank_by_api')
legal_search_builder.add_edge('rerank_by_api', END)

legal_search_agent = legal_search_builder.compile()

if __name__ == '__main__':
  input = input('요청을 입력해주세요 : ')
  req = {'user_input': input)
  legal_search_agent.invoke(req)
