# RAG-and-AI-agent-Dish-Recommendation-System
本项目基于大模型（LLM）与检索增强生成（RAG）技术，构建了一个智能菜品推荐系统。系统能够根据用户输入的口味偏好、饮食习惯及忌口信息，从预先构建的菜品知识库中检索相关数据，并结合大模型生成个性化推荐结果。  在实现过程中，系统采用向量数据库（Chroma）对菜品数据进行向量化存储，通过相似度检索（Top-K）获取最相关的菜品信息，并利用Agent框架进行工具调用与结果整合，从而实现“理解用户需求 → 检索知识 → 智能推荐”的完整流程。  该系统具有良好的扩展性，可进一步应用于个性化学习推荐、智能问答等场景。

📌 AI Agent 个性化菜品推荐系统
📖 项目简介

本项目基于大语言模型（LLM）与检索增强生成（RAG）技术，实现了一个智能菜品推荐系统。系统能够根据用户输入的口味偏好、喜好与忌口信息，从本地菜品知识库中检索相关内容，并生成个性化推荐结果。

通过结合向量数据库与Agent机制，本系统实现了智能化的信息检索与自然语言生成，提升了推荐的准确性与用户体验。

🚀 核心功能
🧠 个性化推荐
根据用户输入（口味、偏好、忌口）生成定制化菜品推荐
📚 RAG 检索增强
从菜品知识库中检索相关内容，提高回答准确性
🔍 向量检索（Chroma）
使用 embedding + 相似度计算实现高效搜索
🤖 Agent 调度机制
通过工具调用实现多功能扩展（如总结、查询等）
💬 自然语言交互
用户可通过对话方式获取推荐结果
🧱 技术架构
用户输入
   ↓
大模型理解（LLM）
   ↓
Retriever（向量检索）
   ↓
Chroma 向量数据库
   ↓
Top-K 相似度匹配
   ↓
RAG 构建上下文
   ↓
大模型生成推荐结果
🛠️ 技术栈
Python
Streamlit（前端界面）
LangChain（Agent + RAG）
Chroma（向量数据库）
DashScope / 通义千问（大模型 & embedding）
TextLoader / PyPDFLoader（数据加载）
📂 项目结构（示例）
AI_Food_Recommendation/
│
├── app.py                      # 主程序（Streamlit入口）
├── rag/
│   ├── vector_store.py         # 向量数据库构建
│   └── retriever.py            # 检索逻辑
│
├── service/
│   └── rag_summarize_service.py # RAG总结链
│
├── utils/
│   ├── file_handler.py
│   ├── prompt_loader.py
│   └── config_handler.py
│
├── data/
│   ├── 菜品大全.txt
│   └── 菜品口味100问.txt
│
├── chroma_db/                  # 向量数据库
├── prompts/
│   └── main_prompt.txt
│
└── config/
    └── chroma.yml
⚙️ 安装与运行
1️⃣ 创建虚拟环境（推荐 Python 3.11）
python -m venv .venv
.\.venv\Scripts\activate
2️⃣ 安装依赖
python -m pip install -r requirements.txt

（或手动安装）

python -m pip install streamlit langchain chromadb dashscope
3️⃣ 运行项目
python -m streamlit run app.py
📊 数据说明

项目使用自定义构建的菜品数据集，包括：

菜品名称
口味标签（酸/甜/辣等）
适合人群
忌口信息
简要描述

并通过文本切分（chunk）后存入向量数据库进行检索。

🔥 项目亮点
✅ 基于 RAG 架构，提高推荐准确性
✅ 使用 Top-K 相似度匹配优化检索效率
✅ Agent 机制实现多工具扩展
✅ 支持个性化输入（口味/忌口）
✅ 易扩展到教育推荐、智能客服等场景
📈 可扩展方向
📊 用户画像与长期记忆
🧠 知识图谱增强推荐
🔁 多轮对话推荐优化
📱 前端 UI 优化（Web/App）
🥗 营养分析与健康推荐
👨‍💻 作者
计算机专业在读
方向：AI Agent / RAG / 推荐系统
