今天的技術研究報告將聚焦於近期資訊安全領域一項具備實質影響力的重大進展：國家級駭客組織利用人工智慧（AI）自動化滲透測試框架（Agentic AI Penetration Testing Framework），發動供應鏈攻擊，對雲端環境構成新型威脅。

---

### (1). 資料來源的可信程度：高

此議題來自多個高度可信的來源，包括 Microsoft Threat Intelligence (微軟威脅情報中心) 的官方公告、Palo Alto Networks Unit 42 的深入分析、以及多家資安新聞媒體的交叉報導。這些來源均詳細說明了攻擊手法、歸因及影響範圍，證據鏈完整且被廣泛引用。

### (2). 技術快訊：AI 自動化攻擊引發供應鏈危機 (AI-driven Attacks Trigger Supply Chain Crisis)

中國政府支持的駭客組織 Storm-0940 自 2026 年 9 月起，被發現利用一款名為 ARTEX 的「AI 自動化滲透測試框架」(Agentic AI Penetration Testing Framework)，大規模地自動化執行攻擊，包括對全球數百個組織進行掃描與滲透。其中一個引人注目的事件是針對雲端備份服務商 ConnectWise 的供應鏈攻擊，駭客透過竊取其多租戶應用程式的憑證，進而未經授權地存取數千個 Microsoft 365 客戶租戶的雲端基礎設施。這種攻擊將傳統需要人工耗費數週的入侵過程，壓縮至數小時內完成，大幅提升了攻擊的速度、規模和複雜度。

### (3). 核心原理：AI 代理與 OAuth 應用程式濫用 (AI Agents & OAuth Application Abuse)

此次攻擊的核心在於結合了兩種強大的技術與手法：

1.  **AI 自動化滲透測試框架 (ARTEX - Agentic AI Penetration Testing Framework)**：
    *   ARTEX 是一個利用 AI 代理 (AI Agents) 能力的自動化框架，能夠自主識別漏洞、執行攻擊、並維持對受害系統的存取。
    *   AI 代理不受人類限制，可全天候、無休止地工作，並同時嘗試多種入侵路徑，顯著縮短了從鎖定目標到達成目的所需的時間。
    *   在 ConnectWise 案例中，Storm-0940 利用 ARTEX 加速了對憑證濫用的應用程式進行驗證，以機器速度自動化攻擊活動。例如，該框架在短時間內嘗試對 2,250 多個租戶進行登入，甚至在高峰期每分鐘嘗試多達 2,900 次失敗登入。

2.  **OAuth 應用程式供應鏈憑證濫用 (OAuth Application Supply Chain Credential Abuse)**：
    *   攻擊者並未直接網路釣魚用戶或破解密碼。
    *   ConnectWise Cloud Backup (現為 SkyKick) 等備份應用程式通常需要廣泛的讀取權限來存取 Microsoft 365 郵箱、檔案和目錄資料，這些權限是客戶透過 OAuth 同意 (OAuth Consent) 預先授予的。
    *   駭客竊取了該備份應用程式的憑證 (credential)，並利用這些憑證請求 Microsoft Graph 權杖 (Microsoft Graph tokens)。一旦取得，駭客便繼承了該應用程式在所有已安裝租戶中的所有權限。
    *   由於這不是人為登入，多因素驗證 (MFA) 在此過程中無法發揮作用。攻擊者透過 Microsoft Graph 執行了偵察、更改應用程式憑證以及嘗試修改權限等後續活動，以擴大或維持持久存取。

### (4). 實戰建議：為什麼這對用戶有用？ (Why This Is Useful to Users?)

這項進展對所有使用雲端服務、依賴第三方 SaaS 應用程式的組織，以及開發和維護軟體供應鏈的團隊至關重要。

1.  **重新評估第三方應用程式風險 (Re-evaluate Third-Party Application Risk)**：攻擊表明，即使是看似無害或必要的第三方服務 (如備份工具)，一旦其憑證被竊取，也可能成為通往您核心資料的後門。
2.  **強化身分與存取管理 (IAM - Identity and Access Management) 策略**：傳統 MFA 對此類自動化應用程式憑證濫用無效。您需要專注於：
    *   **最小權限原則 (Principle of Least Privilege)**：嚴格審查所有應用程式和服務帳戶的權限，僅授予其完成任務所需的最少權限。
    *   **OAuth 同意審查 (OAuth Consent Review)**：定期審查應用程式被授予的 OAuth 權限，移除不必要或過度寬鬆的權限。
    *   **條件式存取 (Conditional Access)**：對所有存取 (包括服務帳戶) 實施基於行為、位置、設備狀態的條件式存取策略。
3.  **雲端安全態勢管理 (CSPM - Cloud Security Posture Management)**：持續監控雲端環境中的配置錯誤、權限膨脹和異常活動。
4.  **供應鏈安全 (Supply Chain Security)**：不僅關注程式碼來源，更要關注所使用的第三方服務、供應商的安全實踐和他們的資安事件響應能力。
5.  **警惕 AI 驅動的自動化攻擊 (Beware of AI-driven Automated Attacks)**：意識到 AI 正被用於自動化攻擊的各個階段，這意味著傳統的基於簽名或已知模式的防禦可能不足，需要更進階的行為分析和威脅情報。

### (5). Lab 提案（實作專案）：模擬 OAuth 應用程式憑證濫用與監控 (Simulating OAuth Application Credential Abuse & Monitoring)

**專案名稱：** 模擬雲端應用程式憑證濫用與異常行為檢測 (Simulated Cloud App Credential Abuse & Anomaly Detection)

**目標：** 了解第三方應用程式如何被濫用以存取雲端資源，並練習配置監控以檢測此類異常行為。

**預估時間：** 3-4 小時

**所需工具/環境：**
*   一個 Azure / AWS / GCP 免費試用帳戶 (本範例以 Azure AD 為主)。
*   Azure CLI 或 Azure PowerShell。
*   Python 環境 (用於撰寫簡單的模擬腳本)。
*   一個具備管理權限的測試使用者帳戶。

**實驗步驟：**

1.  **設定測試環境：**
    *   在 Azure AD (或您選擇的雲端 IdP) 中創建一個新的應用程式註冊 (App Registration)，並授予其一些過度寬鬆的權限 (例如 `User.ReadWrite.All`, `Files.ReadWrite.All`)。將其設定為多租戶應用程式以模擬第三方服務。
    *   為該應用程式創建一個用戶端密碼 (client secret)。
    *   創建兩個測試使用者帳戶，一個作為「正常用戶」，一個作為「被模擬存取的用戶」。

2.  **模擬正常應用程式存取：**
    *   使用 Python 腳本或 Postman 模擬該應用程式以其自身權限 (client credential flow) 存取 Azure Graph API，執行一些正常的讀取操作 (例如列出用戶、讀取測試檔案)。
    *   觀察 Azure AD 登入日誌 (Sign-in logs) 和審計日誌 (Audit logs)，記錄正常行為的特徵 (應用程式 ID、IP 地址、操作類型)。

3.  **模擬憑證竊取與濫用：**
    *   假設攻擊者竊取了該應用程式的用戶端密碼。
    *   使用另一個 Python 腳本，模擬攻擊者從一個「異常」的 IP 地址 (例如，您的家庭 IP 地址而不是預期的伺服器 IP) 使用相同的應用程式憑證存取 Azure Graph API。
    *   執行惡意操作，例如嘗試修改用戶屬性、刪除測試檔案、或創建新的應用程式註冊 (如果權限允許)。

4.  **配置監控與警報：**
    *   在 Azure Monitor 或 Log Analytics 中，建立查詢來篩選 Azure AD 的登入日誌和審計日誌。
    *   嘗試識別模擬的「異常行為」：
        *   來自非預期 IP 地址的應用程式登入。
        *   特定應用程式在短時間內執行大量不尋常操作。
        *   應用程式嘗試執行超出其正常業務範圍的操作 (例如修改管理員組)。
    *   配置一個簡單的警報規則，當偵測到這些異常模式時觸發通知。

5.  **檢討與防禦思考：**
    *   分析日誌中正常與異常活動的差異。
    *   思考如何收緊應用程式權限 (最小權限原則)。
    *   討論如何利用 Azure AD Identity Protection 或其他 CSPM 工具自動化此類風險的識別。
    *   考慮如何在不破壞業務流程的前提下，定期輪換應用程式憑證。

### (6). 參考文獻：

*   **Microsoft Security Blog - AI-driven, large-scale nation-state campaign using ARTEX enables supply chain compromise:** [https://www.microsoft.com/security/blog/2026/10/21/ai-driven-large-scale-nation-state-campaign-using-artex-enables-supply-chain-compromise/](https://www.microsoft.com/security/blog/2026/10/21/ai-driven-large-scale-nation-state-campaign-using-artex-enables-supply-chain-compromise/)
*   **The Week Trust Broke: 8 Cyber Incidents That Made October 2026's Third Week Brutal:** [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaXpFn6kAFAVH2yqNqglS97gAJbOilsQLl4pTMh8P2teiiA4zUFaM2wnG4NQTp5yRQM8JBJ3fvWp9VOGrBRoMMv2k_KBrn3AUI_rgSFP2LYrVvvUK4VjLfHgqj-XnznHdhW84cQl225DtyxI4iU40vPIwq1cIByYsKOnYC1-WIVYtsx_R0zYuS3HHilzvEUURyyVDzkdE8kciWweZyEOLcSx4dI3Xx4fsjjTtY0k_-YQg1KpA==](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaXpFn6kAFAVH2yqNqglS97gAJbOilsQLl4pTMh8P2teiiA4zUFaM2wnG4NQTp5yRQM8JBJ3fvWp9VOGrBRoMMv2k_KBrn3AUI_rgSFP2LYrVvvUK4VjLfHgqj-XnznHdhW84cQl225DtyxI4iU40vPIwq1cIByYsKOnYC1-WIVYtsx_R0zYuS3HHilzvEUURyyVDzkdE8kciWweZyEOLcSx4dI3Xx4fsjjTtY0k_-YQg1KpA==)
*   **September 2026 Cyber Threats: ClickFix, AI & RMM | Blackpoint:** [https://www.blackpointcyber.com/resources/september-2026-cyber-threats-clickfix-ai-rmm](https://www.blackpointcyber.com/resources/september-2026-cyber-threats-clickfix-ai-rmm)
*   **The Month in Cyber: September 2026 - Unit 42 investigated an AI-directed intrusion:** [https://www.cybersecurity-magazine.com/articles/the-month-in-cyber-september-2026](https://www.cybersecurity-magazine.com/articles/the-month-in-cyber-september-2026)
*   **Threat Brief: Critical Vulnerabilities in PHP: CVE-2026-109618, CVE-2026-109619 (Updated October 25) - Palo Alto Networks Unit 42:** [https://unit42.paloaltonetworks.com/threat-brief-critical-vulnerabilities-in-php-cve-2026-109618-cve-2026-109619/](https://unit42.paloaltonetworks.com/threat-brief-critical-vulnerabilities-in-php-cve-2026-109618-cve-2026-109619/)