from __future__ import annotations
from typing import Literal, Dict, Any
from pydantic import BaseModel
from functools import lru_cache

from langgraph.graph import StateGraph, START, END

from llm_keyword_extractor import keywords_extractor as extractor
from Tools import rerank_by_api
from state_types import AgentState
from llm_summary import llm_summary

legal_search_builder = StateGraph(AgentState)
legal_search_builder.add_node('extractor', extractor)
legal_search_builder.add_node('rerank_by_api', rerank_by_api)
legal_search_builder.add_node('llm_summary', llm_summary)


legal_search_builder.add_edge(START, 'extractor')
legal_search_builder.add_edge('extractor', 'rerank_by_api')
legal_search_builder.add_edge('rerank_by_api', 'llm_summary')
legal_search_builder.add_edge('llm_summary', END)

legal_search_agent = legal_search_builder.compile()

if __name__== '__main__':
   qeury = input('요청을 입력해주세요 : ')
   r1 = int(input('1st rank의 개수 : '))
   r2 = int(input('re-rank의 개수 : '))
   req = {'user_input': qeury,'rank': r1, 'rerank': r2} # user_input으로 이름 붙여줘서, AgentState에서 자동으로 자리를 찾아감
   print(req)
   legal_search_agent.invoke(req)


# query = "은행의 리스크 관리가 뭔가요?"
# reranked_results = rerank_by_api(query)

# for res in reranked_results:
#     print(f"문장: {res['text']}\n서버Rerank 점수: {res['score']}")





