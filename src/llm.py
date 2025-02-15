"""
主にLangChainを用いたロジック
"""

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper

from consts.prompts import SYSTEM_PROMPT


def response_text_from_llm(user_message: str, llm: ChatOpenAI) -> str:
    """
    ユーザーのリクエストからレスポンステキストを返す
    """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]
    response = llm.predict_messages(messages)
    return response.content.strip()

def response_text_from_llm_searching_internet(user_message: str, llm: ChatOpenAI, serpapi_api_key: str) -> str:
    """
    ユーザーのリクエストから、SerpAPI検索をして、レスポンステキストを返す
    """
    # SerpAPI検索のセットアップ
    search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
    
    # ユーザーの質問をネット検索
    search_results = search.run(user_message)

    # LLMに渡すメッセージを構築
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"ユーザーの質問: {user_message}\n\n検索結果:\n{search_results}"),
    ]

    # LLMの応答を取得
    response = llm.predict_messages(messages)
    return response.content.strip()

