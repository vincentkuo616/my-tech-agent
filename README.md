# my-tech-agent
做資料收集，以讓我學習近期技術、文章。


my-tech-agent/
├── .github/
│   └── workflows/
│       └── weekly_report.yml    # GitHub Actions 自動排程設定
├── reports/                      # 存放自動生成的技術週報（不需手動建立，腳本會自動產生）
├── agent.py                      # 核心大腦：調用 Gemini API 的 Python 腳本
├── project_intro.txt             # 存放原本 Gem 的 @專案簡介.txt 內容
└── requirements.txt              # 定義 Python 套件依賴
