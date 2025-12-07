title: Physical AI & Humanoid Robotics – AI-Native Textbook Plan
version: 1.0

goals:
  - Create a complete AI-native textbook using Docusaurus.
  - Deploy book on GitHub Pages or Vercel.
  - Build an integrated RAG chatbot using FastAPI + Qdrant + Neon + OpenAI Agents SDK.
  - Add personalization, signup/signin using Better-Auth.
  - Add chapter-wise personalization + Urdu/English translation toggle.
  - Integrate reusable intelligence via Claude Code Subagents & Agent Skills.

modules:
  - Book Creation
  - RAG Backend
  - Database Layer
  - Authentication Layer
  - Personalization Engine
  - Urdu Translation Engine
  - Subagents + Skills Engine
  - Deployment

milestones:
  - Week 1: Docusaurus project + structure + initial chapters.
  - Week 2: RAG backend + embeddings + Qdrant + Neon.
  - Week 3: Frontend chatbot integration into Docusaurus.
  - Week 4: Better-Auth integration + personalization UI.
  - Week 5: Subagents + Agent skills.
  - Week 6: Final polishing + demo video + submission.

tech-stack:
  - Docusaurus 3
  - TypeScript + React
  - FastAPI
  - Qdrant Cloud (free)
  - Neon Postgres
  - Better-Auth
  - OpenAI Agents / ChatKit SDK
  - Claude Code Subagents
  - Docker (optional)
  - GitHub Pages / Vercel

success-criteria:
  base-points: 100
  bonus:
    - reusable-intelligence: +50
    - auth-personalization: +50
    - per-chapter-customization: +50
    - urdu-translation: +50