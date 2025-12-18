# Tasks: RAG Retrieval Validation

**Input**: Design documents from `specs/002-rag-validation/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configure the environment and create placeholder files.

- [x] T001 Update `backend/requirements.txt` to include `qdrant-client`, `cohere`, and `python-dotenv`.
- [x] T002 [P] Create the fixture file `tests/fixtures/rag_validation_dataset.json` with example data.
- [x] T003 [P] Create the environment file `backend/.env` with placeholder variables from `quickstart.md`.

---

## Phase 2: Foundational (Core Validation Logic)

**Purpose**: Implement the core, reusable logic for the validation suite in a dedicated library file.
**⚠️ CRITICAL**: The test implementation cannot begin until this phase is complete.

- [x] T004 Create the library file `backend/validation.py` and add necessary imports.
- [x] T005 Implement the `get_cohere_embedding` function in `backend/validation.py`.
- [x] T006 Implement the `search_qdrant` function in `backend/validation.py`.
- [x] T007 Implement the `run_validation_suite` function in `backend/validation.py` to orchestrate the query loop.
- [x] T008 Implement the `calculate_summary_metrics` function in `backend/validation.py`.

**Checkpoint**: Foundational library ready. Test implementation can now begin.

---

## Phase 3: User Story 1 - Validate Retrieval Accuracy (Priority: P1) 🎯 MVP

**Goal**: As an AI developer, I want to run a validation suite against the RAG retrieval pipeline to measure its accuracy, so that I can ensure the quality of the retrieved context.

**Independent Test**: Running `pytest tests/test_rag_validation.py` will execute the full validation suite, check `Recall@10` against a threshold, and print a summary report.

### Implementation for User Story 1

- [x] T009 [US1] Create the test file `tests/test_rag_validation.py` with an empty `test_retrieval_pipeline_accuracy` function.
- [x] T010 [US1] In `tests/test_rag_validation.py`, implement logic to load the golden dataset from `tests/fixtures/rag_validation_dataset.json`.
- [x] T011 [US1] In `tests/test_rag_validation.py`, import and call the `run_validation_suite` and `calculate_summary_metrics` functions from `backend.validation`.
- [x] T012 [US1] In `tests/test_rag_validation.py`, implement logic to log failed test cases to `stdout` as JSON.
- [x] T013 [US1] In `tests/test_rag_validation.py`, implement logic to print the final `ValidationSummary` report to `stdout`.
- [x] T014 [US1] In `tests/test_rag_validation.py`, add the final `assert` statement to verify that `Recall@K` is >= 0.95.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently via `pytest`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improve code quality and documentation.

- [x] T015 [P] Add comprehensive docstrings and type hinting to all new functions in `backend/validation.py`.
- [x] T016 [P] Add docstrings and comments to `tests/test_rag_validation.py` explaining the test flow.
- [x] T017 Final review of all generated artifacts (`plan.md`, `quickstart.md`, etc.) for correctness and clarity.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Parallel Opportunities

- Within Phase 1, T002 and T003 can be done in parallel.
- Within Phase 4, T015 and T016 can be done in parallel.
- The entire feature is a single user story, so there are no parallel story opportunities.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Run `pytest tests/test_rag_validation.py` and confirm it passes and produces the correct report.
5. The feature is considered complete and ready for use.
