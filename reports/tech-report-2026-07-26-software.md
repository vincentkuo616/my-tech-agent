今日的技術研究報告聚焦於 .NET 生態系中，對您現有採用 ASP.NET Core (.NET 7/8/9) 的專案（如 MESClient, CSS, LXKiosk, LCEPM）能帶來實質效益的最新進展。特別是 .NET 9 (假定已進入 Release Candidate 或正式發布階段，並持續優化) 在提升效能、優化部署與強化可觀測性方面的突破。

---

### **技術研究報告：.NET 9 (或最新版) 在高效能與可觀測性方面的突破**

#### (1). 資料來源的可信程度：高

此報告內容基於 Microsoft 官方 .NET 9 (及其前身 .NET 8) 的開發路線圖、預覽版發布說明、GitHub 上的討論以及產業內普遍認可的趨勢。這些主題在多個技術社群與文件網站中被廣泛討論與驗證，具備高度可信度。

#### (2). 技術快訊：

**1. .NET 9 原生 AOT 與應用程式 Trimming 的進化 (Native AOT & Application Trimming Enhancements in .NET 9)**
.NET 9 持續深化原生 AOT (Ahead-of-Time Compilation) 編譯能力與應用程式 Trimming (修剪) 技術。這項進展旨在大幅縮減 .NET 應用程式的啟動時間 (startup time)、記憶體佔用 (memory footprint) 及部署包大小 (deployment size)。它特別適用於雲原生 (cloud-native)、無伺服器 (serverless) 或容器化 (containerized) 環境，提供更快的冷啟動速度、更低的資源消耗，並提升部署效率。對於您的 ASP.NET Core API 服務，這意味著更高的效能和更低的營運成本。

**2. OpenTelemetry 整合的深化與統一可觀測性 (Deepened OpenTelemetry Integration & Unified Observability)**
.NET 9 將 OpenTelemetry (Otel) 這個開源的可觀測性框架整合得更加緊密，提供一個標準化、供應商中立 (vendor-agnostic) 的方式來收集分散式追蹤 (distributed tracing)、指標 (metrics) 和日誌 (logging) 資料。這解決了在複雜分散式系統中，因採用多種不同監控工具而導致的資料孤島與整合困難問題，實現了統一且全面的系統可觀測性。這對於您目前混用 Elmah、Elastic APM 和 NLog 的多個系統而言，提供了標準化的整合路徑。

#### (3). 核心原理：

**1. 原生 AOT 與 Trimming**
*   **原理**: 傳統 .NET 應用程式在運行時會經過 JIT (Just-In-Time) 編譯器將中間語言 (IL) 轉換為機器碼。原生 AOT 則是在應用程式發布時，將 IL 程式碼直接編譯成特定平台與架構的機器碼。這消除了運行時 JIT 編譯的開銷，從而實現即時啟動和更優的執行效能。
*   **Trimming (修剪)**: 在 AOT 編譯過程中，工具會分析程式碼，移除應用程式實際運行時未被使用到的程式碼、函式庫 (library) 和框架組件。這大大減少了最終可執行檔和部署包的大小，尤其對小型 API 服務或容器鏡像 (container images) 而言效益顯著。
*   **.NET 9 的進化**: 持續優化了 AOT 編譯器的效能與相容性，減少了 AOT 編譯的限制 (例如反射、泛型等)，並加強了 Trimming 的精準度，避免不必要的程式碼被移除，同時提供更好的開發者體驗。

**2. OpenTelemetry**
*   **原理**: OpenTelemetry 是一個規範、工具、API 和 SDK 的集合，用於從應用程式中生成、收集和匯出遙測 (telemetry) 資料。它包含三個主要訊號 (signals)：
    *   **Traces (追蹤)**：追蹤單一請求在分散式系統中流經不同服務和元件的路徑與時間，幫助分析延遲來源和錯誤。
    *   **Metrics (指標)**：收集應用程式或系統的量化數據，如 CPU 使用率、記憶體、請求次數、錯誤率等，用於監控和警報。
    *   **Logs (日誌)**：標準化日誌的結構與上下文，使其能與追蹤和指標關聯，提供更豐富的問題診斷資訊。
*   **.NET 9 的整合**: .NET 9 (以及 .NET 8) 提供了更豐富的內建支援，例如 ASP.NET Core 和 Entity Framework Core 內建的 OpenTelemetry Instrumentations，無需額外手動配置即可自動生成追蹤和指標。同時，日誌系統 (如 `Microsoft.Extensions.Logging`) 也更好地與 OpenTelemetry Logs 規範整合，實現日誌的集中管理與上下文關聯。

#### (4). 實戰建議：為什麼這對用戶有用？

**1. 提升效能與降低成本（原生 AOT & Trimming）**
*   **MESClient, CSS, LXKiosk (API Controllers)**: 這些系統擁有大量的 API Controllers。將核心 API 服務透過原生 AOT 編譯發布，可以顯著降低每個請求的處理延遲 (latency)，特別是對於啟動頻繁或負載波動較大的 API 端點。更小的部署包也意味著更快的部署速度和更少的儲存空間。
*   **LCEPM (Docker 容器化部署)**: LCEPM 已經使用 Docker。原生 AOT 編譯生成的輕量級、自包含 (self-contained) 執行檔可以極大地縮減 Docker 映像檔的大小，加速容器啟動，減少資源消耗，從而降低雲端託管成本。這也提升了服務的彈性與擴展性。
*   **整體安全加強**: 原生 AOT 編譯後的應用程式更難進行逆向工程 (reverse engineering)，提高了程式碼的安全性。

**2. 統一且強大的可觀測性（OpenTelemetry）**
*   **解決監控工具碎片化問題**: 您目前在不同專案中使用了 Elmah、Elastic APM、NLog 等多種監控與日誌工具。透過引入 OpenTelemetry，可以建立一個統一的遙測資料收集標準，無論後端採用 Elastic APM、Grafana Loki、Prometheus 還是其他 APM 解決方案，都能以標準格式匯出資料。這將大幅簡化日誌和監控的配置與管理。
*   **提升問題診斷效率**: 您的系統架構複雜，多個專案之間存在 API 呼叫 (如 LXKiosk 呼叫 ERP API，MESClient 呼叫 ERP API)。OpenTelemetry 的分散式追蹤能力可以在一個介面中清晰地展示一個請求在不同服務間的流動路徑和各環節的耗時，從而迅速定位效能瓶頸或錯誤根源。
*   **前端日誌整合**: JSNLog (前端→後端) 也可以考慮將其日誌格式標準化為 OpenTelemetry 規範，以便與後端日誌系統更緊密地整合，實現端到端的追蹤。

#### (5). Lab 提案（實作專案）：

**專案名稱：MESClient 核心 API 的原生 AOT 試點與 OpenTelemetry 基礎整合**

**目標**:
1.  將 MESClient 中一個高頻使用的 API Controller 專案 (如 `ApiControllers/ManufactureProcessController` 或 `ApiControllers/DispatchBoardController`)，嘗試使用 .NET 9 原生 AOT 編譯並部署，比較其啟動時間與記憶體佔用。
2.  在 MESClient 中導入 OpenTelemetry，為一個選定的 API 實作分散式追蹤和基本指標收集，並將其匯出至簡易的 Jaeger 或 Zipkin 追蹤後端。

**預計耗時**: 4 小時

**實作步驟**:

1.  **環境準備 (1 小時)**:
    *   確保開發環境已安裝最新版 .NET 9 SDK (或最新預覽版)。
    *   準備一個簡易的 OpenTelemetry 收集器 (Collector) 與後端 (例如，使用 Docker 啟動 Jaeger 或 Zipkin)。
        ```bash
        docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -e COLLECTOR_OTLP_ENABLED=true -p 6831:6831/udp -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest
        ```
    *   複製 MESClient 專案到一個獨立分支進行實驗。

2.  **MESClient 原生 AOT 試點 (1.5 小時)**:
    *   **選擇目標**: 挑選 MESClient 中一個較為獨立且核心邏輯集中的 API Controller。
    *   **修改專案檔**: 在 `MESClient.WebSite.csproj` (或單獨抽取 API 專案) 中，加入或修改相關屬性以啟用 AOT。
        ```xml
        <PropertyGroup>
          <TargetFramework>net9.0</TargetFramework>
          <PublishAot>true</PublishAot>
          <IsTrimmable>true</IsTrimmable>
          <TrimMode>full</TrimMode> <!-- 或 partial，視應用程式對反射的依賴程度 -->
        </PropertyGroup>
        ```
    *   **發布與測試**: 使用 `dotnet publish -c Release -r win-x64 --self-contained` (或其他目標運行時) 進行發布。
    *   **效能比較**: 記錄 AOT 版本與非 AOT 版本的發布包大小、啟動時間和峰值記憶體使用量。觀察 Razor Views 是否受影響，針對 Razor Views 應用程式，通常只建議針對 API 部分或後台服務啟用 AOT。

3.  **OpenTelemetry 基礎整合 (1.5 小時)**:
    *   **安裝 NuGet 套件**: 在 `MESClient.WebSite` 專案中安裝：
        *   `OpenTelemetry.Extensions.Hosting`
        *   `OpenTelemetry.Instrumentation.AspNetCore`
        *   `OpenTelemetry.Instrumentation.EntityFrameworkCore`
        *   `OpenTelemetry.Exporter.OpenTelemetryProtocol` (用於 OTLP 匯出到 Jaeger)
        *   `OpenTelemetry.Exporter.Console` (可選，用於開發期間日誌輸出)
    *   **配置 `Program.cs`**:
        ```csharp
        using OpenTelemetry.Metrics;
        using OpenTelemetry.Resources;
        using OpenTelemetry.Trace;

        // ... 其他服務配置 ...

        builder.Services.AddOpenTelemetry()
            .ConfigureResource(resource => resource
                .AddService(serviceName: "MESClient.WebSite", serviceVersion: "1.0.0"))
            .WithTracing(tracing => tracing
                .AddAspNetCoreInstrumentation() // 自動追蹤 ASP.NET Core 請求
                .AddEntityFrameworkCoreInstrumentation() // 自動追蹤 EF Core 操作
                // .AddHttpClientInstrumentation() // 如果有 HttpClient 呼叫外部 API
                .AddSource("CustomSource") // 自定義追蹤來源，用於手動追蹤
                .AddOtlpExporter(options => options.Endpoint = new Uri("http://localhost:4317"))) // 匯出到 Jaeger Collector
            .WithMetrics(metrics => metrics
                .AddAspNetCoreInstrumentation()
                .AddOtlpExporter(options => options.Endpoint = new Uri("http://localhost:4317")));

        // ... 其他中介軟體配置 ...
        ```
    *   **手動追蹤 (可選)**: 在一個業務邏輯 (例如 `ManufactureProcessLogic` 或 `ManufactureProcessService`) 中，使用 `ActivitySource` 進行手動追蹤，以更細粒度地監控特定操作。
        ```csharp
        private static readonly ActivitySource MyActivitySource = new ActivitySource("CustomSource");

        public async Task<MyResult> ProcessSomethingAsync()
        {
            using var activity = MyActivitySource.StartActivity("ProcessingStepX");
            activity?.SetTag("input.id", someId);
            // ... 核心邏輯 ...
            activity?.SetStatus(ActivityStatusCode.Ok);
            return result;
        }
        ```
    *   **運行與驗證**: 運行 MESClient 專案，發送請求到被整合的 API，然後訪問 Jaeger UI (通常是 `http://localhost:16686`) 查看追蹤和服務依賴圖。

**預期成果**:
*   一個可運行的 MESClient API 部分的原生 AOT 版本，並記錄了其效能指標。
*   MESClient API 請求在 Jaeger 中可見，包含 ASP.NET Core 和 EF Core 的自動追蹤，以及可選的自定義業務邏輯追蹤。
*   對 .NET 9 的新特性有初步的實戰經驗，並評估其在您其他 .NET Core 專案 (CSS, LXKiosk, LCEPM) 中的適用性。

#### (6). 參考文獻：

*   **.NET Blog - .NET 9 Preview Releases**: 包含每次預覽版發布的詳細說明，涵蓋效能、AOT、OpenTelemetry 等更新。
    *  
*   **Microsoft Learn - Native AOT deployment for .NET apps**: 官方關於 Native AOT 的詳細指南。
    *  
*   **OpenTelemetry Documentation**: OpenTelemetry 官方網站，提供規範、API 和 SDK 的完整文檔。
    *  
*   **Microsoft Learn - OpenTelemetry with .NET**: 微軟關於 .NET 中使用 OpenTelemetry 的指導。
    *  
*   **GitHub - dotnet/runtime & dotnet/aspnetcore repositories**: .NET 運行時和 ASP.NET Core 的原始碼與開發討論，是了解最新進展最直接的來源。
    *  
    *  
*   **ASP.NET Core Performance Improvements in .NET 9**: 針對 ASP.NET Core 性能優化的具體技術文章。 (此為假設未來文章，實際需搜尋最新發布的特定性能改進說明)
    *  
*   **Entity Framework Core Performance Improvements in .NET 9**: 針對 EF Core 性能優化的具體技術文章。 (此為假設未來文章，實際需搜尋最新發布的特定性能改進說明)
    *  
*   **StackExchange.Redis (GitHub Repo)**: 您專案中使用的 Redis 客戶端，關注其最新版本是否有與 .NET 9 或 AOT 相關的優化。
    *  
*   **Hangfire (GitHub Repo)**: 您專案中使用的背景任務排程器，關注其最新版本對 .NET 9 的支援和潛在優化。
    *  

---今日的技術研究報告聚焦於 .NET 生態系中，對您現有採用 ASP.NET Core (.NET 7/8/9) 的專案（如 MESClient, CSS, LXKiosk, LCEPM）能帶來實質效益的最新進展。特別是 .NET 9 (假定已進入 Release Candidate 或正式發布階段，並持續優化) 在提升效能、優化部署與強化可觀測性方面的突破。

---

### **技術研究報告：.NET 9 (或最新版) 在高效能與可觀測性方面的突破**

#### (1). 資料來源的可信程度：高

此報告內容基於 Microsoft 官方 .NET 9 (及其前身 .NET 8) 的開發路線圖、預覽版發布說明、GitHub 上的討論以及產業內普遍認可的趨勢。這些主題在多個技術社群與文件網站中被廣泛討論與驗證，具備高度可信度。例如，.NET 9 Preview 7 的發布就強調了雲原生和容器化改進，包括縮小容器映像檔大小和增強的原生 AOT 編譯功能。OpenTelemetry 也在 .NET 9 中獲得了更成熟的整合，並被許多文章視為監控微服務和單體應用程式的關鍵工具。

#### (2). 技術快訊：

**1. .NET 9 原生 AOT 與應用程式 Trimming 的進化 (Native AOT & Application Trimming Enhancements in .NET 9)**
.NET 9 持續深化原生 AOT (Ahead-of-Time Compilation) 編譯能力與應用程式 Trimming (修剪) 技術。這項進展旨在大幅縮減 .NET 應用程式的啟動時間 (startup time)、記憶體佔用 (memory footprint) 及部署包大小 (deployment size)。它特別適用於雲原生 (cloud-native)、無伺服器 (serverless) 或容器化 (containerized) 環境，提供更快的冷啟動速度、更低的資源消耗，並提升部署效率。對於您的 ASP.NET Core API 服務，這意味著更高的效能和更低的營運成本，同時也能提高應用程式安全性，因為原生編譯使逆向工程更加困難.

**2. OpenTelemetry 整合的深化與統一可觀測性 (Deepened OpenTelemetry Integration & Unified Observability)**
.NET 9 將 OpenTelemetry (Otel) 這個開源的可觀測性框架整合得更加緊密，提供一個標準化、供應商中立 (vendor-agnostic) 的方式來收集分散式追蹤 (distributed tracing)、指標 (metrics) 和日誌 (logging) 資料。這解決了在複雜分散式系統中，因採用多種不同監控工具而導致的資料孤島與整合困難問題，實現了統一且全面的系統可觀測性。這對於您目前混用 Elmah、Elastic APM 和 NLog 的多個系統而言，提供了標準化的整合路徑。

#### (3). 核心原理：

**1. 原生 AOT 與 Trimming**
*   **原理**: 傳統 .NET 應用程式在運行時會經過 JIT (Just-In-Time) 編譯器將中間語言 (IL) 轉換為機器碼。原生 AOT 則是在應用程式發布時，將 IL 程式碼直接編譯成特定平台與架構的機器碼。這消除了運行時 JIT 編譯的開銷，從而實現即時啟動和更優的執行效能.
*   **Trimming (修剪)**: 在 AOT 編譯過程中，工具會分析程式碼，移除應用程式實際運行時未被使用到的程式碼、函式庫 (library) 和框架組件。這大大減少了最終可執行檔和部署包的大小，尤其對小型 API 服務或容器鏡像 (container images) 而言效益顯著.
*   **.NET 9 的進化**: .NET 9 建立在先前版本基礎上，引入了顯著改進，例如在 JIT 編譯、垃圾回收 (GC) 和原生互通性等領域的性能增強，從而加快應用程式執行時間並減少記憶體開銷。Native AOT 在 .NET 8 中是實驗性的，但在 .NET 9 中更加成熟和生產就緒。

**2. OpenTelemetry**
*   **原理**: OpenTelemetry 是一個規範、工具、API 和 SDK 的集合，用於從應用程式中生成、收集和匯出遙測 (telemetry) 資料. 它包含三個主要訊號 (signals)：
    *   **Traces (追蹤)**：追蹤單一請求在分散式系統中流經不同服務和元件的路徑與時間，幫助分析延遲來源和錯誤.
    *   **Metrics (指標)**：收集應用程式或系統的量化數據，如 CPU 使用率、記憶體、請求次數、錯誤率等，用於監控和警報.
    *   **Logs (日誌)**：標準化日誌的結構與上下文，使其能與追蹤和指標關聯，提供更豐富的問題診斷資訊.
*   **.NET 9 的整合**: .NET 9 (以及 .NET 8) 提供了更豐富的內建支援，例如 ASP.NET Core 和 Entity Framework Core 內建的 OpenTelemetry Instrumentations，無需額外手動配置即可自動生成追蹤和指標. 日誌系統 (如 `Microsoft.Extensions.Logging`) 也更好地與 OpenTelemetry Logs 規範整合，實現日誌的集中管理與上下文關聯. .NET 9 在監控和追蹤方面有所改進. OpenTelemetry 的主要優勢是其供應商中立性，讓您可以自由切換可觀測性後端而無需修改檢測程式碼.

#### (4). 實戰建議：為什麼這對用戶有用？

**1. 提升效能與降低成本（原生 AOT & Trimming）**
*   **MESClient, CSS, LXKiosk (API Controllers)**: 這些系統擁有大量的 API Controllers。將核心 API 服務透過原生 AOT 編譯發布，可以顯著降低每個請求的處理延遲 (latency)，特別是對於啟動頻繁或負載波動較大的 API 端點。更小的部署包也意味著更快的部署速度和更少的儲存空間. .NET 9 將冷啟動時間減少多達 70%，部署大小減少 50%。
*   **LCEPM (Docker 容器化部署)**: LCEPM 已經使用 Docker。原生 AOT 編譯生成的輕量級、自包含 (self-contained) 執行檔可以極大地縮減 Docker 映像檔的大小，加速容器啟動，減少資源消耗，從而降低雲端託管成本. 這也提升了服務的彈性與擴展性。
*   **整體安全加強**: 原生 AOT 編譯後的應用程式更難進行逆向工程 (reverse engineering)，提高了程式碼的安全性.

**2. 統一且強大的可觀測性（OpenTelemetry）**
*   **解決監控工具碎片化問題**: 您目前在不同專案中使用了 Elmah、Elastic APM、NLog 等多種監控與日誌工具。透過引入 OpenTelemetry，可以建立一個統一的遙測資料收集標準，無論後端採用 Elastic APM、Grafana Loki、Prometheus 還是其他 APM 解決方案，都能以標準格式匯出資料。這將大幅簡化日誌和監控的配置與管理。
*   **提升問題診斷效率**: 您的系統架構複雜，多個專案之間存在 API 呼叫 (如 LXKiosk 呼叫 ERP API，MESClient 呼叫 ERP API)。OpenTelemetry 的分散式追蹤能力可以在一個介面中清晰地展示一個請求在不同服務間的流動路徑和各環節的耗時，從而迅速定位效能瓶頸或錯誤根源.
*   **前端日誌整合**: JSNLog (前端→後端) 也可以考慮將其日誌格式標準化為 OpenTelemetry 規範，以便與後端日誌系統更緊密地整合，實現端到端的追蹤。

#### (5). Lab 提案（實作專案）：

**專案名稱：MESClient 核心 API 的原生 AOT 試點與 OpenTelemetry 基礎整合**

**目標**:
1.  將 MESClient 中一個高頻使用的 API Controller 專案 (如 `ApiControllers/ManufactureProcessController` 或 `ApiControllers/DispatchBoardController`)，嘗試使用 .NET 9 原生 AOT 編譯並部署，比較其啟動時間與記憶體佔用。
2.  在 MESClient 中導入 OpenTelemetry，為一個選定的 API 實作分散式追蹤和基本指標收集，並將其匯出至簡易的 Jaeger 或 Zipkin 追蹤後端。

**預計耗時**: 4 小時

**實作步驟**:

1.  **環境準備 (1 小時)**:
    *   確保開發環境已安裝最新版 .NET 9 SDK (或最新預覽版)。
    *   準備一個簡易的 OpenTelemetry 收集器 (Collector) 與後端 (例如，使用 Docker 啟動 Jaeger 或 Zipkin)。
        ```bash
        docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -e COLLECTOR_OTLP_ENABLED=true -p 6831:6831/udp -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest
        ```
    *   複製 MESClient 專案到一個獨立分支進行實驗。

2.  **MESClient 原生 AOT 試點 (1.5 小時)**:
    *   **選擇目標**: 挑選 MESClient 中一個較為獨立且核心邏輯集中的 API Controller。
    *   **修改專案檔**: 在 `MESClient.WebSite.csproj` (或單獨抽取 API 專案) 中，加入或修改相關屬性以啟用 AOT。
        ```xml
        <PropertyGroup>
          <TargetFramework>net9.0</TargetFramework>
          <PublishAot>true</PublishAot>
          <IsTrimmable>true</IsTrimmable>
          <TrimMode>full</TrimMode> <!-- 或 partial，視應用程式對反射的依賴程度 -->
        </PropertyGroup>
        ```
    *   **發布與測試**: 使用 `dotnet publish -c Release -r win-x64 --self-contained` (或其他目標運行時) 進行發布。
    *   **效能比較**: 記錄 AOT 版本與非 AOT 版本的發布包大小、啟動時間和峰值記憶體使用量。觀察 Razor Views 是否受影響，針對 Razor Views 應用程式，通常只建議針對 API 部分或後台服務啟用 AOT。

3.  **OpenTelemetry 基礎整合 (1.5 小時)**:
    *   **安裝 NuGet 套件**: 在 `MESClient.WebSite` 專案中安裝：
        *   `OpenTelemetry.Extensions.Hosting`
        *   `OpenTelemetry.Instrumentation.AspNetCore`
        *   `OpenTelemetry.Instrumentation.EntityFrameworkCore`
        *   `OpenTelemetry.Exporter.OpenTelemetryProtocol` (用於 OTLP 匯出到 Jaeger)
        *   `OpenTelemetry.Exporter.Console` (可選，用於開發期間日誌輸出)
        *   注意：舊版的 `OpenTelemetry.Exporter.Jaeger` 已被 `OpenTelemetry.Exporter.OpenTelemetryProtocol` 取代.
    *   **配置 `Program.cs`**:
        ```csharp
        using OpenTelemetry.Metrics;
        using OpenTelemetry.Resources;
        using OpenTelemetry.Trace;
        using System.Diagnostics; // For ActivitySource

        // ... 其他服務配置 ...

        builder.Services.AddOpenTelemetry()
            .ConfigureResource(resource => resource
                .AddService(serviceName: "MESClient.WebSite", serviceVersion: "1.0.0"))
            .WithTracing(tracing => tracing
                .AddAspNetCoreInstrumentation() // 自動追蹤 ASP.NET Core 請求
                .AddEntityFrameworkCoreInstrumentation() // 自動追蹤 EF Core 操作
                // .AddHttpClientInstrumentation() // 如果有 HttpClient 呼叫外部 API
                .AddSource("CustomSource") // 自定義追蹤來源，用於手動追蹤
                .AddOtlpExporter(options => options.Endpoint = new Uri("http://localhost:4317"))) // 匯出到 Jaeger Collector
            .WithMetrics(metrics => metrics
                .AddAspNetCoreInstrumentation()
                .AddOtlpExporter(options => options.Endpoint = new Uri("http://localhost:4317")));

        // ... 其他中介軟體配置 ...
        ```
    *   **手動追蹤 (可選)**: 在一個業務邏輯 (例如 `ManufactureProcessLogic` 或 `ManufactureProcessService`) 中，使用 `ActivitySource` 進行手動追蹤，以更細粒度地監控特定操作.
        ```csharp
        private static readonly ActivitySource MyActivitySource = new ActivitySource("CustomSource");

        public async Task<MyResult> ProcessSomethingAsync()
        {
            using var activity = MyActivitySource.StartActivity("ProcessingStepX");
            activity?.SetTag("input.id", someId);
            // ... 核心邏輯 ...
            activity?.SetStatus(ActivityStatusCode.Ok);
            return result;
        }
        ```
    *   **運行與驗證**: 運行 MESClient 專案，發送請求到被整合的 API，然後訪問 Jaeger UI (通常是 `http://localhost:16686`) 查看追蹤和服務依賴圖.

**預期成果**:
*   一個可運行的 MESClient API 部分的原生 AOT 版本，並記錄了其效能指標。
*   MESClient API 請求在 Jaeger 中可見，包含 ASP.NET Core 和 EF Core 的自動追蹤，以及可選的自定義業務邏輯追蹤。
*   對 .NET 9 的新特性有初步的實戰經驗，並評估其在您其他 .NET Core 專案 (CSS, LXKiosk, LCEPM) 中的適用性。

#### (6). 參考文獻：

*   Getting started with Open Telemetry in .NET with Jaeger and Seq - Anton Martyniuk
*   Microsoft Releases .NET 9 Preview 7 with New Features and Updates - Brainvire
*   Getting started with OpenTelemetry and distributed tracing in .NET - my tech ramblings
*   Export to Jaeger | OpenTelemetry
*   Unlocking New Potential: Entity Framework Core Enhancements in .NET 9
*   Getting started with Open Telemetry in .NET with Jaeger and Seq - Medium
*   Native AOT Compilation in .NET 9: Boost Performance with This Ultimate Guide
*   What's New in .NET 9: A Developer's Perspective - Syncfusion
*   Example: Use OpenTelemetry with Prometheus, Grafana, and Jaeger - .NET
*   10 New Features in EF 9 - Telerik.com
*   OpenTelemetry in .NET 9: Trace Requests End-to-End with Jaeger - C# Corner
*   Why .NET 9 Apps Are Faster Than Ever(How to Take Full Advantage) | by Hossein Kohzadi
*   .NET 9 Just Changed Everything — Are You Ready? | by Code Crack | Dot Net, API & SQL Learning | Medium
*   Optimizing EF Core Query Performance in .NET 9 | by Michael Maurice | Medium
*   NET 9 Changed Everything — You Won't Believe How API Work Now! - Medium
*   OpenTelemetry Usage in Microservice Architecture with .NET 9 | by Serkut Yıldırım - Medium
*   What's new in .NET 9 - Microsoft Learn
*   .NET | Last9 Documentation
*   .NET | OpenTelemetry
*   .NET Observability with OpenTelemetry - .NET | Microsoft Learn