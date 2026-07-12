## 技術研究報告：提升工作軟體效率與可觀察性新進展

本報告將專注於針對您現有以 .NET 為主的軟體系統架構，探討近期（約近 1-2 個月）具備實質影響力的新技術進展，旨在提升效率、優化效能或解決現有痛點。

### 1. OpenTelemetry .NET 生態系統的成熟與應用

#### (1). 資料來源的可信程度：高

OpenTelemetry 作為雲原生運算基金會（CNCF）的畢業專案，已成為分散式追蹤、指標和日誌收集的事實標準。其規範由產業巨頭（如 Google, Microsoft, Amazon 等）共同制定，並擁有活躍的開源社群及眾多企業應用案例。相關資訊主要來自官方文件、CNCF 博客、微軟 .NET 團隊部落格及各大雲服務供應商的支援文件，可靠性極高。

#### (2). 技術快訊：統一分散式系統的觀測性 (Observability)

您的多個專案 (MESClient, CSS, LXKiosk, LCEPM, ERP-Web, HKLogistics) 雖然各自獨立，但存在頻繁的系統間整合與 API 呼叫 (如 LXKiosk 串接 ERP, MESClient 串接 ERP, HKLogistics 串接 ERP)。目前您使用 Elmah/Elastic APM 進行錯誤監控，NLog/JSNLog 進行日誌記錄。然而，在處理跨多個服務的複雜請求時，單一服務的日誌和錯誤監控難以提供完整的請求生命週期視圖。

OpenTelemetry 旨在解決這一痛點，它提供了一套標準化的 API、SDK 和工具，用於收集應用程式的遙測資料 (Telemetry Data)，包含：

*   **分散式追蹤 (Distributed Tracing)**：追蹤一個請求在多個服務間的流動路徑和時間。
*   **指標 (Metrics)**：收集應用程式的效能數據，如 CPU 使用率、記憶體、請求頻率等。
*   **日誌 (Logs)**：標準化日誌格式，並與追蹤資訊關聯。

透過 OpenTelemetry，您可以將這些遙測資料匯出到後端分析系統 (如 Jaeger, Prometheus, Grafana, Elastic APM 等)，從而獲得對整個分散式系統更深入、更統一的觀測能力，大幅提升故障排除和效能優化的效率。近期 .NET SDK 的持續優化，使其在 .NET Core 及 .NET Framework 應用中的整合更加成熟和便捷，尤其是在 .NET 9/10 環境下，相關支援和效能表現更佳。

#### (3). 核心原理：標準化遙測資料的收集與匯出

OpenTelemetry 的核心原理是提供一個**供應商中立 (Vendor-Neutral)** 的遙測數據收集框架。它不限定特定的後端分析工具，而是定義了一套通用的資料模型、API 和 SDK，讓開發者能夠使用統一的方式從應用程式中採集遙測數據。

其主要組成部分包括：

*   **API (Application Programming Interface)**：用於在程式碼中建立和管理 traces, metrics, logs 的介面。
*   **SDK (Software Development Kit)**：實現了 API 並提供了處理和匯出遙測數據的工具。它包含各種 **Instrumentation Libraries**，能自動或手動從常見的框架和函式庫 (如 ASP.NET Core, Entity Framework Core, HttpClient, gRPC, Redis 等) 收集遙測數據。
*   **Collector (收集器)**：一個代理程式或服務，用於接收、處理和匯出遙測數據。它可以在邊緣 (Sidecar, Agent) 或集中式 (Gateway) 部署，支援多種輸入和輸出格式，用於將數據轉發到不同的後端分析系統。

當一個請求進入系統時，OpenTelemetry 會生成一個唯一的 **trace ID** 和 **span ID**。這個 trace ID 會隨著請求在您的各個微服務或層級中傳播 (Context Propagation)。每個服務在處理請求時都會建立自己的 span，記錄操作的開始、結束時間、屬性等，並將這些 span 與共同的 trace ID 關聯起來。最終，這些具有關聯性的 traces, metrics, logs 會被匯出到選定的後端分析工具中，形成一個完整的請求流動圖。

在 .NET 生態中，OpenTelemetry .NET SDK 透過 `ActivitySource` 和 `Activity` 物件來實現追蹤。它利用 `EventSource` 收集內建的 .NET 運行時事件，並透過 `Meter` API 收集自定義指標。近期，日誌整合也得到了顯著改善，可以將標準的 `ILogger` 日誌自動轉換為 OpenTelemetry Logs，並與 trace/span 資訊自動關聯。

#### (4). 實戰建議：為什麼這對用戶有用？

考慮到您的系統架構和開發重點，導入 OpenTelemetry 將帶來以下顯著效益：

1.  **統一 Observability 視圖**：您擁有多個高度耦合或整合的系統 (MESClient, CSS, LXKiosk, LCEPM, ERP-Web)。OpenTelemetry 可以將這些系統的遙測數據匯集到一個平台，提供一個單一的儀表板來觀察整個業務流程，而無需在不同系統的日誌檔或監控工具之間切換。
2.  **快速故障排除**：當 MESClient 的報工請求因 ERP-Web 的某個模組延遲時，傳統的日誌分析可能需要多個團隊協作，依序查詢。透過分散式追蹤，您可以立即看到請求在 MESClient、ERP-Web 之間以及 ERP-Web 內部各層（Controller -> BLL -> Service -> DbContext）的耗時，精確定位瓶頸。
3.  **效能優化依據**：指標收集能提供實時的系統健康狀態，結合追蹤數據，可以量化每次程式碼變更對效能的影響，為優化決策提供數據支持。
4.  **降低技術債**：逐步取代或整合現有的 Elmah, Elastic APM (若有切換需求), NLog 配置，將遙測數據標準化。長期來看，這將簡化監控基礎設施的管理。
5.  **支援現代化與雲原生**：您的 .NET Core 專案已朝現代化方向發展。OpenTelemetry 是雲原生架構的基石之一，為未來向微服務或更複雜的分散式架構演進打下良好基礎。對於 .NET Framework 專案 (如 ERP-Web, HKLogistics)，OpenTelemetry 也提供了相容性層，可以逐步導入。

特別是對於 **ERP-Web** 和 **HKLogistics** 這類大型且關鍵的系統，其複雜的業務邏輯和廣泛的外部整合使得問題診斷極為困難。導入 OpenTelemetry 將極大地提升這些系統的可維護性和穩定性。而對於 **LXKiosk** 這種對即時性要求高的現場應用，能快速定位 API 串接 ERP 的瓶頸至關重要。

#### (5). Lab 提案（實作專案）：為現有 ASP.NET Core 應用添加 OpenTelemetry Observability

**專案名稱**：MESClient 模組的 OpenTelemetry 追蹤與日誌整合

**目標**：在 MESClient 專案中，整合 OpenTelemetry 追蹤和日誌，並將數據匯出到一個本地運行的 Jaeger 追蹤伺服器，觀察一個前端請求到後端 API，再到資料庫的完整追蹤鏈。

**預計耗時**：3-4 小時

**步驟**：

1.  **環境準備**：
    *   確保 .NET SDK 9 已安裝。
    *   安裝 Docker Desktop (用於運行 Jaeger)。
    *   在終端機中運行 Jaeger：`docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -e COLLECTOR_OTLP_ENABLED=true -p 6831:6831/udp -p 6832:6832/udp -p 16686:16686 -p 4317:4317 -p 4318:4318 -p 14250:14250 -p 14268:14268 -p 14269:14269 -p 9411:9411 jaegertracing/all-in-one:latest`
    *   訪問 Jaeger UI：`http://localhost:16686`

2.  **MESClient 專案修改**：
    *   **添加 NuGet 套件**：
        在 `MESClient.WebSite.csproj` 中添加：
        ```xml
        <ItemGroup>
            <PackageReference Include="OpenTelemetry.Exporter.Jaeger" Version="1.8.1" />
            <PackageReference Include="OpenTelemetry.Extensions.Hosting" Version="1.8.1" />
            <PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="1.8.1" />
            <PackageReference Include="OpenTelemetry.Instrumentation.EntityFrameworkCore" Version="1.0.0-beta.10" />
            <PackageReference Include="OpenTelemetry.Instrumentation.HttpClient" Version="1.8.1" />
            <PackageReference Include="OpenTelemetry.Instrumentation.Runtime" Version="1.8.0" />
            <PackageReference Include="OpenTelemetry.Instrumentation.SqlClient" Version="1.7.0-beta.1" />
            <PackageReference Include="OpenTelemetry.Exporter.Console" Version="1.8.1" />
            <PackageReference Include="Microsoft.Extensions.Logging.Console" Version="9.0.0-preview.*" />
        </ItemGroup>
        ```
        *   *(註：版本號請參考實際最新穩定版或預覽版，此處為示例)*

    *   **配置 `Program.cs` 或 `Startup.cs`** (以 .NET 9 Minimal API 樣式為例，假設在 `Program.cs` 中配置)：
        ```csharp
        using OpenTelemetry.Logs;
        using OpenTelemetry.Metrics;
        using OpenTelemetry.Trace;
        using OpenTelemetry.Exporter;
        using LC.Core.Authentication; // 假設是您的驗證相關命名空間
        using DbContexts; // 假設是您的 DbContext 命名空間

        var builder = WebApplication.CreateBuilder(args);

        // ... 現有服務註冊 ...
        builder.Services.AddControllersWithViews();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.AddDbContext<MESClientDbContext>(options =>
            options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
        // ... 其他服務 ...

        // 配置 OpenTelemetry
        builder.Services.AddOpenTelemetry()
            .ConfigureResource(resource => resource.AddService(
                serviceName: "MESClient.WebSite", // 您的服務名稱
                serviceVersion: "1.0.0"))
            .WithTracing(tracing =>
            {
                tracing.AddSource("MESClient.App"); // 添加自定義 ActivitySource
                tracing.AddAspNetCoreInstrumentation(options =>
                {
                    options.Filter = (httpContext) =>
                    {
                        // 過濾掉 Swagger 和健康檢查端點，避免不必要的追蹤
                        return !httpContext.Request.Path.StartsWithSegments("/swagger") &&
                               !httpContext.Request.Path.StartsWithSegments("/health");
                    };
                    options.RecordException = true; // 記錄異常
                });
                tracing.AddHttpClientInstrumentation(); // 追蹤 HttpClient 請求 (如果 MESClient 有呼叫外部 API)
                tracing.AddEntityFrameworkCoreInstrumentation(options =>
                {
                    options.Set}DbStatementForText = true; // 記錄 SQL 語句
                    options.SetDbStatementForStoredProcedure = true; // 記錄儲存程序
                });
                // 如果您使用了 SQLClient 直接操作資料庫，可以添加此項
                // tracing.AddSqlClientInstrumentation(options => options.SetDbStatementForText = true);
                tracing.AddOtlpExporter(options =>
                {
                    options.Endpoint = new Uri("http://localhost:4317"); // Jaeger 預設 OTLP GRPC 端口
                    options.Protocol = OtlpExportProtocol.Grpc;
                });
                // 也可以添加 Console Exporter 方便在開發時查看
                tracing.AddConsoleExporter();
            })
            .WithMetrics(metrics =>
            {
                metrics.AddAspNetCoreInstrumentation();
                metrics.AddHttpClientInstrumentation();
                metrics.AddRuntimeInstrumentation(); // 收集 .NET Runtime 指標
                metrics.AddOtlpExporter(options =>
                {
                    options.Endpoint = new Uri("http://localhost:4317");
                    options.Protocol = OtlpExportProtocol.Grpc;
                });
            });

        // 配置日誌輸出到 OpenTelemetry
        builder.Logging.AddOpenTelemetry(logging =>
        {
            logging.IncludeScopes = true;
            logging.IncludeFormattedMessage = true;
            logging.ParseStateValues = true;
            logging.AddOtlpExporter(options =>
            {
                options.Endpoint = new Uri("http://localhost:4317");
                options.Protocol = OtlpExportProtocol.Grpc;
            });
            logging.AddConsoleExporter();
        });

        var app = builder.Build();

        // ... 現有中介軟體 ...
        app.UseExceptionHandler("/Home/Error");
        app.UseHsts();
        app.UseHttpsRedirection();
        app.UseStaticFiles();
        app.UseRouting();
        app.UseAuthentication();
        app.UseAuthorization();
        // ... 其他中介軟體 ...

        app.MapControllerRoute(
            name: "default",
            pattern: "{controller=Home}/{action=Index}/{id?}");

        app.Run();
        ```

    *   **在 Controllers 或 Logic/Service 中添加自定義追蹤 (可選)**：
        為了更細粒度地追蹤業務邏輯，可以在關鍵的 Logic/Service 方法中手動創建 `Activity`。
        ```csharp
        using System.Diagnostics;

        public class SomeService // 假設您的 MESClient.Layer4.AuthServices.AuthService
        {
            private static readonly ActivitySource _activitySource = new ActivitySource("MESClient.App"); // 與 Program.cs 中的 AddSource 名稱一致

            public async Task<MyResult> DoSomethingAsync()
            {
                using (var activity = _activitySource.StartActivity("SomeService.DoSomething"))
                {
                    activity?.AddTag("input.param", "someValue"); // 添加自定義標籤

                    // ... 您的業務邏輯 ...
                    await Task.Delay(50); // 模擬耗時操作

                    activity?.SetStatus(ActivityStatusCode.Ok); // 設定狀態
                    return new MyResult();
                }
            }
        }
        ```

3.  **執行與觀察**：
    *   啟動 MESClient 應用程式。
    *   訪問 MESClient 的任意頁面或觸發一個 API 請求，特別是涉及資料庫操作的功能 (例如製程報工、使用者/角色管理)。
    *   回到 Jaeger UI (http://localhost:16686)。
    *   在左上角的 "Service" 下拉選單中選擇 "MESClient.WebSite"，然後點擊 "Find Traces"。
    *   您將會看到每個請求的完整追蹤鏈，可以點擊進入查看詳細的 Span (HTTP Request, EF Core Query, 自定義 Span)，包括耗時、標籤等資訊。

**成果驗證**：成功在 Jaeger UI 中看到 MESClient 應用程式的 HTTP 請求、資料庫查詢以及自定義業務邏輯方法的追蹤，並能清晰呈現請求在各個組件之間的流動與耗時。

#### (6). 參考文獻：

1.  **OpenTelemetry 官方網站**: [https://opentelemetry.io/](https://opentelemetry.io/)
2.  **OpenTelemetry .NET GitHub 儲存庫**: [https://github.com/open-telemetry/opentelemetry-dotnet](https://github.com/open-telemetry/opentelemetry-dotnet)
3.  **Microsoft Learn - 分散式追蹤搭配 OpenTelemetry**: [https://learn.microsoft.com/zh-tw/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthrough](https://learn.microsoft.com/zh-tw/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthrough)
4.  **Jaeger 官方網站**: [https://www.jaegertracing.io/](https://www.jaegertracing.io/)
5.  **CNCF Landscape - OpenTelemetry**: [https://landscape.cncf.io/card-mode?category=observability&grouping=project&name=opentelemetry](https://landscape.cncf.io/card-mode?category=observability&grouping=project&name=opentelemetry)

---

### 2. C# Source Generators (C# 來源產生器) 的進階應用

#### (1). 資料來源的可信程度：高

C# Source Generators 是 .NET 5 引入的一項功能，微軟官方文件和部落格有詳細介紹，且已被廣泛應用於如 ASP.NET Core Minimal APIs、`System.Text.Json` 序列化等核心函式庫中。許多流行的開源專案 (如 `CommunityToolkit.Mvvm`, `AutoMapper` 的實驗性生成器) 也都在使用。相關教程、案例和社群討論非常活躍，可信度高。

#### (2). 技術快訊：編譯期程式碼生成，取代部分 T4 模板與反射

您在多個專案 (MESClient, CSS, LXKiosk, ERP-Web, HKLogistics, LCEPM) 中大量使用 T4 模板來生成程式碼，例如將 Enum/Resource 同步到 JavaScript、生成 Entity 檔案等。雖然 T4 模板功能強大，但它是一種基於文字轉換的生成方式，通常需要額外的工具或手動步驟來觸發，且缺乏與編譯器的深度整合。

C# Source Generators 則是一種在編譯期間運行的程式碼生成技術。它允許開發者編寫一個分析現有程式碼並在編譯時**生成新程式碼**的元件。這些生成的程式碼會被納入編譯流程，如同手寫的程式碼一樣。這解決了 T4 模板的一些缺點，並帶來以下優勢：

*   **自動化與編譯期整合**：程式碼生成在每次編譯時自動觸發，無需手動運行 T4 或外部腳本。
*   **效能優化**：生成的程式碼可以取代運行時反射 (Reflection) 的需求，例如用於 JSON 序列化、DI 容器註冊、DTO 映射等，從而提升應用程式的運行時效能。
*   **減少樣板程式碼 (Boilerplate Code)**：自動生成重複性高、模式固定的程式碼，讓開發者專注於業務邏輯。
*   **類型安全與 IDE 支援**：生成的程式碼是標準的 C# 程式碼，IDE (如 Visual Studio, Rider) 可以提供完整的 IntelliSense、錯誤檢查和重構支援。

雖然它不能完全取代所有 T4 的應用 (特別是生成非 C# 語言的檔案)，但對於生成 C# 相關的程式碼，它是更現代、更高效且與 .NET 生態系統整合更緊密的方式。

#### (3). 核心原理：基於 Roslyn 編譯器 API 進行分析與生成

C# Source Generators 的核心是利用 .NET 編譯器 (Roslyn) 的**編譯器 API**。Roslyn 不僅是一個編譯器，它還提供了豐富的 API 供開發者以程式設計方式分析和操作 C# 程式碼。

一個 Source Generator 的運作流程如下：

1.  **初始化 (Initialize)**：Generator 在編譯開始時被初始化，它可以註冊回調函數，以監聽編譯器發出的特定事件 (例如，當編譯器準備處理語法樹或符號時)。
2.  **執行 (Execute)**：當編譯器觸發註冊的回調時，Generator 會獲得一個 `GeneratorExecutionContext`，其中包含了當前編譯的相關資訊，例如：
    *   **編譯參考 (Compilation)**：允許 Generator 訪問所有已編譯的程式碼的語法樹 (Syntax Trees) 和符號 (Symbols)。
    *   **附加檔案 (Additional Files)**：允許 Generator 讀取專案中包含的其他非 C# 檔案 (例如您的 `translations.csv` 或 `ApiGuid.cs` 等)。
3.  **分析與判斷**：Generator 使用 Roslyn API (如 `SyntaxReceiver` 或 `IncrementalGenerator` 的 `ForAttributeWithMetadataName` 等) 分析現有程式碼的結構，尋找特定的屬性、介面實現、類別模式等。例如，它可以掃描所有以 "Logic" 或 "Service" 結尾的類別，或具有特定屬性的類別。
4.  **生成程式碼 (AddSource)**：根據分析結果，Generator 動態創建新的 C# 原始碼字串。這些字串可以是新的類別、方法、介面實現等等。
5.  **注入編譯**：Generator 將生成的原始碼字串透過 `AddSource` 方法添加到 `GeneratorExecutionContext` 中。這些生成的程式碼會被 Roslyn 編譯器視為專案的一部分進行編譯，產生最終的組件 (Assembly)。

這樣一來，所有生成的程式碼在編譯期就已經存在並經過編譯器檢查，解決了反射帶來的運行時效能開銷和類型不安全問題。

#### (4). 實戰建議：為什麼這對用戶有用？

對於您的專案，尤其是有大量樣板程式碼和 T4 模板使用的情況，C# Source Generators 能帶來以下好處：

1.  **改善 DI 自動註冊**：您目前使用 "Logic"/"Service" 結尾類別的自動註冊。可以開發一個 Source Generator，在編譯時掃描這些類別，並**直接生成** `IServiceCollection` 的擴充方法來註冊服務，取代運行時的反射掃描，提升啟動效能。
2.  **消除部分反射開銷**：
    *   **Mapper 生成**：如果您的專案中存在大量 DTO 和 Entity 之間的映射，可以考慮使用 Source Generator 生成映射程式碼，取代運行時的 AutoMapper 反射。
    *   **選項綁定**：對於 `IConfiguration` 到 Options 類別的綁定，可以生成靜態方法，避免運行時反射。
3.  **增強多語系資源管理**：您有多個專案使用 `.resx` 資源檔並透過 T4 同步到 JS。可以考慮生成一個 C# 類別，將 `.resx` 資源靜態化，並提供強類型訪問，避免魔法字串，並在需要時再將其同步到 JS。
4.  **簡化權限系統定義**：在 CSS 專案中，權限系統有 ApiGuid、MenuAttr。可以開發 Source Generator，掃描這些屬性或 GUID 定義，自動生成相關的權限常量類別或驗證邏輯，確保一致性並減少手動維護的工作。
5.  **提升前端同步效率**：對於將 C# Enums 同步到 JavaScript (Domain.js, LC.Core.js, LCERPApiLogics.js)，Source Generator 可以更精確地生成這些 JS 檔案，無需依賴 Powershell 腳本，且能更好地整合到 CI/CD 流程中。
6.  **解決 .NET Framework 專案痛點**：雖然主要用於 .NET (Core)，但 Source Generators 也可以在 .NET Framework 專案中使用 (通常需要手動設置 ProjectReference 並確保 .NET Standard 2.0 兼容)。對於 ERP-Web 和 HKLogistics 的 `DB.tt` 生成 Entity 檔案，如果未來要遷移或需要新的生成邏輯，可以考慮用 Source Generator 取代部分 T4 邏輯。

#### (5). Lab 提案（實作專案）：自動生成 DI 服務註冊擴充方法

**專案名稱**：Source Generator 自動註冊 Logic/Service

**目標**：建立一個 C# Source Generator，它能掃描一個假想的 .NET Core 應用程式專案中的類別，凡是名稱以 "Logic" 或 "Service" 結尾的公共類別，就自動生成一個 `IServiceCollection` 的擴充方法來註冊這些服務。

**預計耗時**：2-3 小時

**步驟**：

1.  **建立 Source Generator 專案**：
    *   新建一個 .NET Standard 2.0 (或更高) 的類別庫專案，例如 `MyServiceGenerator`。
    *   編輯 `.csproj` 檔案，添加必要的 NuGet 套件和配置：
        ```xml
        <Project Sdk="Microsoft.NET.Sdk">
            <PropertyGroup>
                <TargetFramework>netstandard2.0</TargetFramework>
                <LangVersion>latest</LangVersion>
                <Nullable>enable</Nullable>
                <!-- 啟用 Source Generators 特性 -->
                <EnforceExtendedAnalyzerRules>true</EnforceExtendedAnalyzerRules>
                <IsRoslynComponent>true</IsRoslynComponent>
            </PropertyGroup>

            <ItemGroup>
                <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.3.4">
                    <PrivateAssets>all</PrivateAssets>
                    <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildTransitive</IncludeAssets>
                </PackageReference>
                <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.8.0">
                    <PrivateAssets>all</PrivateAssets>
                    <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildTransitive</IncludeAssets>
                </PackageReference>
            </ItemGroup>
        </Project>
        ```
        *   *(註：`Microsoft.CodeAnalysis.CSharp` 版本應與您目標 .NET 環境的編譯器版本匹配，此處為示例)*

2.  **編寫 Source Generator 邏輯**：
    *   在 `MyServiceGenerator` 專案中，創建一個類別 `ServiceRegistrationGenerator.cs`：
        ```csharp
        using Microsoft.CodeAnalysis;
        using Microsoft.CodeAnalysis.CSharp.Syntax;
        using System.Collections.Generic;
        using System.Linq;
        using System.Text;

        [Generator]
        public class ServiceRegistrationGenerator : ISourceGenerator
        {
            public void Initialize(GeneratorInitializationContext context)
            {
                // 註冊一個 SyntaxReceiver，它會在編譯器解析語法樹時接收到回調
                context.RegisterForSyntaxNotifications(() => new ServiceSyntaxReceiver());
            }

            public void Execute(GeneratorExecutionContext context)
            {
                if (context.SyntaxReceiver is not ServiceSyntaxReceiver receiver)
                    return;

                // 檢查是否有 System.IServiceCollection 類型可用
                var iServiceCollectionType = context.Compilation.GetTypeByMetadataName("Microsoft.Extensions.DependencyInjection.IServiceCollection");
                if (iServiceCollectionType == null) return; // 如果沒有，則不生成

                var serviceClasses = new List<INamedTypeSymbol>();

                foreach (var candidateClass in receiver.CandidateClasses)
                {
                    var model = context.Compilation.GetSemanticModel(candidateClass.SyntaxTree);
                    var symbol = model.GetDeclaredSymbol(candidateClass) as INamedTypeSymbol;

                    if (symbol == null || symbol.IsAbstract || symbol.IsStatic || symbol.DeclaredAccessibility != Accessibility.Public)
                        continue;

                    // 檢查類別名稱是否以 "Logic" 或 "Service" 結尾
                    if (symbol.Name.EndsWith("Logic") || symbol.Name.EndsWith("Service"))
                    {
                        serviceClasses.Add(symbol);
                    }
                }

                if (!serviceClasses.Any()) return;

                // 生成程式碼
                var sb = new StringBuilder();
                sb.AppendLine("using Microsoft.Extensions.DependencyInjection;");
                sb.AppendLine("using Microsoft.Extensions.DependencyInjection.Extensions;"); // For TryAddScoped etc.
                sb.AppendLine();
                sb.AppendLine($"namespace {context.Compilation.AssemblyName}.Generated");
                sb.AppendLine("{");
                sb.AppendLine("    public static class AutoServiceRegistrationExtensions");
                sb.AppendLine("    {");
                sb.AppendLine("        public static IServiceCollection AddAutoRegisteredServices(this IServiceCollection services)");
                sb.AppendLine("        {");

                foreach (var service in serviceClasses.OrderBy(s => s.ToDisplayString()))
                {
                    // 生成 Scoped 註冊，可以根據需求改成 Singleton/Transient
                    // 這裡假設都註冊為 Scoped，且如果存在介面，則註冊介面到實現
                    var interfaces = service.AllInterfaces.Where(i => i.DeclaredAccessibility == Accessibility.Public).ToList();
                    if (interfaces.Any())
                    {
                        foreach (var iface in interfaces)
                        {
                            sb.AppendLine($"            services.TryAddScoped<{iface.ToDisplayString()}, {service.ToDisplayString()}>();");
                        }
                    }
                    else
                    {
                        sb.AppendLine($"            services.TryAddScoped<{service.ToDisplayString()}>();");
                    }
                }

                sb.AppendLine("            return services;");
                sb.AppendLine("        }");
                sb.AppendLine("    }");
                sb.AppendLine("}");

                context.AddSource("AutoServiceRegistration.g.cs", sb.ToString());
            }
        }

        public class ServiceSyntaxReceiver : ISyntaxReceiver
        {
            public List<ClassDeclarationSyntax> CandidateClasses { get; } = new List<ClassDeclarationSyntax>();

            public void OnVisitSyntaxNode(SyntaxNode syntaxNode)
            {
                // 只對類別聲明感興趣
                if (syntaxNode is ClassDeclarationSyntax classDeclarationSyntax)
                {
                    CandidateClasses.Add(classDeclarationSyntax);
                }
            }
        }
        ```

3.  **創建一個目標應用程式專案 (模擬 MESClient 的 Logic/Service)**：
    *   新建一個 ASP.NET Core Web API 專案，例如 `MyApplication`。
    *   添加 `MyServiceGenerator` 專案引用，並標記為 `OutputItemType="Analyzer"` 和 `ReferenceOutputAssembly="false"`：
        ```xml
        <ItemGroup>
            <ProjectReference Include="..\MyServiceGenerator\MyServiceGenerator.csproj"
                              OutputItemType="Analyzer" ReferenceOutputAssembly="false" />
        </ItemGroup>
        ```
    *   在 `MyApplication` 專案中，創建幾個測試服務和邏輯類別：
        ```csharp
        // Services/UserService.cs
        namespace MyApplication.Services
        {
            public interface IUserService { string GetUserName(); }
            public class UserService : IUserService { public string GetUserName() => "Generated User"; }
        }

        // Logics/ProductLogic.cs
        namespace MyApplication.Logics
        {
            public class ProductLogic { public string GetProductName() => "Generated Product"; }
        }

        // OtherClasses/NonService.cs (不應被生成)
        namespace MyApplication.OtherClasses
        {
            public class NonService { }
        }
        ```

    *   在 `MyApplication` 的 `Program.cs` (或 `Startup.cs`) 中，調用生成的擴充方法：
        ```csharp
        using MyApplication.Generated; // 導入生成的命名空間

        var builder = WebApplication.CreateBuilder(args);
        builder.Services.AddControllers();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();

        // 調用自動生成的服務註冊方法
        builder.Services.AddAutoRegisteredServices();

        var app = builder.Build();

        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();
        app.UseAuthorization();
        app.MapControllers();

        // 測試生成的服務是否可用
        app.MapGet("/user", (IUserService userService) => userService.GetUserName());
        app.MapGet("/product", (MyApplication.Logics.ProductLogic productLogic) => productLogic.GetProductName()); // 直接注入具體類別
        
        app.Run();
        ```

4.  **運行與驗證**：
    *   在 `MyApplication` 專案中，編譯專案。
    *   在 Visual Studio 的 Solution Explorer 中，展開 `MyApplication` -> `Dependencies` -> `Analyzers` -> `MyServiceGenerator`。在它下面應該能找到 `AutoServiceRegistration.g.cs` 文件，查看其生成的內容。
    *   運行 `MyApplication` 應用程式。
    *   訪問 `/user` 和 `/product` 端點，驗證服務是否成功被注入並可使用。

**成果驗證**：成功地在編譯時生成了一個 `AutoServiceRegistrationExtensions` 類別，它包含了對 `UserService` 和 `ProductLogic` 的 `IServiceCollection` 擴充註冊方法，且應用程式能夠正確地解析和使用這些服務。

#### (6). 參考文獻：

1.  **Microsoft Learn - 建立 C# 來源產生器**: [https://learn.microsoft.com/zh-tw/dotnet/csharp/roslyn/source-generators-overview](https://learn.microsoft.com/zh-tw/dotnet/csharp/roslyn/source-generators-overview)
2.  **Microsoft DevBlogs - Introducing C# Source Generators**: [https://devblogs.microsoft.com/dotnet/introducing-c-source-generators/](https://devblogs.microsoft.com/dotnet/introducing-c-source-generators/)
3.  **Roslyn (C# Compiler) GitHub 儲存庫**: [https://github.com/dotnet/roslyn](https://github.com/dotnet/roslyn)
4.  **Awesome Source Generators**: [https://github.com/amis94/awesome-source-generators](https://github.com/amis94/awesome-source-generators)