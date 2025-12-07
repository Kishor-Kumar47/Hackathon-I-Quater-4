## Project Overview
**Name:** Physical AI & Humanoid Robotics Textbook
**Type:** AI-Native Educational Platform
**Goal:** Win Panaversity Hackathon with 300/300 points
**Deadline:** Nov 30, 2025, 6:00 PM

---

## 🎯 Core Requirements (100 Points)

### 1. Docusaurus Book (40 points)
**What:** Comprehensive textbook covering 13 weeks of Physical AI course

**Content Requirements:**
- 50+ pages of high-quality content
- 30+ working code examples
- 20+ diagrams and illustrations
- 13 weeks covered (see syllabus below)
- Each chapter: intro, theory, examples, exercises, quiz

**Technical Stack:**
- Docusaurus v3.x with TypeScript
- Dark mode + Light mode
- Search functionality
- Mobile responsive
- Table of contents
- Prev/Next navigation

**Course Syllabus:**
```
Week 1-2:  Physical AI Introduction
           - Foundations & embodied intelligence
           - Sensor systems (LiDAR, cameras, IMUs)

Week 3-5:  ROS 2 Fundamentals
           - Architecture, nodes, topics, services
           - Python integration with rclpy
           - Launch files & parameters

Week 6-7:  Gazebo Simulation
           - Environment setup
           - URDF/SDF robot descriptions
           - Physics & sensor simulation

Week 8-10: NVIDIA Isaac Platform
           - Isaac Sim & Isaac SDK
           - AI-powered perception
           - Reinforcement learning

Week 11-12: Humanoid Robot Development
            - Kinematics & dynamics
            - Bipedal locomotion
            - Manipulation & grasping

Week 13:    Conversational Robotics
            - GPT integration
            - Speech recognition
            - Multi-modal interaction
```

**Acceptance Criteria:**
- ✅ Builds without errors
- ✅ All links work
- ✅ Page load < 3 seconds
- ✅ Lighthouse score > 90
- ✅ Mobile responsive

---

### 2. GitHub Pages Deployment (10 points)
**What:** Live, accessible book on the internet

**Requirements:**
- Deployed to GitHub Pages or Vercel
- HTTPS enabled
- Custom domain (optional)
- Auto-deploy on push to main branch
- CI/CD pipeline with GitHub Actions

**URL Format:**
```
https://yourusername.github.io/physical-ai-book/
```

**Acceptance Criteria:**
- ✅ Publicly accessible
- ✅ Fast loading globally
- ✅ No broken links
- ✅ Works on all devices

---

### 3. RAG Chatbot Backend (30 points)
**What:** FastAPI server with intelligent Q&A system

**Architecture:**
```
Backend Stack:
├── FastAPI (Python web framework)
├── OpenAI API (GPT-4 for answers + embeddings)
├── Neon Serverless Postgres (user data, chat history)
├── Qdrant Cloud (vector database for RAG)
└── Better-Auth (authentication)
```

**Core Features:**
1. **Document Ingestion**
   - Read all markdown files
   - Chunk into 512-token pieces
   - Generate embeddings (OpenAI ada-002)
   - Store in Qdrant with metadata

2. **RAG Query Pipeline**
   - User asks question
   - Generate question embedding
   - Search Qdrant (top 5 results)
   - Build context from results
   - Send to GPT-4 with context
   - Return intelligent answer

3. **Selected Text Query**
   - User highlights text on page
   - Ask question about that text only
   - No RAG needed - direct to GPT-4

**Database Schema:**
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    programming_level VARCHAR(50),
    hardware_background TEXT,
    ai_knowledge VARCHAR(50),
    ros_experience BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat history
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    context_chunks TEXT[],
    timestamp TIMESTAMP DEFAULT NOW()
);

-- User preferences
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    content_level VARCHAR(50) DEFAULT 'intermediate',
    preferred_language VARCHAR(10) DEFAULT 'en',
    personalization_enabled BOOLEAN DEFAULT TRUE,
    translation_enabled BOOLEAN DEFAULT FALSE
);
```

**API Endpoints:**
```
POST   /api/chat/query
       Body: { "question": "What is ROS 2?" }
       Response: { "answer": "...", "sources": [...] }

POST   /api/chat/query-selected
       Body: { "text": "...", "question": "..." }
       Response: { "answer": "..." }

GET    /api/chat/history?user_id=123
       Response: { "history": [...] }

POST   /api/auth/signup
       Body: { "email": "...", "password": "...", "background": {...} }

POST   /api/auth/login
       Body: { "email": "...", "password": "..." }
       Response: { "token": "...", "user": {...} }
```

**Acceptance Criteria:**
- ✅ All endpoints working
- ✅ Response time < 3 seconds
- ✅ Accurate answers (90%+ relevance)
- ✅ Error handling complete
- ✅ Swagger docs at /docs

---

### 4. Frontend Chatbot Widget (20 points)
**What:** Interactive chat interface in the book

**UI Requirements:**
- Floating button (bottom-right corner)
- Expandable chat window (400x600px)
- Message history with scrolling
- User messages (right, blue)
- Bot messages (left, gray)
- Typing indicator
- Error messages
- Mobile responsive

**Features:**
1. **General Chat**
   - Ask any question about the book
   - Get RAG-powered answers
   - Show source references

2. **Text Selection Integration**
   - Select text on any page
   - "Ask about this" popup appears
   - Click to ask question about selection
   - Answer based only on selected text

**Tech Stack:**
- React component
- Axios for API calls
- Markdown rendering for answers
- Syntax highlighting for code

**Acceptance Criteria:**
- ✅ Works on all pages
- ✅ Fast responses
- ✅ Beautiful UI
- ✅ Mobile friendly
- ✅ Accessible (keyboard nav)

---

## 🎁 Bonus Features (200 Points)

### 5. Better-Auth Integration (50 points)
**What:** Secure authentication with user profiling

**Features:**
- Signup with email/password
- Multi-step onboarding (5 steps)
- Detailed background questionnaire
- Secure password hashing (bcrypt)
- JWT session management (7 days)
- Profile editing
- Password reset

**Signup Questions:**
```javascript
Step 1: Account Info
- Email
- Password (min 8 chars)

Step 2: Programming Background
- Years of experience (0-20+)
- Languages known (Python, C++, JavaScript, etc.)
- Comfort level (beginner/intermediate/advanced)

Step 3: Hardware Background
- Arduino experience? (yes/no)
- Raspberry Pi experience? (yes/no)
- Previous robotics projects (text field)

Step 4: AI/ML Knowledge
- ML experience level (none/beginner/intermediate/advanced)
- Courses completed (list)
- Familiar with concepts? (supervised learning, neural networks, etc.)

Step 5: ROS & Goals
- ROS experience? (yes/no)
- Which version? (ROS1/ROS2/None)
- Learning goals (text field)
- Time commitment (hours/week)
```

**Why This Matters:**
- Enables personalization
- Tracks user progress
- Provides analytics
- Creates user profiles for demo

**Acceptance Criteria:**
- ✅ Secure authentication
- ✅ All questions collected
- ✅ Session persists
- ✅ Profile page works
- ✅ No security vulnerabilities

---

### 6. Content Personalization (50 points)
**What:** Adapt content based on user's background

**How It Works:**
1. User clicks "Personalize for Me" button at chapter start
2. Backend reads user profile
3. Sends original content + profile to GPT-4
4. GPT-4 adapts content for user's level
5. Return personalized version
6. Cache for performance

**Adaptation Rules:**

**For Beginners:**
- Add prerequisite explanations
- Simpler vocabulary
- More detailed examples
- Step-by-step instructions
- Basic code with comments

**For Intermediate:**
- Balanced explanations
- Standard examples
- Some advanced topics
- Assume basic knowledge

**For Advanced:**
- Concise explanations
- Complex examples
- Skip basics
- Focus on optimizations
- Advanced concepts

**Example:**
```
Original: "ROS 2 uses DDS for communication."

Beginner: "ROS 2 uses a system called DDS (Data Distribution
Service) to help different parts of the robot talk to each other.
Think of it like a telephone network where different programs
can call each other."

Advanced: "ROS 2's DDS middleware provides real-time pub/sub
with QoS policies, offering significant improvements over
ROS 1's TCP-based transport layer."
```

**Acceptance Criteria:**
- ✅ Button on each chapter
- ✅ Accurate adaptation
- ✅ Fast (< 5 seconds)
- ✅ Can toggle back
- ✅ Cached for reuse

---

### 7. Urdu Translation (50 points)
**What:** Translate entire book to Urdu

**Features:**
- "اردو میں پڑھیں" button at chapter start
- Real-time translation using GPT-4
- Preserve code blocks (keep in English)
- Keep technical terms in English
- RTL (right-to-left) text layout
- Beautiful Urdu fonts
- Cache translations

**Translation Rules:**
```
✅ Translate: Explanations, descriptions, instructions
❌ Keep English: Code, technical terms (ROS, SLAM, DDS), URLs
✅ RTL Layout: Urdu text flows right-to-left
✅ Fonts: Noto Nastaliq Urdu or Jameel Noori
```

**Example:**
```
English:
"ROS 2 nodes communicate via topics using a publish-subscribe pattern."

Urdu:
"ROS 2 nodes ایک دوسرے سے topics کے ذریعے بات چیت کرتے ہیں
publish-subscribe pattern استعمال کرتے ہوئے۔"
```

**Acceptance Criteria:**
- ✅ All chapters translatable
- ✅ Code blocks preserved
- ✅ Proper Urdu fonts
- ✅ RTL layout correct
- ✅ Fast (cached)
- ✅ Can switch back to English

---

### 8. Claude Code Subagents (50 points)
**What:** Demonstrate AI-assisted development

**Create 3+ Subagents:**

**Subagent 1: Content Writer**
```markdown
Role: Technical Content Writer
Expertise: Physical AI, ROS 2, Robotics
Task: Write pedagogical content with examples

Usage:
"Write a 2000-word chapter on ROS 2 nodes and topics
with 3 Python examples"
```

**Subagent 2: Code Generator**
```markdown
Role: ROS 2 Python Expert
Expertise: rclpy, Gazebo, Isaac Sim
Task: Generate working code examples

Usage:
"Create a ROS 2 publisher node that sends velocity
commands to a robot"
```

**Subagent 3: Diagram Creator**
```markdown
Role: Technical Illustrator
Expertise: Mermaid diagrams, Architecture diagrams
Task: Create visual representations

Usage:
"Create a Mermaid diagram showing ROS 2 architecture
with nodes, topics, and services"
```

**Documentation Required:**
```markdown
# docs/claude-code-usage.md

## How We Used Claude Code

### Content Generation
- 80% of chapters written with Content Writer subagent
- Saved ~40 hours of writing time
- Maintained consistent quality

### Code Examples
- 50+ examples generated with Code Generator
- All tested and working
- Properly documented

### Diagrams
- 30+ technical diagrams created
- Mermaid and SVG formats
- Clear and educational

### Productivity Impact
- Total time saved: ~60 hours
- Content quality: Professional grade
- Code accuracy: 95%+

### Reusability
All subagents are in `.claude/` directory and can be
reused for future Panaversity projects.
```

**Acceptance Criteria:**
- ✅ 3+ subagents created
- ✅ 5+ agent skills defined
- ✅ Comprehensive docs
- ✅ Shown in demo video
- ✅ Reusable by others

---

## 📹 Demo Video Requirements

**Duration:** Exactly 90 seconds
**Format:** MP4, 1920x1080, 30fps
**Upload:** YouTube (unlisted link)

**Script (90 seconds):**
```
[00-10s] Introduction
"Assalam-o-Alaikum! This is my Physical AI textbook
for the Panaversity Hackathon..."

[10-25s] Book Navigation
- Quick scroll through chapters
- Show beautiful UI
- Highlight content quality

[25-35s] RAG Chatbot
- Ask: "What is ROS 2?"
- Show intelligent answer
- Demonstrate selected text query

[35-45s] Authentication
- Show signup form
- Fill background questions
- Login successfully

[45-55s] Personalization
- Click "Personalize for Me"
- Show content adaptation
- Demonstrate level changes

[55-65s] Urdu Translation
- Click "اردو میں پڑھیں"
- Show RTL layout
- Beautiful Urdu fonts

[65-75s] Claude Code
- Show subagent documentation
- Highlight usage statistics
- Demonstrate reusability

[75-85s] Technical Excellence
- GitHub repo tour
- Show clean code
- Highlight test coverage

[85-90s] Conclusion
"All links in description. Thank you!"
```

**Acceptance Criteria:**
- ✅ Exactly 90 seconds (judges stop watching at 90s!)
- ✅ All features demonstrated
- ✅ Professional quality
- ✅ Clear audio (no background noise)
- ✅ Smooth editing
- ✅ Engaging narration

---

## 🎯 Point Distribution Summary

```
Base Requirements:
├── Docusaurus Book (40 pts)
├── GitHub Pages (10 pts)
├── RAG Backend (30 pts)
└── Frontend Chatbot (20 pts)
SUBTOTAL: 100 points

Bonus Features:
├── Better-Auth (50 pts)
├── Personalization (50 pts)
├── Urdu Translation (50 pts)
└── Claude Subagents (50 pts)
SUBTOTAL: 200 points

GRAND TOTAL: 300 points 🏆
```

---

## ✅ Definition of Done

A feature is "done" when:
- ✅ Code works without errors
- ✅ Tested on multiple devices
- ✅ Documented in README
- ✅ Committed to GitHub
- ✅ Deployed and live
- ✅ Demo-ready

---

## 🚀 Success Criteria

**Minimum to Pass:** 100 points (base features)
**Competitive:** 200 points (base + 2 bonuses)
**WINNING:** 300 points (everything perfect!) 🏆

**Your Goal:** 300/300 points!

---

**File Location:** `.spec/sp.specify`
**Last Updated:** Nov 2025
**Status:** SPECIFICATION COMPLETE ✅
