# Implementation Plan: Frontend-Backend Integration for RAG Chatbot

**Branch**: `004-frontend-rag-docusaurus` | **Date**: 2025-12-18 | **Spec**: [specs/004-frontend-rag-docusaurus/spec.md](spec.md)
**Input**: Feature specification from `specs/004-frontend-rag-docusaurus/spec.md`

## Summary

This plan outlines the integration of the existing FastAPI-based RAG backend with the Docusaurus frontend located in the `my-website` folder. It will involve implementing a UI component in Docusaurus to send user queries to the backend, handle responses, and display them with visual indicators for query mode. The plan also covers configuring secure communication for both local development and production environments.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript/TypeScript (frontend, Docusaurus uses React)
**Primary Dependencies**:
-   **Backend**: FastAPI, Uvicorn, Python-dotenv, (existing RAG components)
-   **Frontend**: React, Docusaurus, (frontend libraries for API calls, e.g., Axios/Fetch)
**Storage**: N/A (Frontend-Backend integration focuses on communication; backend uses Qdrant).
**Testing**:
-   **Frontend**: Jest/React Testing Library (unit/component tests), Playwright/Cypress (E2E integration tests).
-   **Integration**: Manual verification during development.
**Target Platform**: Web browsers (frontend), Linux server (backend).
**Project Type**: Frontend (Docusaurus application in `my-website`) interacting with Backend (FastAPI service).
**Performance Goals**:
-   SC-001: 99% of user queries within 5 seconds.
-   SC-003: Error messages displayed within 2 seconds.
**Constraints**:
-   FR-005: Communication via CORS (explicit origin whitelist, HTTPS).
-   FR-004: UI visual indicator for mode ("Full Book Search" vs. "Context from Selection").
-   FR-007: Docusaurus project in `my-website` folder is the target.
**Scale/Scope**: Integration of existing RAG backend with Docusaurus frontend for interactive querying, supporting two query modes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **[PASS] I. Library-First**: Frontend components will be developed as modular React components. Backend integration logic will be encapsulated.
- **[PASS] II. CLI Interface**: Backend already exposes functionality via API (HTTP is a form of CLI). Frontend will interact via this API.
- **[PASS] III. Test-First (NON-NEGOTIABLE)**: The plan includes frontend unit/component tests and E2E integration tests.
- **[PASS] IV. Integration Testing**: The entire feature is about integration; E2E tests are crucial.
- **[PASS] V. Simplicity**: The approach leverages existing frameworks and established communication patterns (REST/HTTP).

**Result**: All gates pass. No complexity justification is needed.

## Project Structure

### Documentation (this feature)

```text
specs/004-frontend-rag-docusaurus/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api-contracts.md
└── tasks.md             # Phase 2 output (to be created by /sp.tasks)
```

### Source Code (repository root)

The implementation primarily focuses on modifying the existing `my-website` Docusaurus project and configuring the `backend` FastAPI service.

```text
my-website/
├── src/
│   ├── components/            # New: Contains the RAGChatbot UI component
│   │   └── RAGChatbot/        # New: Chat widget React component
│   │       ├── index.tsx      # Chat component logic
│   │       └── styles.module.css # Component-specific styles
│   ├── pages/                 # New/Modified: Example page integrating RAGChatbot
│   │   └── chat.tsx           # Example page with chatbot
│   └── theme/                 # Optional: If custom Docusaurus theme modifications are needed
│       └── ...
├── docusaurus.config.js       # Modified: Potentially for plugins or custom CSS
├── package.json               # Modified: Add frontend dependencies (e.g., Axios)
└── ...                        # Existing Docusaurus files

backend/
├── main.py                    # Modified: Add CORS middleware
├── ...                        # Existing RAG backend files
```

**Structure Decision**: This structure integrates the new UI component into the `my-website/src/components` directory, which is a standard Docusaurus practice for custom React components. `backend/main.py` will be modified for CORS.

## Complexity Tracking

Not applicable. No constitutional violations were identified.