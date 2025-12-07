tasks:

  - id: setup-docusaurus
    desc: Create Docusaurus repo, install Spec-Kit Plus, and push to GitHub.
    steps:
      - npx create-docusaurus@latest textbook classic
      - configure GitHub Pages deployment
      - add sidebar + multi-level chapters for Physical AI

  - id: write-book
    desc: Write full textbook content as per Physical AI & Humanoid Robotics syllabus.
    steps:
      - Module 1: ROS2 Nervous System
      - Module 2: Gazebo + Unity Digital Twin
      - Module 3: NVIDIA Isaac Sim
      - Module 4: Vision-Language-Action (VLA)
      - Capstone: Autonomous Humanoid Robot
      - Hardware Requirements chapter
      - Weekly breakdown
      - Lab architecture

  - id: rag-backend
    desc: Create a FastAPI server for RAG chatbot.
    steps:
      - setup Qdrant Cloud
      - setup Neon DB
      - create embeddings pipeline
      - implement chat endpoint
      - implement "selected text only" query mode

  - id: integrate-chatbot
    desc: Add frontend chatbot into Docusaurus book.
    steps:
      - create React widget
      - connect to FastAPI endpoint
      - add chat bubble UI
      - allow PDF or section-based context selection

  - id: better-auth
    desc: Implement signup + signin with background question prompts.
    steps:
      - install Better-Auth
      - ask user hardware & software experience
      - store profile in Neon DB
      - expose user profile to personalization engine

  - id: chapter-personalisation
    desc: Add “Personalize Chapter” button.
    steps:
      - detect logged-in user
      - modify chapter difficulty
      - add examples based on user's hardware (Jetson, PC, Cloud)

  - id: urdu-translation
    desc: Add a toggle button for Urdu translation.
    steps:
      - add Translate button at chapter start
      - call backend translation agent
      - replace DOM content dynamically

  - id: subagents
    desc: Add Claude Code Subagents for reusable intelligence.
    steps:
      - create skill: "summarize-chapter"
      - create skill: "explain-code"
      - create skill: "convert-to-urdu"
      - create skill: "personalize-content"
      - call subagents inside RAG pipeline

  - id: final-deploy
    desc: Deploy everything + record demo.
    steps:
      - deploy Docusaurus to GitHub Pages or Vercel
      - deploy