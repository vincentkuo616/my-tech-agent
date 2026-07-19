今日技術研究報告：工作軟體技術 (Software Technology)

針對您目前維護的 MESClient、CSS、ERP-Web、HKLogistics、LXKiosk 及 LCEPM 等專案，其技術棧涵蓋 ASP.NET Core (.NET 9) 至 .NET Framework 4.7.2，並廣泛使用 EF Core、Kendo UI、Hangfire、SignalR 等技術。考量這些系統的規模、複雜度及對效能、開發效率的需求，本次報告將聚焦於 **.NET 9 最新進展中的「原生 AOT 支援強化」** 與 **「Blazor 的漸進式增強 (Progressive Enhancements)」**。

---

### (1). 資料來源的可信程度：高

這些技術進展主要來自 Microsoft 官方的 .NET 部落格、GitHub 儲存庫發布說明，以及受信任的技術媒體報導和社群討論。這些來源是技術發布的第一手資料，具有最高的權威性和準確性。

---

### (2). 技術快訊：原生 AOT 支援強化 (Enhanced Native AOT Support) 與 Blazor 漸進式增強 (Progressive Enhancements)

#### **原生 AOT 支援強化**

在 .NET 9 的最新預覽版中，Microsoft 持續強化了 Native AOT (Ahead-of-Time Compilation) 的支援。這項技術允許開發者將 .NET 應用程式直接編譯成原生的機器碼，而非傳統的中介語言 (IL)。其核心目標是顯著提升應用程式的啟動速度、減少記憶體佔用，並提供更小的部署體積，同時也能提升一些執行時的效能。近期進展主要在於擴展對更多 ASP.NET Core 模式（如 Minimal APIs, gRPC）的支援度、改進診斷工具、以及解決相容性問題，使其更適合生產環境使用。

#### **Blazor 漸進式增強**

Blazor 作為 .NET 官方的全端 Web UI 框架，在 .NET 9 中持續獲得重大更新，特別是在「漸進式增強」方面。這包含對 Blazor Web App 中各種渲染模式（靜態伺服器端、互動式伺服器端、互動式 WebAssembly、自動模式）的無縫整合與優化。最新的更新讓開發者能更容易地在同一應用程式內，針對不同元件或頁面選擇最合適的渲染策略，同時改進了對 Web Components 的支援、預渲染 (prerendering) 效能，以及增強了對表單處理、路由和狀態管理的開發者體驗。這些改進旨在讓 Blazor 應用程式在啟動速度、使用者互動性與整體效能上達到最佳平衡。

---

### (3). 核心原理：結構化說明運作機制

#### **原生 AOT (Native Ahead-of-Time Compilation)**

*   **傳統模式 (JIT)：** 傳統 .NET 應用程式發佈時包含 IL (Intermediate Language) 程式碼。在運行時，CLR (Common Language Runtime) 中的 JIT (Just-In-Time) 編譯器會將 IL 實時編譯成機器碼並執行。這會導致首次啟動時間較長（JIT 編譯開銷），且記憶體中需同時存在 IL 和機器碼。
*   **AOT 編譯：** Native AOT 在編譯時期就將整個 .NET 應用程式 (包括框架函式庫) 編譯成特定平台和架構的原生機器碼。
*   **運作機制：**
    1.  **編譯階段：** .NET SDK (利用 LLVM 等工具鏈) 分析應用程式程式碼、依賴關係，並識別所有可能執行的程式碼路徑。它將這些路徑轉換為原生的 CPU 指令，並移除未使用的程式碼 (tree-shaking)。
    2.  **打包階段：** 生成一個單一的、獨立的可執行檔，其中包含了應用程式、運行時和所有依賴項的原生機器碼。
    3.  **運行階段：** 應用程式直接作為原生程序啟動，無需 JIT 編譯器，也無需 CLR 在後台進行複雜的運行時管理（但仍有輕量級的運行時支援，例如垃圾回收）。
*   **近期強化：** 提升了編譯器的智能性，能更好地處理反射 (Reflection)、泛型 (Generics) 和動態載入，這些曾是 Native AOT 的難點。擴展了對 ASP.NET Core Kestrel 伺服器和 Minimal APIs 的支援，讓更多 Web 工作負載能從 AOT 中受益。

#### **Blazor 漸進式增強 (Progressive Enhancements)**

*   **Blazor Web App 統一模型：** .NET 8 引入了 Blazor Web App，統一了 Blazor Server 和 Blazor WebAssembly 的開發模型。在 .NET 9 中，這個模型得到了進一步的精煉和優化。
*   **多重渲染模式：**
    *   **靜態伺服器端渲染 (Static Server-Side Rendering - SSR)：** 網頁在伺服器端生成 HTML 並直接發送給客戶端，首次載入速度快，適合內容展示頁面。
    *   **互動式伺服器端渲染 (Interactive Server-Side Rendering)：** 伺服器生成 HTML 後，透過 SignalR 維護與客戶端的連線，實現雙向即時互動，保持程式碼在伺服器端執行。
    *   **互動式 WebAssembly (Interactive WebAssembly - WebAssembly)：** 將 .NET 程式碼編譯成 WebAssembly，下載到客戶端瀏覽器執行，提供接近原生應用的互動體驗，但首次載入可能較慢。
    *   **自動模式 (Auto):** 智慧地在首次渲染時使用 Interactive Server 模式，後續下載 WebAssembly 到客戶端，切換到 Interactive WebAssembly 模式，以兼顧啟動速度和離線能力。
*   **漸進式運作機制：**
    1.  **頁面級/元件級控制：** 開發者可以在 Razor 頁面或 Blazor 元件層級，使用 `RenderMode` 屬性精確指定要採用的渲染模式，例如 `@rendermode InteractiveServer` 或 `@rendermode InteractiveWebAssembly`。
    2.  **混合應用：** 允許應用程式的大部分使用快速的靜態 SSR，而只有需要高度互動性的特定區域採用互動式模式。
    3.  **增強導航與表單：** 內建的導航和表單處理機制得到了優化，即使在部分互動模式下也能提供流暢的用戶體驗，例如無需完整頁面刷新即可提交表單或導航。
    4.  **Web Components 互操作性：** 增強了 Blazor 元件與標準 Web Components 的整合能力，方便將 Blazor 建立的組件嵌入其他框架，或在 Blazor 中使用現有的 Web Components。

---

### (4). 實戰建議：為什麼這對用戶有用？

#### **MESClient, CSS, LXKiosk (ASP.NET Core / .NET 9)**

*   **Native AOT:**
    *   **更快的啟動速度：** 對於這些可能需要快速響應的業務應用（特別是 MESClient 的現場作業 Kiosk 系統 LXKiosk），更快的應用程式啟動時間意味著操作員可以更快地投入工作，或在系統重啟後迅速恢復服務。
    *   **減少記憶體佔用：** 降低記憶體使用量對於資源有限的 Kiosk 設備 (LXKiosk) 或需要部署多個實例的 Web 應用程式 (MESClient, CSS) 尤其有利，可以提升部署密度和降低營運成本。
    *   **更小的部署體積：** 單一原生可執行檔，減少了部署複雜性，方便打包和分發。
    *   **潛在的安全性提升：** 原生編譯理論上可以讓逆向工程變得更困難一些，提供輕微的安全性提升 (雖然不能完全依賴)。
    *   **痛點解決：**
        *   **LXKiosk：** 設備記憶體與啟動速度限制。
        *   **MESClient/CSS：** 服務重啟後的恢復時間、資源利用效率。
*   **Blazor 漸進式增強:**
    *   **現代化前端體驗：** 雖然目前使用 Kendo UI + jQuery，但 Blazor 提供了完全基於 C# 的全端開發模式，可以考慮將新的功能模組或較小的子系統逐步遷移至 Blazor。
    *   **性能與互動性平衡：** 透過智慧選擇 SSR 或 WebAssembly 渲染模式，可以在首次載入速度和用戶互動流暢度之間取得最佳平衡，提升使用者體驗。對於像 CSS 的前台客戶入口，快速的首次載入和流暢的互動性至關重要。
    *   **漸進式導入：** 無需完全重寫現有應用程式。可以從小型元件或報表頁面開始嘗試 Blazor，利用 Web Components 互操作性將 Blazor 元件嵌入現有的 Razor View 中，逐步引入現代化技術。
    *   **痛點解決：**
        *   **MESClient/CSS：** 提升複雜前端模組的開發效率和可維護性，提供更現代化的互動體驗。

#### **ERP-Web, HKLogistics (ASP.NET MVC 5 / .NET Framework 4.7.2)**

*   **Native AOT (間接影響與未來規劃):**
    *   雖然這些舊系統不能直接受益於 Native AOT，但其強化暗示著 .NET Core/.NET 9 在性能和部署優勢上的巨大潛力。
    *   **增量現代化策略：** 可以考慮將這些大型系統中的特定「業務微服務」或「獨立功能模組」逐步抽離出來，用 ASP.NET Core (.NET 9) 和 Native AOT 重新實現，並通過 API 與現有舊系統通訊。例如，HKLogistics 的 GPS 資料匯入或 AI 路線規劃服務，未來可以考慮獨立為 AOT 編譯的微服務。
    *   **長期遷移目標：** 了解 Native AOT 的優勢有助於規劃未來的整體系統遷移策略和目標。
*   **Blazor 漸進式增強 (前端現代化策略):**
    *   **緩解前端技術債：** ERP-Web 和 HKLogistics 的前端仍基於 jQuery + Kendo UI + Bootstrap + ES5/ES6。Blazor 提供了一條清晰的現代化路徑。
    *   **新功能開發：** 建議未來所有新的功能模組，特別是那些需要豐富互動性的模組（如 ERP 的新看板、HKLogistics 的新司機任務介面），可以優先考慮使用 Blazor Web App 開發，並以 Web Components 的形式嵌入到現有的 MVC Razor View 中。
    *   **提升開發效率：** 全端 C# 語言統一，減少前後端上下文切換和技能棧要求，對於熟悉 .NET 的團隊而言，開發複雜 UI 的效率將顯著提升。
    *   **痛點解決：**
        *   **ERP-Web/HKLogistics：** 解決龐大前端程式碼的維護性和技術債問題，提供更具吸引力的使用者體驗。

---

### (5). Lab 提案（實作專案）：Blazor 漸進式 Web API Dashboard

**專案名稱：** `BlazorHybridDashboard`

**目標：** 學習如何在現有的 ASP.NET Core MVC 專案中，以「漸進式」的方式整合 Blazor Web App，並利用其互動能力建立一個輕量級的儀表板。此儀表板將透過 API 顯示模擬的即時數據，模擬 MESClient/CSS 中的看板或報表功能。

**預計時間：** 3-4 小時

**假設前提：** 您已安裝 .NET 9 SDK。

**實作步驟：**

1.  **建立 ASP.NET Core MVC 專案 (Host):**
    *   使用 .NET 9 建立一個新的 `ASP.NET Core Web App (MVC)` 專案，命名為 `MyWebApp`。
    *   確保專案已配置為使用控制器和視圖。

2.  **整合 Blazor Web App:**
    *   在 `MyWebApp` 專案中，加入 Blazor Web App 的支援：
        *   編輯 `MyWebApp.csproj`，在 `<PropertyGroup>` 中新增 `<EnableSdkWebAssemblyHost>true</EnableSdkWebAssemblyHost>`。
        *   在 `Program.cs` 中，加入 Blazor 相關服務和中介軟體：
            ```csharp
            builder.Services.AddRazorComponents()
                .AddInteractiveServerComponents()
                .AddInteractiveWebAssemblyComponents(); // 如果需要 Blazor WebAssembly 互動模式

            // ... (其他服務)

            app.MapRazorComponents<App>() // App 是一個 Blazor 根組件，稍後創建
                .AddInteractiveServerRenderMode()
                .AddInteractiveWebAssemblyRenderMode(); // 如果需要 WebAssembly
            ```
            *注意：此處 `App` 組件需要創建，它是 Blazor 的入口。*

3.  **建立 Blazor Root Component (App.razor):**
    *   在 `MyWebApp` 專案根目錄下，新增一個 `Components` 資料夾。
    *   在 `Components` 資料夾中，新增 `App.razor` 檔案：
        ```razor
        @using Microsoft.AspNetCore.Components.Web
        @namespace MyWebApp.Components
        @{
            Layout = typeof(Layout.MainLayout); // 稍後創建
        }
        <Router AppAssembly="@typeof(Program).Assembly">
            <Found Context="routeData">
                <RouteView RouteData="@routeData" DefaultLayout="@typeof(Layout.MainLayout)" />
                <FocusOnNavigate RouteData="@routeData" Selector="h1" />
            </Found>
            <NotFound>
                <PageTitle>Not found</PageTitle>
                <LayoutView Layout="@typeof(Layout.MainLayout)">
                    <p role="alert">Sorry, there's nothing at this address.</p>
                </LayoutView>
            </NotFound>
        </Router>
        ```
    *   在 `Components` 資料夾下，新增 `Layout` 資料夾，並創建 `MainLayout.razor` (基礎頁面佈局) 和 `NavMenu.razor` (導航選單)。您可以從預設的 Blazor 專案模板中複製這些檔案，或者簡化它們。

4.  **建立 Blazor Dashboard 元件：**
    *   在 `Components/Pages` 資料夾中，新增一個 `Dashboard.razor` 檔案。
    *   這個元件將透過 API 獲取數據並展示，可以包含 Kendo UI for Blazor 元件來模擬您現有的 Kendo UI 風格。
    *   **範例 `Dashboard.razor`:**
        ```razor
        @page "/dashboard"
        @using System.Net.Http.Json
        @using System.Text.Json.Serialization
        @inject HttpClient Http

        <PageTitle>Dashboard</PageTitle>

        <h1>MES Metrics Dashboard</h1>

        <p role="status">Current count: @_currentCount</p>
        <button class="btn btn-primary" @onclick="IncrementCount">Click me</button>

        @if (_forecasts == null)
        {
            <p><em>Loading...</em></p>
        }
        else
        {
            <h3>Weather Forecast</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Temp. (C)</th>
                        <th>Temp. (F)</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var forecast in _forecasts)
                    {
                        <tr>
                            <td>@forecast.Date.ToShortDateString()</td>
                            <td>@forecast.TemperatureC</td>
                            <td>@forecast.TemperatureF</td>
                            <td>@forecast.Summary</td>
                        </tr>
                    }
                </tbody>
            </table>
        }

        @code {
            private int _currentCount = 0;
            private WeatherForecast[] _forecasts;

            private void IncrementCount()
            {
                _currentCount++;
            }

            protected override async Task OnInitializedAsync()
            {
                // 模擬從 API 獲取數據
                _forecasts = await Http.GetFromJsonAsync<WeatherForecast[]>("api/WeatherForecast");
            }

            public class WeatherForecast
            {
                public DateOnly Date { get; set; }
                public int TemperatureC { get; set; }
                public string Summary { get; set; }
                public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
            }
        }
        ```
        *注意：`HttpClient` 需要在 `Program.cs` 中註冊，並且要有一個對應的 API Controller 提供數據。*

5.  **建立 API Controller (For Blazor Data Source):**
    *   在 `MyWebApp` 專案的 `Controllers` 資料夾中，新增 `WeatherForecastController.cs` (可以從預設 Web API 專案複製)。
    *   確保該 Controller 返回 Blazor 元件期望的 JSON 格式數據。

6.  **在 MVC View 中嵌入 Blazor 元件 (漸進式導入):**
    *   在 `Views/Home/Index.cshtml` 或任何您想要嵌入的 MVC View 中，使用 `<component>` Tag Helper 嵌入 Blazor 元件。
    *   **範例 `Index.cshtml`:**
        ```cshtml
        @{
            ViewData["Title"] = "Home Page";
        }

        <div class="text-center">
            <h1 class="display-4">Welcome to Hybrid App</h1>
            <p>Learn about <a href="https://learn.microsoft.com/aspnet/core">building Web apps with ASP.NET Core</a>.</p>
        </div>

        <h2>Blazor Dashboard (Embedded)</h2>
        @* 嵌入 Blazor Dashboard 元件 *@
        <component type="typeof(MyWebApp.Components.Pages.Dashboard)" render-mode="ServerPrerendered" />
        @* render-mode 可以是 ServerPrerendered, Server, WebAssembly, Auto, Static *戶端載入速度*@

        @* 必須確保 Blazor 的腳本被加載，通常在 _Layout.cshtml 底部 *@
        @section Scripts {
            <script src="_framework/blazor.web.js"></script>
        }
        ```
    *   確保 `_Layout.cshtml` 檔案中包含 `_framework/blazor.web.js` 腳本的引用，這對於 Blazor 互動性是必需的。

7.  **運行與測試：**
    *   執行專案，訪問首頁，您將看到傳統 MVC 內容旁邊嵌入了一個可互動的 Blazor 儀表板。點擊按鈕，觀察 Blazor 元件的狀態更新，而頁面其他部分保持不變。
    *   嘗試調整 `render-mode` 屬性，觀察不同模式下的行為和效能差異。

**學習重點：**
*   理解 Blazor Web App 如何與現有 ASP.NET Core MVC 專案共存。
*   掌握如何在 MVC View 中嵌入 Blazor 元件，實現漸進式前端現代化。
*   體驗 Blazor 的元件化開發模式和互動性。
*   思考如何將現有的 Kendo UI 或 jQuery 邏輯，逐步轉換為 Blazor 元件。

---

### (6). 參考文獻：

*   **.NET 9 預覽版資訊 (Native AOT & Blazor):**
    *   Microsoft .NET Blog - Announcing .NET 9 Preview X: 通常會詳細介紹每個預覽版的新特性，包括 Native AOT 和 Blazor 的改進。
        *   Example: [https://devblogs.microsoft.com/dotnet/](https://devblogs.microsoft.com/dotnet/) (此為通用部落格連結，需搜尋具體預覽版文章，例如 "Announcing .NET 9 Preview 4")
    *   GitHub .NET 儲存庫發布說明：提供更詳細的技術細節和變更日誌。
        *   Example: [https://github.com/dotnet/sdk/releases](https://github.com/dotnet/sdk/releases) (需查找對應 .NET 9 的發布版本)

*   **Native AOT 官方文件：**
    *   Native AOT deployment overview - .NET documentation: [https://learn.microsoft.com/dotnet/core/deploying/native-aot/](https://learn.microsoft.com/dotnet/core/deploying/native-aot/)
    *   ASP.NET Core support for native AOT - .NET documentation: [https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/native-aot](https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/native-aot)

*   **Blazor 官方文件：**
    *   ASP.NET Core Blazor overview - .NET documentation: [https://learn.microsoft.com/aspnet/core/blazor/](https://learn.microsoft.com/aspnet/core/blazor/)
    *   ASP.NET Core Blazor rendering modes - .NET documentation: [https://learn.microsoft.com/aspnet/core/blazor/components/render-modes](https://learn.microsoft.com/aspnet/core/blazor/components/render-modes)
    *   What's new in .NET 9 for ASP.NET Core Blazor: [https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/blazor](https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/blazor)

---

**補充說明：** 由於 `.NET 9` 目前仍處於預覽階段，其功能和 API 可能會有所變動。在生產環境中實施前，請務必參考最新的官方文件和發布說明。這個 Lab 提案旨在提供一個快速入門，讓您能親身體驗這些新技術的潛力。**今日技術研究報告：工作軟體技術 (Software Technology)**

針對您目前維護的 MESClient、CSS、ERP-Web、HKLogistics、LXKiosk 及 LCEPM 等專案，其技術棧涵蓋 ASP.NET Core (.NET 9) 至 .NET Framework 4.7.2，並廣泛使用 EF Core、Kendo UI、Hangfire、SignalR 等技術。考量這些系統的規模、複雜度及對效能、開發效率的需求，本次報告將聚焦於 **.NET 9 最新進展中的「原生 AOT 支援強化」** 與 **「Blazor 的漸進式增強 (Progressive Enhancements)」**。

---

### (1). 資料來源的可信程度：高

這些技術進展主要來自 Microsoft 官方的 .NET 部落格、GitHub 儲存庫發布說明，以及受信任的技術媒體報導和社群討論。這些來源是技術發布的第一手資料，具有最高的權威性和準確性。例如，.NET 9 Preview 5 和 Preview 6 的發布就直接來自 GitHub 討論區和 Microsoft 開發者部落格。

---

### (2). 技術快訊：原生 AOT 支援強化 (Enhanced Native AOT Support) 與 Blazor 漸進式增強 (Progressive Enhancements)

#### **原生 AOT 支援強化**

在 .NET 9 的最新預覽版中，Microsoft 持續強化了 Native AOT (Ahead-of-Time Compilation) 的支援。 這項技術允許開發者將 .NET 應用程式直接編譯成原生的機器碼，而非傳統的中介語言 (IL)。其核心目標是顯著提升應用程式的啟動速度、減少記憶體佔用，並提供更小的部署體積，同時也能提升一些執行時的效能。 近期進展主要在於擴展對更多 ASP.NET Core 模式（如 Minimal APIs, gRPC）的支援度、改進診斷工具、以及解決相容性問題，使其更適合生產環境使用。 .NET 9 中的 Native AOT 已經可以產生單一的、獨立的可執行檔，減少了部署複雜性。

#### **Blazor 漸進式增強**

Blazor 作為 .NET 官方的全端 Web UI 框架，在 .NET 9 中持續獲得重大更新，特別是在「漸進式增強」方面。 這包含對 Blazor Web App 中各種渲染模式（靜態伺服器端、互動式伺服器端、互動式 WebAssembly、自動模式）的無縫整合與優化。 最新的更新讓開發者能更容易地在同一應用程式內，針對不同元件或頁面選擇最合適的渲染策略，同時改進了對 Web Components 的支援、預渲染 (prerendering) 效能，以及增強了對表單處理、路由和狀態管理的開發者體驗。 這些改進旨在讓 Blazor 應用程式在啟動速度、使用者互動性與整體效能上達到最佳平衡。

---

### (3). 核心原理：結構化說明運作機制

#### **原生 AOT (Native Ahead-of-Time Compilation)**

*   **傳統模式 (JIT)：** 傳統 .NET 應用程式發佈時包含 IL (Intermediate Language) 程式碼。在運行時，CLR (Common Language Runtime) 中的 JIT (Just-In-Time) 編譯器會將 IL 實時編譯成機器碼並執行。這會導致首次啟動時間較長（JIT 編譯開銷），且記憶體中需同時存在 IL 和機器碼。
*   **AOT 編譯：** Native AOT 在編譯時期就將整個 .NET 應用程式 (包括框架函式庫) 編譯成特定平台和架構的原生機器碼。
*   **運作機制：**
    1.  **編譯階段：** .NET SDK (利用 LLVM 等工具鏈) 分析應用程式程式碼、依賴關係，並識別所有可能執行的程式碼路徑。它將這些路徑轉換為原生的 CPU 指令，並移除未使用的程式碼 (tree-shaking)。
    2.  **打包階段：** 生成一個單一的、獨立的可執行檔，其中包含了應用程式、運行時和所有依賴項的原生機器碼。
    3.  **運行階段：** 應用程式直接作為原生程序啟動，無需 JIT 編譯器，也無需 CLR 在後台進行複雜的運行時管理（但仍有輕量級的運行時支援，例如垃圾回收）。
*   **近期強化：** .NET 9 提升了編譯器的智能性，能更好地處理反射 (Reflection)、泛型 (Generics) 和動態載入，這些曾是 Native AOT 的難點。 擴展了對 ASP.NET Core Kestrel 伺服器和 Minimal APIs 的支援，讓更多 Web 工作負載能從 AOT 中受益。 此外，.NET 9 的 runtime 包含了對 ARM64 程式碼生成、程式碼佈局、循環優化等方面的性能提升，進一步增強了 Native AOT 的效率。

#### **Blazor 漸進式增強 (Progressive Enhancements)**

*   **Blazor Web App 統一模型：** .NET 8 引入了 Blazor Web App，統一了 Blazor Server 和 Blazor WebAssembly 的開發模型。 在 .NET 9 中，這個模型得到了進一步的精煉和優化。
*   **多重渲染模式：**
    *   **靜態伺服器端渲染 (Static Server-Side Rendering - SSR)：** 網頁在伺服器端生成 HTML 並直接發送給客戶端，首次載入速度快，適合內容展示頁面。
    *   **互動式伺服器端渲染 (Interactive Server-Side Rendering)：** 伺服器生成 HTML 後，透過 SignalR 維護與客戶端的連線，實現雙向即時互動，保持程式碼在伺服器端執行。
    *   **互動式 WebAssembly (Interactive WebAssembly - WebAssembly)：** 將 .NET 程式碼編譯成 WebAssembly，下載到客戶端瀏覽器執行，提供接近原生應用的互動體驗，但首次載入可能較慢。
    *   **自動模式 (Auto):** 智慧地在首次渲染時使用 Interactive Server 模式，後續下載 WebAssembly 到客戶端，切換到 Interactive WebAssembly 模式，以兼顧啟動速度和離線能力。
*   **漸進式運作機制：**
    1.  **頁面級/元件級控制：** 開發者可以在 Razor 頁面或 Blazor 元件層級，使用 `RenderMode` 屬性精確指定要採用的渲染模式，例如 `@rendermode InteractiveServer` 或 `@rendermode InteractiveWebAssembly`。
    2.  **混合應用：** 允許應用程式的大部分使用快速的靜態 SSR，而只有需要高度互動性的特定區域採用互動式模式。
    3.  **增強導航與表單：** 內建的導航和表單處理機制得到了優化，即使在部分互動模式下也能提供流暢的用戶體驗，例如無需完整頁面刷新即可提交表單或導航。
    4.  **Web Components 互操作性：** .NET MAUI Blazor Hybrid 應用程式的模板，顯示了 Blazor 與其他 Web 應用程序的混合能力。

---

### (4). 實戰建議：為什麼這對用戶有用？

#### **MESClient, CSS, LXKiosk (ASP.NET Core / .NET 9)**

*   **Native AOT:**
    *   **更快的啟動速度：** 對於這些可能需要快速響應的業務應用（特別是 MESClient 的現場作業 Kiosk 系統 LXKiosk），更快的應用程式啟動時間意味著操作員可以更快地投入工作，或在系統重啟後迅速恢復服務。
    *   **減少記憶體佔用：** 降低記憶體使用量對於資源有限的 Kiosk 設備 (LXKiosk) 或需要部署多個實例的 Web 應用程式 (MESClient, CSS) 尤其有利，可以提升部署密度和降低營運成本。
    *   **更小的部署體積：** 單一原生可執行檔，減少了部署複雜性，方便打包和分發。
    *   **潛在的安全性提升：** 原生編譯理論上可以讓逆向工程變得更困難一些，提供輕微的安全性提升 (雖然不能完全依賴)。
    *   **痛點解決：**
        *   **LXKiosk：** 設備記憶體與啟動速度限制。
        *   **MESClient/CSS：** 服務重啟後的恢復時間、資源利用效率。
*   **Blazor 漸進式增強:**
    *   **現代化前端體驗：** 雖然目前使用 Kendo UI + jQuery，但 Blazor 提供了完全基於 C# 的全端開發模式，可以考慮將新的功能模組或較小的子系統逐步遷移至 Blazor。
    *   **性能與互動性平衡：** 透過智慧選擇 SSR 或 WebAssembly 渲染模式，可以在首次載入速度和用戶互動流暢度之間取得最佳平衡，提升使用者體驗。 對於像 CSS 的前台客戶入口，快速的首次載入和流暢的互動性至關重要。
    *   **漸進式導入：** 無需完全重寫現有應用程式。可以從小型元件或報表頁面開始嘗試 Blazor，利用 Web Components 互操作性將 Blazor 元件嵌入現有的 Razor View 中，逐步引入現代化技術。
    *   **痛點解決：**
        *   **MESClient/CSS：** 提升複雜前端模組的開發效率和可維護性，提供更現代化的互動體驗。

#### **ERP-Web, HKLogistics (ASP.NET MVC 5 / .NET Framework 4.7.2)**

*   **Native AOT (間接影響與未來規劃):**
    *   雖然這些舊系統不能直接受益於 Native AOT，但其強化暗示著 .NET Core/.NET 9 在性能和部署優勢上的巨大潛力。
    *   **增量現代化策略：** 可以考慮將這些大型系統中的特定「業務微服務」或「獨立功能模組」逐步抽離出來，用 ASP.NET Core (.NET 9) 和 Native AOT 重新實現，並通過 API 與現有舊系統通訊。例如，HKLogistics 的 GPS 資料匯入或 AI 路線規劃服務，未來可以考慮獨立為 AOT 編譯的微服務。
    *   **長期遷移目標：** 了解 Native AOT 的優勢有助於規劃未來的整體系統遷移策略和目標。
*   **Blazor 漸進式增強 (前端現代化策略):**
    *   **緩解前端技術債：** ERP-Web 和 HKLogistics 的前端仍基於 jQuery + Kendo UI + Bootstrap + ES5/ES6。Blazor 提供了一條清晰的現代化路徑。
    *   **新功能開發：** 建議未來所有新的功能模組，特別是那些需要豐富互動性的模組（如 ERP 的新看板、HKLogistics 的新司機任務介面），可以優先考慮使用 Blazor Web App 開發，並以 Web Components 的形式嵌入到現有的 MVC Razor View 中。
    *   **提升開發效率：** 全端 C# 語言統一，減少前後端上下文切換和技能棧要求，對於熟悉 .NET 的團隊而言，開發複雜 UI 的效率將顯著提升。
    *   **痛點解決：**
        *   **ERP-Web/HKLogistics：** 解決龐大前端程式碼的維護性和技術債問題，提供更具吸引力的使用者體驗。

---

### (5). Lab 提案（實作專案）：Blazor 漸進式 Web API Dashboard

**專案名稱：** `BlazorHybridDashboard`

**目標：** 學習如何在現有的 ASP.NET Core MVC 專案中，以「漸進式」的方式整合 Blazor Web App，並利用其互動能力建立一個輕量級的儀表板。此儀表板將透過 API 顯示模擬的即時數據，模擬 MESClient/CSS 中的看板或報表功能。

**預計時間：** 3-4 小時

**假設前提：** 您已安裝 .NET 9 SDK。

**實作步驟：**

1.  **建立 ASP.NET Core MVC 專案 (Host):**
    *   使用 .NET 9 建立一個新的 `ASP.NET Core Web App (MVC)` 專案，命名為 `MyWebApp`。
    *   確保專案已配置為使用控制器和視圖。

2.  **整合 Blazor Web App:**
    *   在 `MyWebApp` 專案中，加入 Blazor Web App 的支援：
        *   編輯 `MyWebApp.csproj`，在 `<PropertyGroup>` 中新增 `<EnableSdkWebAssemblyHost>true</EnableSdkWebAssemblyHost>`。
        *   在 `Program.cs` 中，加入 Blazor 相關服務和中介軟體：
            ```csharp
            builder.Services.AddRazorComponents()
                .AddInteractiveServerComponents()
                .AddInteractiveWebAssemblyComponents(); // 如果需要 Blazor WebAssembly 互動模式

            // ... (其他服務)

            app.MapRazorComponents<App>() // App 是一個 Blazor 根組件，稍後創建
                .AddInteractiveServerRenderMode()
                .AddInteractiveWebAssemblyRenderMode(); // 如果需要 WebAssembly
            ```
            *注意：此處 `App` 組件需要創建，它是 Blazor 的入口。*

3.  **建立 Blazor Root Component (App.razor):**
    *   在 `MyWebApp` 專案根目錄下，新增一個 `Components` 資料夾。
    *   在 `Components` 資料夾中，新增 `App.razor` 檔案：
        ```razor
        @using Microsoft.AspNetCore.Components.Web
        @namespace MyWebApp.Components
        @{
            Layout = typeof(Layout.MainLayout); // 稍後創建
        }
        <Router AppAssembly="@typeof(Program).Assembly">
            <Found Context="routeData">
                <RouteView RouteData="@routeData" DefaultLayout="@typeof(Layout.MainLayout)" />
                <FocusOnNavigate RouteData="@routeData" Selector="h1" />
            </Found>
            <NotFound>
                <PageTitle>Not found</PageTitle>
                <LayoutView Layout="@typeof(Layout.MainLayout)">
                    <p role="alert">Sorry, there's nothing at this address.</p>
                </LayoutView>
            </NotFound>
        </Router>
        ```
    *   在 `Components` 資料夾下，新增 `Layout` 資料夾，並創建 `MainLayout.razor` (基礎頁面佈局) 和 `NavMenu.razor` (導航選單)。您可以從預設的 Blazor 專案模板中複製這些檔案，或者簡化它們。

4.  **建立 Blazor Dashboard 元件：**
    *   在 `Components/Pages` 資料夾中，新增一個 `Dashboard.razor` 檔案。
    *   這個元件將透過 API 獲取數據並展示，可以包含 Kendo UI for Blazor 元件來模擬您現有的 Kendo UI 風格。
    *   **範例 `Dashboard.razor`:**
        ```razor
        @page "/dashboard"
        @using System.Net.Http.Json
        @using System.Text.Json.Serialization
        @inject HttpClient Http

        <PageTitle>Dashboard</PageTitle>

        <h1>MES Metrics Dashboard</h1>

        <p role="status">Current count: @_currentCount</p>
        <button class="btn btn-primary" @onclick="IncrementCount">Click me</button>

        @if (_forecasts == null)
        {
            <p><em>Loading...</em></p>
        }
        else
        {
            <h3>Weather Forecast</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Temp. (C)</th>
                        <th>Temp. (F)</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var forecast in _forecasts)
                    {
                        <tr>
                            <td>@forecast.Date.ToShortDateString()</td>
                            <td>@forecast.TemperatureC</td>
                            <td>@forecast.TemperatureF</td>
                            <td>@forecast.Summary</td>
                        </tr>
                    }
                </tbody>
            </table>
        }

        @code {
            private int _currentCount = 0;
            private WeatherForecast[] _forecasts;

            private void IncrementCount()
            {
                _currentCount++;
            }

            protected override async Task OnInitializedAsync()
            {
                // 模擬從 API 獲取數據
                _forecasts = await Http.GetFromJsonAsync<WeatherForecast[]>("api/WeatherForecast");
            }

            public class WeatherForecast
            {
                public DateOnly Date { get; set; }
                public int TemperatureC { get; set; }
                public string Summary { get; set; }
                public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
            }
        }
        ```
        *注意：`HttpClient` 需要在 `Program.cs` 中註冊，並且要有一個對應的 API Controller 提供數據。*

5.  **建立 API Controller (For Blazor Data Source):**
    *   在 `MyWebApp` 專案的 `Controllers` 資料夾中，新增 `WeatherForecastController.cs` (可以從預設 Web API 專案複製)。
    *   確保該 Controller 返回 Blazor 元件期望的 JSON 格式數據。

6.  **在 MVC View 中嵌入 Blazor 元件 (漸進式導入):**
    *   在 `Views/Home/Index.cshtml` 或任何您想要嵌入的 MVC View 中，使用 `<component>` Tag Helper 嵌入 Blazor 元件。
    *   **範例 `Index.cshtml`:**
        ```cshtml
        @{
            ViewData["Title"] = "Home Page";
        }

        <div class="text-center">
            <h1 class="display-4">Welcome to Hybrid App</h1>
            <p>Learn about <a href="https://learn.microsoft.com/aspnet/core">building Web apps with ASP.NET Core</a>.</p>
        </div>

        <h2>Blazor Dashboard (Embedded)</h2>
        @* 嵌入 Blazor Dashboard 元件 *@
        <component type="typeof(MyWebApp.Components.Pages.Dashboard)" render-mode="ServerPrerendered" />
        @* render-mode 可以是 ServerPrerendered, Server, WebAssembly, Auto, Static *戶端載入速度*@

        @* 必須確保 Blazor 的腳本被加載，通常在 _Layout.cshtml 底部 *@
        @section Scripts {
            <script src="_framework/blazor.web.js"></script>
        }
        ```
    *   確保 `_Layout.cshtml` 檔案中包含 `_framework/blazor.web.js` 腳本的引用，這對於 Blazor 互動性是必需的。

7.  **運行與測試：**
    *   執行專案，訪問首頁，您將看到傳統 MVC 內容旁邊嵌入了一個可互動的 Blazor 儀表板。點擊按鈕，觀察 Blazor 元件的狀態更新，而頁面其他部分保持不變。
    *   嘗試調整 `render-mode` 屬性，觀察不同模式下的行為和效能差異。

**學習重點：**
*   理解 Blazor Web App 如何與現有 ASP.NET Core MVC 專案共存。
*   掌握如何在 MVC View 中嵌入 Blazor 元件，實現漸進式前端現代化。
*   體驗 Blazor 的元件化開發模式和互動性。
*   思考如何將現有的 Kendo UI 或 jQuery 邏輯，逐步轉換為 Blazor 元件。

---

### (6). 參考文獻：

*   **.NET 9 預覽版資訊 (Native AOT & Blazor):**
    *   Microsoft .NET Blog - Announcing .NET 9 Preview X: [https://devblogs.microsoft.com/dotnet/](https://devblogs.microsoft.com/dotnet/) (此為通用部落格連結，需搜尋具體預覽版文章，例如 "Announcing .NET 9 Preview 4", "Announcing .NET 9 Preview 5", "Announcing .NET 9 Preview 6")
    *   GitHub .NET 儲存庫發布說明： [https://github.com/dotnet/sdk/releases](https://github.com/dotnet/sdk/releases) (需查找對應 .NET 9 的發布版本)

*   **Native AOT 官方文件：**
    *   Native AOT deployment overview - .NET documentation: [https://learn.microsoft.com/dotnet/core/deploying/native-aot/](https://learn.microsoft.com/dotnet/core/deploying/native-aot/)
    *   ASP.NET Core support for native AOT - .NET documentation: [https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/native-aot](https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/native-aot)

*   **Blazor 官方文件：**
    *   ASP.NET Core Blazor overview - .NET documentation: [https://learn.microsoft.com/aspnet/core/blazor/](https://learn.microsoft.com/aspnet/core/blazor/)
    *   ASP.NET Core Blazor rendering modes - .NET documentation: [https://learn.microsoft.com/aspnet/core/blazor/components/render-modes](https://learn.microsoft.com/aspnet/core/blazor/components/render-modes)
    *   What's new in .NET 9 for ASP.NET Core Blazor: [https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/blazor](https://learn.microsoft.com/aspnet/core/whats-new/dotnet-9/blazor)

---

**補充說明：** 由於 `.NET 9` 目前仍處於預覽階段，其功能和 API 可能會有所變動。在生產環境中實施前，請務必參考最新的官方文件和發布說明。這個 Lab 提案旨在提供一個快速入門，讓您能親身體驗這些新技術的潛力。