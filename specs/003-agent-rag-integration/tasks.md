# Tasks: Agent & Retrieval Integration Implementation

**Input**: Design documents from `specs/003-agent-rag-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Project Initialization and Dependencies)

**Purpose**: Establish the foundational project structure and install necessary packages.

- [x] T001 Update `backend/pyproject.toml` to include `fastapi`, `uvicorn`, `qdrant-client`, `openai`, `langchain-openai`, `langchain-community`, `python-dotenv`, `uv`.
- [x] T002 Create the core backend folder structure: `backend/app/api`, `backend/app/services`, `backend/app/models`.
- [x] T003 Create `backend/main.py` as the FastAPI application entry point.
- [x] T004 Create `backend/.env` with placeholder variables for `OPENAI_API_KEY`, `QDRANT_HOST`, `QDRANT_API_KEY`, `QDRANT_COLLECTION`.

---

## Phase 2: Foundational (Core Components)

**Purpose**: Implement the reusable models, services, and agent tools.

- [x] T005 Create `backend/app/models/chat.py` and implement Pydantic models for `AgentQueryRequest`, `AgentResponse`, `RetrievalToolInput`, and `RetrievedDocument` as defined in `data-model.md`.
- [x] T006 Implement Qdrant retrieval service in `backend/app/services/qdrant_retriever.py` to connect to Qdrant and perform searches.
- [x] T007 Implement a LangChain Tool for Qdrant retrieval in `backend/app/services/qdrant_retriever.py` that utilizes the Qdrant retrieval service.
- [x] T008 Implement the core LangChain Agent definition in `backend/app/services/agent.py`, including the Qdrant retrieval tool, and basic agent logic to process queries.

---

## Phase 3: User Story 1 - Agent Answers Questions Based on Full Book Context (P1) 🎯 MVP

**Goal**: Implement the primary functionality where the agent answers queries by retrieving context from the full indexed book.

**Independent Test**: Send an API request to `POST /chat` with a `query` only. The response should be a grounded answer based on the retrieved context.

### Implementation for User Story 1

- [x] T009 [US1] Create the chat API route in `backend/app/api/chat.py` to handle `POST /chat` requests.
- [x] T010 [US1] Integrate `backend/app/services/agent.py` into the `/chat` API route to process queries using the LangChain agent for full-book context retrieval.
- [x] T011 [US1] Implement error handling within the API route for agent processing failures.
- [x] T012 [US1] Create a local test `tests/test_agent.py` for the agent's full-book query -> retrieval -> response flow.

---

## Phase 4: User Story 2 - Agent Answers Questions Based on User-Selected Text (P2)

**Goal**: Implement the functionality for the agent to answer queries using *only* user-provided text.

**Independent Test**: Send an API request to `POST /chat` with both a `query` and `context`. The response should be a grounded answer based exclusively on the provided `context`.

### Implementation for User Story 2

- [x] T013 [US2] Modify the `/chat` API route in `backend/app/api/chat.py` to detect the presence of the `context` field in the `AgentQueryRequest`.
- [x] T014 [US2] Update `backend/app/services/agent.py` to use the provided `context` directly instead of invoking the Qdrant retrieval tool when `context` is present.
- [x] T015 [US2] Create a local test `tests/test_agent.py` for the agent's query + user-provided context -> response flow.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Refine the implementation, address edge cases, and ensure code quality and documentation.

- [x] T016 Implement the "no context found" response (FR-006) in `backend/app/services/agent.py`, ensuring the agent responds with "I'm sorry, I couldn't find an answer in the provided context."
- [x] T017 Add comprehensive docstrings and type hinting to all new functions, classes, and methods across `backend/app/models/`, `backend/app/services/`, and `backend/app/api/`.
- [x] T018 Update `quickstart.md` with final, detailed instructions for installation, environment setup, and running/interacting with the service.
- [x] T019 Conduct a final review of the `plan.md` to ensure all placeholders are removed and it accurately reflects the completed design.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on Foundational completion. Can run in parallel with or after User Story 1.
- **Polish (Phase 5)**: Depends on User Story 1 and User Story 2 completion.

### Parallel Opportunities

- Within Phase 1, T001, T002, T003, T004 can be started in parallel.
- Within Phase 2, T005, T006, T007, T008 can be started in parallel (with internal dependencies).
- User Story 1 (Phase 3) and User Story 2 (Phase 4) can be developed by different teams/developers in parallel after Phase 2 is complete.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Test User Story 1 functionality via the API endpoint.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready.
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!).
3. Add User Story 2 -> Test independently -> Deploy/Demo.
4. Add Polish -> Final testing -> Deploy/Demo.
