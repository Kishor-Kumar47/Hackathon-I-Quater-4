import os
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI
from langchain_core.tools import BaseTool
from .qdrant_retriever import QdrantRetrievalTool

class RAGAgent:
    def __init__(self):
        # Use OpenRouter API with the free model
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        self.client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.retrieval_tool = QdrantRetrievalTool()

    def process_query(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes a user query using the RAG agent.

        Args:
            query: The user's question.
            context: Optional context to use instead of retrieving from vector database.

        Returns:
            A dictionary containing the agent's answer.
        """
        try:
            # If context is provided, use it directly; otherwise, retrieve from Qdrant
            if context:
                retrieved_content = context
            else:
                # Use the retrieval tool to get relevant documents
                retrieved_content = self.retrieval_tool._run(query)

            # Prepare the system message with instructions to use context
            system_message = {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions based ONLY on the context provided. If you don't know the answer, state that you couldn't find it in the provided context."
            }

            # Prepare the user message with the query and retrieved context
            user_message = {
                "role": "user",
                "content": f"Context: {retrieved_content}\n\nQuestion: {query}\n\nPlease answer based only on the provided context."
            }

            # Make the API call to OpenRouter
            response = self.client.chat.completions.create(
                model="xiaomi/mimo-v2-flash:free",  # Using the free model as requested
                messages=[system_message, user_message],
                temperature=0.1,
                max_tokens=1000
            )

            answer = response.choices[0].message.content

        except Exception as e:
            # Handle cases where the agent might fail to find an answer
            # or parsing errors occur, including API credit issues
            error_msg = str(e)
            print(f"Error in RAGAgent: {error_msg}")

            # Check if it's an API credit issue
            if "402" in error_msg or "credit" in error_msg.lower() or "payment" in error_msg.lower():
                answer = "I'm sorry, but I cannot process your request right now due to API credit limitations. However, I can still answer if you provide specific context by selecting text on the page."
            else:
                answer = "I'm sorry, I couldn't find an answer in the provided context."

        return {"answer": answer}