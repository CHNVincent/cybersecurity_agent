# CyberSecurity Agent

A cybersecurity intelligent agent built with Django, featuring AI-driven code auditing capabilities through the CyberSec agent that includes four main components: brain (LLM), planning, tool use, and memory.

## 🛡️ Features

- **Intelligent Code Auditing**: Leverages AI to identify security vulnerabilities in code
- **Four-Agent Core**: Brain (LLM), Planning, Tool Use (Skills), Memory system
- **MCP (Model Context Protocol) Support**: Enables external model communication
- **Modular Skill Architecture**: Pluggable skills system for extending functionality
- **Memory Management**: Short-term (conversation context) and long-term (persistent) memory
- **Secure Web Interface**: Built for cybersecurity professionals

## 📋 Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Frontend**: HTML/CSS/JS (based on existing interface)
- **Database**: SQLite for development, PostgreSQL for production
- **LLMs**: Alibaba Tongyi (AliBailian), OpenAI compatibility layer
- **Memory**: Vector database (Chroma/FAISS support)
- **Messaging**: WebSocket support for MCP
- **Background Processing**: Celery (optional)

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- Virtual Environment
- Database (SQLite included, PostgreSQL recommended)

### Installation

1. **Clone Repository & Setup Virtual Environment**

   ```bash
   git clone [repository-url]
   cd cybersecurity_agent
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**

   Rename `.env.example` to `.env` and configure:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True  # Set to False for production
   ALI_BAILIAN_API_KEY=your-ali-api-key
   ALI_BAILIAN_MODEL=codeqwen-plus  # For code auditing
   OPENAI_API_KEY=your-openai-key
   ```

4. **Database Setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

   The application will be accessible at `http://localhost:8000`.

## 🔧 API Routes

- `POST /api/agent/chat/` - Chat with the cybersecurity agent
- `GET /api/conversations/` - List conversation history
- `GET /api/skills/` - List available skills
- `POST /api/skills/install/` - Install a new skill (upload zip)
- `DELETE /api/skills/{skill_name}/` - Uninstall a skill

## 🛠️ Core Architecture

### Agent Components

1. **Brain (LLM Module)**: Interfaces with LLMs like AliBailian for reasoning and response generation
2. **Planning Module**: Creates execution plans for complex tasks
3. **Tool Use (Skill Manager)**: Manages installable skills/plugins
4. **Memory Module**: Handles both short-term and long-term memory persistence
5. **MCP Module**: Provides Model Context Protocol interface for external integrations

### Skill System

Skills are modular, pluggable components that extend the agent's capabilities. They're located in the `skills/` directory with the following structure:

```
skills/
└── skill_name/
    ├── skill.json          # Skill metadata and parameters
    ├── main.py             # Skill implementation
    └── requirements.txt    # Skill-specific dependencies
```

## 💾 Memory System

### Short-term Memory
- Stores conversation context for active sessions
- Limited capacity for fast access
- Expires after conversation ends

### Long-term Memory
- Persistent storage using vector databases
- Stores security audits, important insights, patterns
- Enables learning from past interactions

## 🔐 Security Measures

- All secrets loaded from environment variables
- Secure file upload handling for code analysis
- Authentication required for API endpoints
- CSRF protection for web forms

## 🧪 Running Tests

```bash
python manage.py test
```

## 🚀 Deployment

This project can be deployed using standard Django hosting solutions. Consider using:

- **Gunicorn + Nginx** for server deployment
- **Docker** for containerization
- **Cloud platform** (AWS, Azure, etc.)

## 🤝 Contributing

Contributions are welcome for improving security audits, adding new skills, optimizing memory systems, or enhancing planning modules!

## 🔒 License

MIT License - See LICENSE for details