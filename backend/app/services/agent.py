# backend/app/services/agent.py

import os
from typing import List, Dict, Any, Optional

# from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.agents.agent import AgentExecutor




from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAi
from langchain_core.tools import BaseTool

from backend.app.services.qdrant_retriever import QdrantRetrievalTool

class RAGAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAi(model="gemini-pro", temperature=0)
        self.retrieval_tool = QdrantRetrievalTool()
        self.tools: List[BaseTool] = [self.retrieval_tool]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer questions based ONLY on the context provided. If you don't know the answer, state that you couldn't find it in the provided context."),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, handle_parsing_errors=True)

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processes a user query using the RAG agent.

        Args:
            query: The user's question.

        Returns:
            A dictionary containing the agent's answer.
        """
        try:
            response = self.agent_executor.invoke({"input": query})
            answer = response["output"]
        except Exception as e:
            # Handle cases where the agent might fail to find an answer
            # or parsing errors occur. This directly addresses FR-006.
            answer = "I'm sorry, I couldn't find an answer in the provided context."

        return {"answer": answer}

