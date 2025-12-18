// my-website/tests/e2e/rag-chatbot.spec.ts

import { test, expect } from '@playwright/test';

test.describe('RAG Chatbot E2E Integration', () => {
  test('should display chat interface and send full-book query', async ({ page }) => {
    // Navigate to the Docusaurus chat page
    await page.goto('/chat');

    // Check if the chat interface is visible
    await expect(page.getByText('RAG Chatbot')).toBeVisible();
    await expect(page.getByPlaceholderText('Ask a question...')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Send' })).toBeVisible();

    // Type a query
    await page.getByPlaceholderText('Ask a question...').fill('What is Docusaurus?');

    // Click send button
    await page.getByRole('button', { name: 'Send' }).click();

    // Expect to see user's query
    await expect(page.getByText('What is Docusaurus?')).toBeVisible();

    // Expect to see a loading indicator (if implemented visually)
    await expect(page.getByText('Thinking...')).toBeVisible();

    // In a real E2E test, you would wait for the backend response and assert its content.
    // For this placeholder, we just assert the loading state disappears.
    await expect(page.getByText('Thinking...')).not.toBeVisible({ timeout: 10000 });

    // Placeholder for asserting agent's response and mode indicator
    // await expect(page.getByText(/Docusaurus is a modern static/)).toBeVisible();
    // await expect(page.getByText('Mode: Full Book Search |')).toBeVisible();
  });

  // Additional E2E tests for context queries, error handling, etc., would go here.
});
