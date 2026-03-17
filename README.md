# CyberSecurity Agent

一个基于 Django 构建的网络安全智能体，具备AI驱动的代码审计能力，包含四大核心组件：大脑（大语言模型）、规划模块、工具使用和记忆模块。

## 🛡️ 功能特性

- **智能代码审计**: 利用 AI 识别代码中的安全漏洞
- **四核心智能体**: 大脑（LLM）、规划、工具使用、记忆系统
- **MCP（模型上下文协议）支持**: 支持外部模型通信
- **模块化技能架构**: 插件式技能系统扩展功能
- **安全管理**: 短期（对话上下文）和长期（持久化）记忆管理
- **安全Web界面**: 专为网络安全专业人士打造

## 📋 技术栈

- **后端**: Django 4.2+, Django REST Framework  
- **前端**: HTML/CSS/JS (基于现有界面)
- **数据库**: SQLite 用于开发，PostgreSQL 用于生产
- **大模型**: 阿里通义千问（AliBailian），支持 OpenAI 兼容层
- **记忆管理**: 向量数据库支持 (Chroma/FAISS)
- **消息传递**: WebSocket 支持 MCP 协议
- **后台处理**: Celery (可选)

## 🚀 部署指引

### 预置条件

- Python 3.10+
- 虚拟环境
- 数据库 (SQLite内置, 生产环境推荐PostgreSQL)

### 安装说明

1. **克隆仓库并设置虚拟环境**

   ```bash
   git clone [repository-url] 
   cd cybersecurity_agent
   python -m venv venv
   source venv/bin/activate  # Windows系统: venv\Scripts\activate
   ```

2. **安装依赖包**

   ```bash
   pip install -r requirements.txt
   ```

3. **环境配置**

   重命名 `.env.example` 为 `.env` 并配置:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True  # 生产环境设为False
   ALI_BAILIAN_API_KEY=your-ali-api-key
   ALI_BAILIAN_MODEL=codeqwen-plus  # 代码审计专用
   OPENAI_API_KEY=your-openai-key
   ```

4. **数据库配置**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **启动开发服务器**

   ```bash
   python manage.py runserver
   ```

   应用将在 `http://localhost:8000` 访问。

## 🔧 API 接口

- `POST /api/agent/chat/` - 与网络安全智能体对话
- `GET /api/conversations/` - 列出对话历史
- `GET /api/skills/` - 列出可用技能
- `POST /api/skills/install/` - 安装新技能 (上传zip)
- `DELETE /api/skills/{skill_name}/` - 卸载技能

## 🛠️ 核心架构

### 智能体组件

1. **大脑 (LLM 模块)**: 接口连接阿里通义及类似大模型进行推理和响应生成
2. **规划模块**: 为复杂任务创建执行计划
3. **工具使用 (技能管理器)**: 管理可安装技能/插件
4. **记忆模块**: 管理短期和长期记忆的持久化
5. **MCP 模块**: 为外部集成提供模型上下文协议接口

### 技能系统

技能是模块化、可插入的组件，可扩展智能体的功能。它们在 `skills/` 目录下具有以下结构：

```
skills/
└── skill_name/
    ├── skill.json          # 技能元数据和参数
    ├── main.py             # 技能实现
    └── requirements.txt    # 技能特定依赖
```

## 💾 记忆系统

### 短期记忆
- 存储活动会话的对话上下文
- 限制容量，快速访问
- 会话结束后过期

### 长期记忆
- 使用向量数据库持久存储
- 存储安全审计、重要见解、模式
- 从过去交互中学习

## 🔐 安全措施

- 所有密钥均从环境变量加载
- 安全的文件上传处理，用于代码分析
- API 端点需要身份验证
- Web 表单启用 CSRF 保护

## 🧪 运行测试

```bash
python manage.py test
```

## 🚀 部署

此项目可使用标准 Django 托管解决方案部署。考虑使用:

- **Gunicorn + Nginx** 进行服务器部署  
- **Docker** 进行容器化
- **云平台** (AWS, Azure 等)

## 🤝 贡献

欢迎贡献改进安全审计、增加新技能、优化记忆系统或增强规划模块！

## 🔒 开源许可

MIT 许可证 - 查看 LICENSE 了解详情