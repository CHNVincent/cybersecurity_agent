# CyberSecurity Agent

一个基于 Django 构建的网络安全智能体，具备 AI 驱动的代码审计能力，包含四大核心组件：大脑（大语言模型）、规划模块、工具使用和记忆模块。
Cybersecurity intelligent agent built with Django, featuring AI-driven code auditing capabilities through the CyberSec agent that includes four main components: brain (LLM), planning, tool use, and memory.

## 🛡️ 功能特性 / Features

- **智能代码审计 / Intelligent Code Auditing**: 利用 AI 识别代码中的安全漏洞 / Leverages AI to identify security vulnerabilities in code
- **四核心智能体 / Four-Agent Core**: 大脑（LLM）、规划、工具使用、记忆系统 / Brain (LLM), Planning, Tool Use (Skills), Memory system  
- **MCP（模型上下文协议）支持 / MCP (Model Context Protocol) Support**: 支持外部模型通信 / Enables external model communication
- **模块化技能架构 / Modular Skill Architecture**: 插件式技能系统扩展功能 / Pluggable skills system for extending functionality
- **安全管理 / Memory Management**: 短期（对话上下文）和长期（持久化）记忆管理 / Short-term (conversation context) and long-term (persistent) memory
- **安全 Web 界面 / Secure Web Interface**: 专为网络安全专业人士打造 / Built for cybersecurity professionals

## 📋 技术栈 / Tech Stack

- **后端 / Backend**: Django 4.2+, Django REST Framework  
- **前端 / Frontend**: HTML/CSS/JS (based on existing interface)
- **数据库 / Database**: SQLite 用于开发，PostgreSQL 用于生产 / SQLite for development, PostgreSQL for production
- **大模型 / LLMs**: 阿里通义千问（AliBailian），支持 OpenAI 兼容层 / Alibaba Tongyi (AliBailian), OpenAI compatibility layer
- **记忆管理 / Memory**: 向量数据库支持 (Chroma/FAISS) / Vector database (Chroma/FAISS support)
- **消息传递 / Messaging**: WebSocket 支持 MCP 协议 / WebSocket support for MCP
- **后台处理 / Background Processing**: Celery (可选) / Celery (optional)

## 🚀 部署指引 / Setup Instructions

### 预置条件 / Prerequisites

- Python 3.10+
- 虚拟环境 / Virtual Environment
- 数据库 (SQLite内置, 生产环境推荐PostgreSQL) / Database (SQLite included, PostgreSQL recommended)

### 安装说明 / Installation

1. **克隆仓库并设置虚拟环境 / Clone Repository & Setup Virtual Environment**

   ```bash
   git clone [repository-url] 
   cd cybersecurity_agent
   python -m venv venv
   source venv/bin/activate  # Windows系统: venv\Scripts\activate  # On Windows: venv\Scripts\activate
   ```

2. **安装依赖包 / Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **环境配置 / Environment Configuration**

   重命名 `.env.example` 为 `.env` 并配置: / Rename `.env.example` to `.env` and configure:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True  # 生产环境设为False / Set to False for production
   ALI_BAILIAN_API_KEY=your-ali-api-key
   ALI_BAILIAN_MODEL=codeqwen-plus  # 代码审计专用 / For code auditing
   OPENAI_API_KEY=your-openai-key
   ```

4. **数据库配置 / Database Setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **启动开发服务器 / Run Development Server**

   ```bash
   python manage.py runserver
   ```

   应用将在 `http://localhost:8000` 访问。 / The application will be accessible at `http://localhost:8000`.

## 🔧 API 接口 / API Routes

- `POST /api/agent/chat/` - 与网络安全智能体对话 / Chat with the cybersecurity agent
- `GET /api/conversations/` - 列出对话历史 / List conversation history
- `GET /api/skills/` - 列出可用技能 / List available skills
- `POST /api/skills/install/` - 安装新技能 (上传zip) / Install a new skill (upload zip)
- `DELETE /api/skills/{skill_name}/` - 卸载技能 / Uninstall a skill

## 🛠️ 核心架构 / Core Architecture

### 智能体组件 / Agent Components

1. **大脑 (LLM 模块) / Brain (LLM Module)**: 接口连接阿里通义及类似大模型进行推理和响应生成 / Interfaces with LLMs like AliBailian for reasoning and response generation
2. **规划模块 / Planning Module**: 为复杂任务创建执行计划 / Creates execution plans for complex tasks
3. **工具使用 (技能管理器) / Tool Use (Skill Manager)**: 管理可安装技能/插件 / Manages installable skills/plugins
4. **记忆模块 / Memory Module**: 管理短期和长期记忆的持久化 / Handles both short-term and long-term memory persistence
5. **MCP 模块 / MCP Module**: 为外部集成提供模型上下文协议接口 / Provides Model Context Protocol interface for external integrations

### 技能系统 / Skill System

技能是模块化、可插入的组件，可扩展智能体的功能。它们在 `skills/` 目录下具有以下结构：
Skills are modular, pluggable components that extend the agent's capabilities. They're located in the `skills/` directory with the following structure:

```
skills/
└── skill_name/
    ├── skill.json          # 技能元数据和参数 / Skill metadata and parameters
    ├── main.py             # 技能实现 / Skill implementation
    └── requirements.txt    # 技能特定依赖 / Skill-specific dependencies
```

## 💾 记忆系统 / Memory System

### 短期记忆 / Short-term Memory
- 存储活动会话的对话上下文 / Stores conversation context for active sessions
- 限制容量，快速访问 / Limited capacity for fast access
- 会话结束后过期 / Expires after conversation ends

### 长期记忆 / Long-term Memory
- 使用向量数据库持久存储 / Persistent storage using vector databases
- 存储安全审计、重要见解、模式 / Stores security audits, important insights, patterns
- 从过去交互中学习 / Enables learning from past interactions

## 🔐 安全措施 / Security Measures

- 所有密钥均从环境变量加载 / All secrets loaded from environment variables
- 安全的文件上传处理，用于代码分析 / Secure file upload handling for code analysis
- API 端点需要身份验证 / Authentication required for API endpoints
- Web 表单启用 CSRF 保护 / CSRF protection for web forms

## 🧪 运行测试 / Running Tests

```bash
python manage.py test
```

## 🚀 部署 / Deployment

此项目可使用标准 Django 托管解决方案部署。考虑使用:
This project can be deployed using standard Django hosting solutions. Consider using:

- **Gunicorn + Nginx** 进行服务器部署 / for server deployment
- **Docker** 进行容器化 / for containerization  
- **云平台** (AWS, Azure, etc.). / Cloud platform (AWS, Azure, etc.)

## 🤝 贡献 / Contributing

欢迎贡献改进安全审计、增加新技能、优化记忆系统或增强规划模块！
Contributions are welcome for improving security audits, adding new skills, optimizing memory systems, or enhancing planning modules!

## 🔒 开源许可 / License

MIT 许可证 - 查看 LICENSE 了解详情 / MIT License - See LICENSE for details