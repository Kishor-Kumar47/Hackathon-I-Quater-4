// my-website/src/pages/chat.tsx

import React from 'react';
import Layout from '@theme/Layout';
import RAGChatbot from '../components/RAGChatbot';

function ChatPage() {
  return (
    <Layout
      title="RAG Chatbot"
      description="Chat with the documentation using AI."
    >
      <main>
        <RAGChatbot />
      </main>
    </Layout>
  );
}

export default ChatPage;
