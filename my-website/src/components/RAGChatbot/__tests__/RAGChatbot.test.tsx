// my-website/src/components/RAGChatbot/__tests__/RAGChatbot.test.tsx

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import axios from 'axios';
import RAGChatbot from '../index';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('RAGChatbot', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockedAxios.post.mockClear();
  });

  test('renders chat interface correctly', () => {
    render(<RAGChatbot />);
    expect(screen.getByText('RAG Chatbot')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Ask a question...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
    expect(screen.getByText('Start a conversation...')).toBeInTheDocument();
  });

  test('sends a full-book query and displays response', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: { answer: 'This is a test agent response.' },
    });

    render(<RAGChatbot />);
    const input = screen.getByPlaceholderText('Ask a question...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test query' } });
    fireEvent.click(sendButton);

    expect(screen.getByText('Thinking...')).toBeInTheDocument();

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledTimes(1);
      expect(mockedAxios.post).toHaveBeenCalledWith('http://localhost:8000/api/chat', { query: 'Test query' });
    });

    await waitFor(() => {
      expect(screen.queryByText('Thinking...')).not.toBeInTheDocument();
      expect(screen.getByText('Test query')).toBeInTheDocument();
      expect(screen.getByText('This is a test agent response.')).toBeInTheDocument();
      expect(screen.getByText('Mode: Full Book Search |')).toBeInTheDocument();
    });
  });

  // Additional tests for context, error handling, etc., would go here
});
