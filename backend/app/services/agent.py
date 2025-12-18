# backend/app/services/agent.py

import os
from typing import List, Dict, Any, Optional

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool

from backend.app.services.qdrant_retriever import QdrantRetrievalTool

class RAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        self.retrieval_tool = QdrantRetrievalTool()
        self.tools: List[BaseTool] = [self.retrieval_tool]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer questions based ONLY on the context provided. If you don't know the answer, state that you couldn't find it in the provided context."),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, handle_parsing_errors=True)

    def process_query(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes a user query using the RAG agent.

        Args:
            query: The user's question.
            context: Optional user-provided context.

        Returns:
            A dictionary containing the agent's answer.
        """
        if context:
            # If context is provided, use it directly without retrieval
            # The agent system prompt already states to use ONLY provided context.
            final_input = f"Context: {context}\n\nQuestion: {query}"
            response = self.llm.invoke(final_input)
            answer = response.content
        else:
            # Otherwise, rely on the agent to use retrieval tool
            try:
                response = self.agent_executor.invoke({"input": query})
                answer = response["output"]
            except Exception as e:
                # Handle cases where the agent might fail to find an answer
                # or parsing errors occur. This directly addresses FR-006.
                answer = "I'm sorry, I couldn't find an answer in the provided context."

        return {"answer": answer}

