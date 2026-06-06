import json
import os

def build():
    # 1. Read Resume Text
    resume_path = r"D:\scaler\YashKhunteta_Resume.txt"
    resume_text = ""
    if os.path.exists(resume_path):
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_text = f.read()
    else:
        print(f"Warning: {resume_path} not found.")

    # 2. Read AttendAI README
    attendance_readme_path = r"D:\scaler\attendance_README.md"
    attendance_readme = ""
    if os.path.exists(attendance_readme_path):
        with open(attendance_readme_path, "r", encoding="utf-8") as f:
            attendance_readme = f.read()
    else:
        print(f"Warning: {attendance_readme_path} not found.")

    # 3. Read Fake News README
    fake_news_readme_path = r"D:\scaler\Capstone2_README.md"
    fake_news_readme = ""
    if os.path.exists(fake_news_readme_path):
        with open(fake_news_readme_path, "r", encoding="utf-8") as f:
            fake_news_readme = f.read()
    else:
        print(f"Warning: {fake_news_readme_path} not found.")

    # 4. Define other project structures and tradeoffs
    corpus = {
        "candidate": {
            "name": "Yash Khunteta",
            "title": "Generative AI Engineer & AI/ML Engineer",
            "contact": {
                "phone": "+91-8005656598",
                "email": "yashkhunteta1234@gmail.com",
                "linkedin": "linkedin.com/in/yashkhunteta",
                "github": "github.com/yashkhunteta",
                "location": "Jaipur, India"
            },
            "summary": "AI/ML Engineer with experience building RAG pipelines, multi-agent LLM systems, and ML models from scratch to deployment. Built a reusable RAG benchmarking framework that cut evaluation time by 60% at Genpact.",
            "skills": {
                "GenAI": "RAG, Fine-Tuning, Embeddings, Prompt Engineering, Vector Databases (FAISS, ChromaDB), Semantic Search",
                "LLM Stack": "LangChain, LangGraph, Hugging Face Transformers, OpenAI API, RAGAS, Multi-Agent Systems",
                "ML / DL": "scikit-learn, TensorFlow, Keras, NLP, YOLO, Model Evaluation, Inference Optimisation",
                "Cloud & Infra": "Azure AI Document Intelligence, Azure OCR, Docker (basic), Git, Jupyter, VS Code",
                "Languages": "Python, SQL, JavaScript"
            },
            "experience": [
                {
                    "role": "Engineering Trainee — AI/ML Analytics",
                    "company": "NIIT Organization",
                    "location": "Jaipur",
                    "period": "Oct 2025 – Present",
                    "details": [
                        "Built AI agents integrated into live ERP tabs to handle student queries, automate task suggestions, and simplify navigation — reducing manual support load.",
                        "Worked with the product team to connect agent outputs to existing enterprise workflows, handling edge cases and keeping latency acceptable for classroom use."
                    ]
                },
                {
                    "role": "Data Scientist Intern",
                    "company": "Genpact",
                    "location": "Bengaluru",
                    "period": "Jan 2025 – Jun 2025",
                    "details": [
                        "Built a modular RAG pipeline that any LLM could plug into, with automated scoring across 10+ metrics (RAGAS, heuristics) — cut benchmarking time by 60%.",
                        "Fine-tuned embedding models and tested different chunking and retrieval strategies to improve answer relevance for specific document types.",
                        "Set up Azure AI Document Intelligence and OCR workflows to extract structured data from unstructured enterprise documents."
                    ]
                }
            ],
            "education": [
                {
                    "degree": "B.Tech Computer Science — Data Science",
                    "institution": "NIT University, Neemrana",
                    "period": "2021 – 2025",
                    "score": "CGPA: 7.48"
                },
                {
                    "degree": "Higher Secondary (10+2), PCM",
                    "institution": "Subodh Public School, Jaipur",
                    "period": "2021",
                    "score": "12th: 79%, 10th: 78%"
                }
            ]
        },
        "projects": [
            {
                "name": "AttendAI",
                "description": "A modern, full-stack remote employee attendance and automated payroll system powered by AI notifications.",
                "tech_stack": "FastAPI, SQLite / MS SQL Server, React (Vite), Vanilla CSS, Nginx, Docker-compose",
                "purpose": "Automate remoteness verification, check-in rules enforcement, leave management, and payroll calculations. Features AI notifications for late check-ins, anomalies, and leave balances.",
                "tradeoffs": [
                    "Chose SQLite for easy out-of-the-box local demo setup, but implemented database-agnostic SQLAlchemy models supporting seamless switch to Microsoft SQL Server.",
                    "Chose inline check-in trigger calculation for payroll deductions/overtime instead of heavy background worker jobs to achieve zero-latency responses for the employee check-in button.",
                    "Implemented custom sliding-window rate limiters on AI chat/endpoints directly in FastAPI rather than Nginx/Redis to allow standalone project deployment without complex infrastructure dependencies."
                ],
                "what_to_do_differently": [
                    "Integrate face recognition checking (WebRTC) via front-end camera to prevent buddy-punching.",
                    "Move email notifications (SMTP) to a Celery + Redis background task queue so email network delays don't slow down check-in API responses."
                ],
                "readme": attendance_readme,
                "github_url": "github.com/yashkhunteta/attend-ai-hub"
            },
            {
                "name": "Fake News Detector App",
                "description": "Machine learning system that predicts whether a given article contains fake news.",
                "tech_stack": "Flask Framework, scikit-learn, PassiveAggressiveClassifier, TF-IDF Vectorizer",
                "purpose": "A lightweight, online-learning text classification app deployed on Heroku to detect fake news articles.",
                "tradeoffs": [
                    "Chose PassiveAggressiveClassifier because of its speed and incremental learning capability (scales nicely with high text volume), trading off the deeper contextual semantic understanding of complex deep learning models like transformers.",
                    "Used TF-IDF representation instead of word embeddings to minimize server memory footprint on Heroku free-tier instances."
                ],
                "what_to_do_differently": [
                    "Fine-tune a pre-trained transformer model (like DistilBERT) to understand context and detect nuanced, synthetically generated misinformation.",
                    "Build a scraper that automatically fetches news updates to constantly update the classification database."
                ],
                "readme": fake_news_readme,
                "github_url": "github.com/yashkhunteta/Fake-News-Detector-App"
            },
            {
                "name": "peoplegpt-100x",
                "description": "ATS resume parser and smart scoring backend to screen candidates.",
                "tech_stack": "LangChain, LangChain-Groq, LangChain-OpenAI, DuckDB, python-docx, pdfplumber, pyresparser, scikit-learn, uv package manager",
                "purpose": "Parse candidate resumes (PDF, docx) and evaluate their education, work experience, projects, language, and fit with strict multi-dimensional smart scoring metrics.",
                "tradeoffs": [
                    "Chose DuckDB as the resume parsing metadata database because of its lightning-fast analytical query performance and zero-dependency configuration, sacrificing multi-user concurrent write scaling for high-speed local evaluation.",
                    "Leveraged Groq API for sub-second LLM inference, sacrificing the higher reasoning capabilities of larger models like Claude 3.5 Sonnet to minimize pipeline latency."
                ],
                "what_to_do_differently": [
                    "Integrate a vector database (like Qdrant or Milvus) to enable semantic search across millions of parsed candidates rather than relying on on-the-fly comparisons.",
                    "Add automated candidate screening feedback email triggers using SMTP to send immediate updates to applicants."
                ],
                "github_url": "github.com/yashkhunteta/peoplegpt-100x"
            },
            {
                "name": "brewpass-saas",
                "description": "Two-sided loyalty SaaS backend and dashboard engine for coffee shops.",
                "tech_stack": "Express, Node.js, JWT, PostgreSQL, pg, Razorpay APIs, MSG91 APIs",
                "purpose": "Power customer loyalty point tracking, subscription tiers, invoicing, and merchant dashboards.",
                "tradeoffs": [
                    "Used raw PostgreSQL queries through 'pg' driver instead of an ORM (like Prisma or Sequelize) to optimize execution speed, minimize memory usage, and keep full control over query performance.",
                    "Used local JWT signature verification to avoid roundtrips to an identity provider, trading off the ability to instantly revoke individual user sessions without a blacklist."
                ],
                "what_to_do_differently": [
                    "Rewrite with TypeScript and an ORM like Prisma for type-safe database schemas and better developer velocity.",
                    "Add Redis cache layers for dashboard analytics queries to prevent heavy database load as coffee shops scale."
                ],
                "github_url": "github.com/yashkhunteta/brewpass-saas"
            },
            {
                "name": "Academic Task Learning Agent",
                "description": "Graph-based multi-agent academic co-pilot using state management.",
                "tech_stack": "LangGraph, LangChain, Python",
                "purpose": "4-agent architecture (Planner, Notewriter, Advisor, Coordinator) that collaborates to help students with task planning, note-taking, and study advice.",
                "tradeoffs": [
                    "Chose LangGraph to build structured state-sharing workflows rather than linear LLM chains, enabling complex cyclic loops and routing but increasing state complexity.",
                    "Chose in-memory state checkpointing for quick state passing, trading off persistence across server restarts."
                ],
                "what_to_do_differently": [
                    "Implement a persistent SQLite-backed checkpointer to allow students to pause and resume multi-agent conversations days later.",
                    "Implement parallel execution of independent node steps (like Planner and Advisor) to speed up response time."
                ],
                "github_url": "github.com/yashkhunteta/academic-task-learning-agent"
            }
        ]
    }

    out_path = r"D:\scaler\knowledge_corpus.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)
    print(f"Knowledge corpus successfully created at {out_path}!")

if __name__ == "__main__":
    build()
