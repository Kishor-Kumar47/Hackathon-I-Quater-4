# Research: Frontend-Backend Integration for RAG Chatbot

**Date**: 2025-12-18
**Author**: Gemini

This document resolves open questions identified during the initial planning phase for the Frontend-Backend Integration for RAG Chatbot feature.

---

### 1. Docusaurus UI Integration Strategy

-   **Unknown**: What is the existing structure of the `my-website` Docusaurus project where the UI component should be integrated?
-   **Decision**: The RAG chatbot UI will be integrated as a new React component within the `my-website/src/components` directory. This component will encapsulate the chat interface and interaction logic. It can then be imported and embedded into existing Docusaurus pages (e.g., a documentation page, a dedicated chat page) or into a custom Docusaurus layout.
-   **Rationale**: This approach is modular, leverages Docusaurus's native React support, and offers flexibility for placement within the site. It avoids direct modification of Docusaurus core files or themes, making it more maintainable and upgrade-friendly.
-   **Alternatives Considered**:
    -   Creating a new Docusaurus plugin: More complex and potentially overkill for a single chat widget.
    -   Directly modifying a Docusaurus theme: Less maintainable, ties the UI tightly to a specific theme version.

---

### 2. Production Deployment Strategy

-   **Unknown**: How will the Docusaurus frontend be deployed in production alongside the FastAPI backend?
-   **Decision**: In production, the Docusaurus frontend and FastAPI backend will be deployed under a single domain (e.g., `example.com`). A reverse proxy (e.g., Nginx, Caddy, or a cloud load balancer) will handle routing:
    -   `example.com/` (and all static assets) will be served by the Docusaurus application.
    -   `example.com/api/` will be proxied to the FastAPI backend service.
-   **Rationale**:
    -   **CORS Simplification**: This deployment strategy eliminates cross-origin issues, as both frontend and backend appear to originate from the same domain (`example.com`). This makes CORS policies significantly simpler to configure (effectively, same-origin).
    -   **HTTPS Termination**: HTTPS can be terminated at the reverse proxy level, centralizing SSL certificate management.
    -   **Unified User Experience**: Presents a single, cohesive URL structure to users.
-   **Alternatives Considered**:
    -   Deploying on separate subdomains (e.g., `docs.example.com` and `api.example.com`): Requires more complex CORS configuration, separate SSL certificate management, and potentially more intricate cookie/authentication handling.
    -   Directly exposing the backend on a different port: Not suitable for production due to security risks, browser limitations, and firewall complexities.
