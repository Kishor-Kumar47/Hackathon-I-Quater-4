## 🎯 Mission Statement
Create the most comprehensive, accessible, and AI-enhanced textbook on Physical AI & Humanoid Robotics that wins the Panaversity Hackathon by achieving all 300 possible points.

---

## 🏛️ Core Principles

### 1. **Excellence First**
- Every feature must be production-ready, not just "working"
- Code quality matters as much as functionality
- User experience is paramount

### 2. **Innovation Over Imitation**
- Implement ALL bonus features (Auth, Personalization, Translation, Subagents)
- Use cutting-edge tech stack properly
- Create reusable components

### 3. **Educational Value**
- Content must be pedagogically sound
- Clear progression from basics to advanced
- Practical examples and real-world applications

### 4. **Technical Rigor**
- Follow best practices for all technologies
- Proper error handling everywhere
- Scalable architecture  with background information.

    Args:
        user_id: Unique identifier from day one

---

## 📐 Architecture Standards

### Frontend (Docusaurus)
```
Rules:
- TypeScript for type safety
- Component-based architecture
- Mobile-first responsive design
- Accessibility (WCAG 2.1 AA)
- Performance: Lighthouse score > 90
```

### Backend (FastAPI)
```
Rules:
- RESTful API design
- Async/await for all I/O operations
- Pydantic models for validation
- Proper HTTP status codes
- Comprehensive error handling
```

### Database Design
```
Rules:
- Normalized schema (3NF minimum)
- Proper indexing
- Foreign key constraints
- Migration scripts for all changes
```

### Vector Database (Qdrant)
```
Rules:
- Optimal chunk size (512 tokens)
- Metadata for filtering
- Proper collection configuration
- Efficient similarity search
```

---

## 💻 Code Standards

### Python Code
```python
# Style: Black formatter
# Linting: Ruff
# Type hints: Required for all functions
# Docstrings: Google style

# Example:
async def get_user_profile(user_id: int) -> UserProfile:
    """
    Retrieve user profilefor the user

    Returns:
        UserProfile object with user data

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    pass
```

### TypeScript/React Code
```typescript
// Style: Prettier
// Linting: ESLint with strict rules
// Naming: PascalCase for components, camelCase for functions

// Example:
interface ChatMessage {
  id: string;
  content: string;
  timestamp: Date;
  isUser: boolean;
}

const ChatBot: React.FC = () => {
  // Component logic
};
```

### File Structure
```
physical-ai-book/
├── frontend/              # Docusaurus book
│   ├── docs/             # Markdown content
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Custom pages
│   │   └── css/          # Styling
│   └── docusaurus.config.ts
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── tests/            # Unit tests
│   └── main.py
├── .spec/                # Spec-Kit Plus files
│   ├── constitution.md
│   ├── specifications.md
│   ├── plan.md
│   └── tasks.md
└── README.md
```

---

## 🎨 UI/UX Standards

### Design System
- **Colors**: Consistent theme (dark mode + light mode)
- **Typography**: Clear hierarchy, readable fonts
- **Spacing**: 8px grid system
- **Components**: Material-UI or Tailwind CSS
- **Animations**: Subtle, purposeful (< 300ms)

### User Flow
```
Landing → Browse Chapters → Sign Up (with background) →
Personalized Content → Use Chatbot → Translate → Learn
```

### Chatbot UX
- Floating button (bottom-right)
- Expandable chat window
- Text selection integration
- Loading indicators
- Error states with retry

---

## 🔐 Security Standards

### Authentication (Better-Auth)
- Secure password hashing (bcrypt)
- JWT tokens with expiration
- HTTPS only in production
- Rate limiting on auth endpoints

### API Security
- CORS properly configured
- Input validation on all endpoints
- SQL injection prevention
- XSS protection

### Data Privacy
- User data encrypted at rest
- No PII in logs
- GDPR-compliant data handling

---

## 📊 Quality Metrics

### Must Achieve
- ✅ All 300 points (base + bonuses)
- ✅ Zero critical bugs
- ✅ < 3s page load time
- ✅ 95%+ test coverage
- ✅ Mobile responsive (all devices)
- ✅ Accessible (screen readers work)

### Demo Video Requirements
- ✅ Professional narration
- ✅ Smooth transitions
- ✅ Shows all features
- ✅ Exactly 90 seconds
- ✅ Clear audio

---

## 🚀 Deployment Standards

### CI/CD Pipeline
```yaml
On Push:
  - Run linters
  - Run tests
  - Build project
  - Deploy to staging

On PR Merge to Main:
  - Deploy to production (GitHub Pages)
  - Update documentation
```

### Monitoring
- Error tracking (Sentry or similar)
- Performance monitoring
- User analytics (privacy-friendly)

---

## 📝 Documentation Standards

### Code Documentation
- Every function has docstring
- Complex logic has inline comments
- README.md is comprehensive
- API documentation (OpenAPI/Swagger)

### User Documentation
- Getting started guide
- Feature tutorials
- FAQ section
- Troubleshooting guide

---

## 🤝 Collaboration Standards

### Git Workflow
```bash
main        # Production-ready code
├── develop # Integration branch
│   ├── feature/auth
│   ├── feature/chatbot
│   ├── feature/personalization
│   ├── feature/translation
```

### Commit Messages
```
feat: add better-auth integration
fix: resolve chatbot loading issue
docs: update installation guide
refactor: improve RAG pipeline
test: add user profile tests
```

---

## ⚡ Performance Standards

### Frontend
- First Contentful Paint < 1.5s
- Time to Interactive < 3s
- Bundle size < 1MB
- Images optimized (WebP format)

### Backend
- API response < 200ms (95th percentile)
- Database queries optimized
- Caching where appropriate
- Async operations for I/O

### RAG Chatbot
- Response time < 3s
- Accurate answers (> 90% relevance)
- Context-aware responses
- Handles edge cases gracefully

---

## 🎯 Success Criteria

### Hackathon Victory
1. ✅ Base functionality perfect (100 points)
2. ✅ All 4 bonuses implemented (200 points)
3. ✅ Professional demo video
4. ✅ Clean, documented code
5. ✅ Live deployment working
6. ✅ Innovative use of Claude Code

### Long-term Goals
- Reusable for other Panaversity projects
- Can be extended to other courses
- Community contributions possible
- Scalable to 10,000+ users

---

## 🔄 Review Process

### Before Committing
- [ ] Code formatted
- [ ] Tests pass
- [ ] No console errors
- [ ] Documentation updated
- [ ] Meets constitution standards

### Before Demo Submission
- [ ] All features work end-to-end
- [ ] Demo video recorded and edited
- [ ] GitHub repo cleaned up
- [ ] README is impressive
- [ ] Links all working

---

## 📞 Support Channels

- Primary: Claude Code AI assistance
- Secondary: Spec-Kit Plus documentation
- Tertiary: Panaversity Discord/WhatsApp

---

**Last Updated:** November 2025
**Version:** 1.0
**Status:** Active Development
**Target:** 300/300 Points 🎯