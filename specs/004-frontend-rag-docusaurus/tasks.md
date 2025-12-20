# Tasks: Frontend-Backend Integration for RAG Chatbot

**Input**: Design documents from `specs/004-frontend-rag-docusaurus/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Backend Configuration & Frontend Environment)

**Purpose**: Establish secure communication and prepare the Docusaurus frontend for integration.

- [x] T001 Configure FastAPI `backend/main.py` with CORS middleware to allow requests from the Docusaurus frontend (`http://localhost:3000` for dev, `[PRODUCTION_FRONTEND_URL]` for prod).
- [x] T002 Ensure the `my-website/` Docusaurus project has necessary Node.js dependencies installed (e.g., `axios` or `fetch` polyfill if needed for older browsers).
- [x] T003 In `my-website/package.json`, add `axios` (or preferred HTTP client) as a dependency.

---

## Phase 2: Foundational (Frontend Chat Component Core)

**Purpose**: Develop the core React component for the RAG chatbot UI within Docusaurus.

- [x] T004 Create the basic Docusaurus React component structure in `my-website/src/components/RAGChatbot/`. This includes `index.tsx` and `styles.module.css`.
- [x] T005 Implement the chat input field and a display area for messages within `my-website/src/components/RAGChatbot/index.tsx`.
- [x] T006 Add state management (e.g., `useState`) for chat messages (history), the current input query, the selected context (if any), loading status, and error messages in `RAGChatbot/index.tsx`.
- [x] T007 Implement basic styling for the chat UI in `my-website/src/components/RAGChatbot/styles.module.css`.

---

## Phase 3: User Story 1 - Full-Book RAG Query from Docusaurus UI (P1) 🎯 MVP

**Goal**: Enable users to send queries to the backend and display responses from the full indexed book.

**Independent Test**: Load the Docusaurus page with the chat component, type a query, and verify an accurate, grounded answer from the full book content is displayed.

### Implementation for User Story 1

- [x] T008 [US1] Implement fetch logic in `my-website/src/components/RAGChatbot/index.tsx` to send full-book queries (without `context`) to the backend's `/api/chat` endpoint.
- [x] T009 [US1] Parse the `BackendAgentResponse` and render the agent's answer in the chat display area of `RAGChatbot/index.tsx`.
- [x] T010 [US1] Display a visual indicator (e.g., a small label or icon) in the UI for "Full Book Search" mode with the agent's response, as per FR-004.
- [x] T011 [US1] Integrate the `RAGChatbot` component into a Docusaurus page (e.g., create `my-website/src/pages/chat.tsx` for testing purposes, or embed into an existing layout).
- [x] T012 [US1] Implement error handling in `RAGChatbot/index.tsx` to display user-friendly messages for backend API errors (FR-006).

---

## Phase 4: User Story 2 - Query with Selected Text from Docusaurus UI (P2)

**Goal**: Allow users to query the RAG agent using selected text from the Docusaurus page as context.

**Independent Test**: Select text on a Docusaurus page, submit a query for it, and verify the agent's response is based *only* on the selected text and displayed correctly with the appropriate indicator.

### Implementation for User Story 2

- [x] T013 [US2] Implement logic in Docusaurus to capture user-selected text from the page. This might involve event listeners for mouse selection or a dedicated selection tool.
- [x] T014 [US2] Develop a UI element (e.g., a button, context menu item) that appears upon text selection, allowing the user to initiate a query with the selected text.
- [x] T015 [US2] Modify the fetch logic in `RAGChatbot/index.tsx` to include the captured `context` field when sending user-selected text queries to `/api/chat`.
- [x] T016 [US2] Display a visual indicator (e.g., "Context from Selection") in the UI with the agent's response when using user-provided text, as per FR-004.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Refine functionality, ensure robustness, and finalize documentation.

- [x] T017 Conduct local integration validation: Run both frontend and backend, test both query types, and verify correct behavior, error handling, and visual indicators.
- [x] T018 Implement frontend unit/component tests for `RAGChatbot/index.tsx` using Jest/React Testing Library.
- [x] T019 Implement E2E integration tests (e.g., Playwright) for the full frontend-backend flow, covering both query types and error handling scenarios.
- [x] T020 Update `quickstart.md` with final, detailed instructions for running both frontend and backend for development, and any specific testing instructions.
- [x] T021 Review and clean up `plan.md` to ensure all placeholders are removed and it accurately reflects the completed design.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on Foundational completion. Can run in parallel with or after User Story 1 (if UI component is flexible).
- **Polish (Phase 5)**: Depends on User Story 1 and User Story 2 completion.

### Parallel Opportunities

- Phase 1 tasks (T001-T003) can be started in parallel if different team members handle backend config vs. frontend setup.
- Phase 2 tasks (T004-T007) can be started in parallel if different team members handle different aspects of the React component.
- User Story 1 (Phase 3) and User Story 2 (Phase 4) can be developed by different teams/developers in parallel after Phase 2 is complete.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Test User Story 1 functionality via the Docusaurus UI.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready.
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!).
3. Add User Story 2 -> Test independently -> Deploy/Demo.
4. Add Polish -> Final testing -> Deploy/Demo.
