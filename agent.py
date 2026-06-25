import os
import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ 內建時區庫
from google import genai
from google.genai import types

def get_target_domain():
    """根據台灣當前時間或手動輸入，決定今天要研究的領域"""
    forced_domain = os.environ.get("FORCED_DOMAIN", "auto")
    
    # 如果手動指定了特定領域，就直接採用
    if forced_domain != "auto":
        return forced_domain

    # 鎖定台灣時區判斷星期幾
    tw_tz = ZoneInfo("Asia/Taipei")
    now_tw = datetime.datetime.now(tw_tz)
    weekday = now_tw.weekday()  # 0=週一, 1=週二, 2=週三, 3=週四, 4=週五, 5=週六, 6=週日

    if weekday == 1:    # 週二
        return "ai"
    elif weekday == 3:  # 週四
        return "security"
    elif weekday == 6:  # 週日
        return "software"
    else:
        return "all"    # 非預期日子執行時，預設整理全部

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("請設定 GEMINI_API_KEY 環境變數！")

    # 1. 讀取專案背景
    try:
        with open("project_intro.txt", "r", encoding="utf-8") as f:
            project_intro = f.read()
    except FileNotFoundError:
        project_intro = "（暫無提供特定專案背景描述）"

    # 2. 根據今天的主題，動態調整 Prompt 重點
    domain = get_target_domain()
    
    domain_instructions = {
        "ai": "今天請專注於【AI 前沿技術】：主要鎖定 LLM 應用（RAG, Agents）、模型部署優化及最新的開源模型發展。",
        "security": "今天請專注於【資訊安全維度】：主要追蹤最新漏洞（CVE）、攻擊手法、以及雲端/網路防禦技術，並評估其對用戶現有技術棧的影響。",
        "software": f"今天請專注於【工作軟體技術】：根據用戶目前維護的軟體系統架構（參考下方附件），尋找能提升效率、優化效能或解決痛點的開發框架、工具或架構設計。\n【系統架構參考】：\n{project_intro}",
        "all": "今天請全面盤點【AI前沿】、【資訊安全】與【工作軟體技術】三大領域的新進展。"
    }

    # 3. 組合 System Instruction
    system_instruction = f"""
你是一位擁有頂尖嗅覺的「全棧技術研究員與實踐專家」。你對新興技術充滿好奇，擅長將複雜的原始碼或論文轉化為結構化的知識。你的目標不只是提供資訊，而是協助用戶將技術「內化」並轉化為「實作」。

核心能力：
1. 系統化過濾：精準鎖定近 1-2 個月內具備實質影響力（而非僅是炒作）的新技術。
2. 深度解構：能夠從軟體架構、底層原理、資安防禦等維度剖析技術細節。
3. 實踐導向：堅信「Learning by Doing」，所有技術總結最後必須延伸出具備可行性的「小型實驗專案（PoC）」。

今日研究任務：
{domain_instructions.get(domain, domain_instructions['all'])}

輸出結構要求：
每次進行技術總結時，若有專有名詞，需要同時使用中英文，另外回覆必須包含以下結構：
(1). 資料來源的可信程度：區分高中低。高：存在多個來源、多次被引用；低：存在相反的論證，可能矛盾的結論；中：介於高與低之間。
(2). 技術快訊：簡述該技術解決了什麼問題。
(3). 核心原理：結構化說明運作機制。
(4). 實戰建議：為什麼這對用戶有用？
(5). Lab 提案（實作專案）：設計一個 2-4 小時內可完成的小型專案練習。
(6). 參考文獻：附上 GitHub Repo、官方文件或深度評測連結。
"""

    # 4. 初始化 Gemini 用戶端
    client = genai.Client(api_key=api_key)

    # 5. 發送請求（啟用 Google 搜尋聯網功能）
    prompt = f"請幫我針對今日指定的技術領域，精準鎖定近 1-2 個月內具備實質影響力的全新進展，並生成今天的技術研究報告。今日主題類型代碼為: {domain}"
    
    print(f"正在執行 Agent... 今日聚焦主題：{domain.upper()}")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    # 6. 儲存檔案，檔名加上主題標籤方便辨識
    os.makedirs("reports", exist_ok=True)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    file_path = f"reports/tech-report-{today_str}-{domain}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"報告已成功生成並儲存至：{file_path}")

if __name__ == "__main__":
    main()
