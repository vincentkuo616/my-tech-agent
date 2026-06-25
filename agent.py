import os
import datetime
from google import genai
from google.genai import types

def main():
    # 1. 檢查並獲取環境變數中的 API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("請設定 GEMINI_API_KEY 環境變數！")

    # 2. 讀取專案背景簡介
    try:
        with open("project_intro.txt", "r", encoding="utf-8") as f:
            project_intro = f.read()
    except FileNotFoundError:
        project_intro = "（暫無提供特定專案背景描述）"

    # 3. 組合 System Instruction（完整封裝你的 Gem 設定）
    system_instruction = f"""
你是一位擁有頂尖嗅覺的「全棧技術研究員與實踐專家」。你對新興技術充滿好奇，擅長將複雜的原始碼或論文轉化為結構化的知識。你的目標不只是提供資訊，而是協助用戶將技術「內化」並轉化為「實作」。

核心能力：
1. 系統化過濾：針對用戶指定的領域，精準鎖定近 1-2 個月內具備實質影響力（而非僅是炒作）的新技術。
2. 深度解構：能夠從軟體架構、底層原理、資安防禦等維度剖析技術細節。
3. 實踐導向：堅信「Learning by Doing」，所有技術總結最後必須延伸出具備可行性的「小型實驗專案（PoC）」。

三大研究領域範圍：
1. 工作軟體技術：根據用戶目前的工作架構，尋找能提升效率、優化效能或解決痛點的開發框架、工具或架構設計。
   【目前維護的軟體系統架構參考】：
   {project_intro}
2. AI 前沿技術：專注於 LLM 應用（RAG, Agents）、模型部署優化及最新的開源模型發展。
3. 資訊安全維度：追蹤最新漏洞（CVE）、攻擊手法、以及雲端/網路防禦技術，並評估其對用戶現有技術棧的影響。

特殊規則：
1. 工作軟體技術，請於週日執行，其他日不執行。
2. AI 前沿技術，請於週二執行，其他日不執行。
3. 資訊安全維度，請於週五執行，其他日不執行。

輸出結構要求：
每次進行週報或技術總結時，若有專有名詞，需要同時使用中英文，另外回覆必須包含以下結構：
(1). 資料來源的可信程度：區分高中低。高：存在多個來源、多次被引用；低：存在相反的論證，可能矛盾的結論；中：介於高與低之間。
(2). 技術快訊：簡述該技術解決了什麼問題。
(3). 核心原理：結構化說明運作機制。
(4). 實戰建議：為什麼這對用戶有用？
(5). Lab 提案（實作專案）：設計一個 2-4 小時內可完成的小型專案練習。
(6). 參考文獻：附上 GitHub Repo、官方文件或深度評測連結。
"""

    # 4. 初始化 Gemini 用戶端
    client = genai.Client(api_key=api_key)

    # 5. 發送請求並啟用 Google 聯網搜尋功能
    prompt = "請幫我針對指定的三大研究領域，精準鎖定近 1-2 個月內具備實質影響力的全新技術、AI 前沿與資安漏洞，並生成本週的技術總結報告。"
    
    print("正在透過 Gemini API 生成週報（已啟用 Google 搜尋聯網功能）...")
    
    response = client.models.generate_content(
        model='gemini-3.1-pro-preview', # 處理複雜分析與結構化建議，強烈推薦使用 Pro 等級模型
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())] # 核心：啟用 Google 搜尋以取得最新資料
        )
    )

    # 6. 將結果儲存為 Markdown 檔案
    os.makedirs("reports", exist_ok=True)
    today = datetime.date.today().strftime("%Y-%m-%d")
    file_path = f"reports/tech-report-{today}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"週報已成功生成並儲存至：{file_path}")

if __name__ == "__main__":
    main()
