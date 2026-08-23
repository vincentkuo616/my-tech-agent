## 今日技術研究報告：聚焦 .NET 生態系下的應用現代化與開發效率躍進

鑑於用戶維護的 MESClient, CSS, ERP-Web, HKLogistics, LXKiosk 等系統，普遍存在大型單體（monolith）或分層單體架構、前後端混合、多專案複雜協作、以及部分專案技術棧較舊（.NET Framework）等共通挑戰，本次研究將鎖定在近年來 .NET 生態系中，對於「提升開發效率、優化多專案協作、簡化雲原生部署路徑」具有實質影響力的兩大進展：**.NET Aspire** 與 **模組化單體 (Modular Monolith) 搭配垂直切片架構 (Vertical Slice Architecture)**。這兩項技術/模式能有效解決目前專案在開發治理、複雜度管理與未來擴展性上的痛點。

---

### (1). 資料來源的可信程度：高

*   **.NET Aspire**：由 Microsoft 官方主導開發，已於 .NET 8 正式版本發布 (General Availability, GA)，並持續在 .NET 9 預覽版中積極演進。相關文件、範例與社區討論極其豐富，且多為官方或資深社群成員發布，具備高度權威性與可信度.
*   **模組化單體 (Modular Monolith) 與垂直切片架構 (Vertical Slice Architecture)**：這是近年來 .NET 社群中廣泛討論並實踐的架構模式，旨在解決傳統分層架構（Layered Architecture）在大型專案中遇到的開發瓶頸與維護複雜性。雖然並非單一產品，但其概念、實踐方式及相關輔助函式庫（如 MediatR, Carter）已形成成熟的模式，並有大量文章、書籍與演講深入探討，社群共識程度高.

---

### (2). 技術快訊：簡化複雜應用程式開發與管理

#### 2.1 .NET Aspire (Orchestration for Cloud-Native .NET Apps)

**解決問題：** 用戶的系統如 MESClient、CSS、ERP-Web 等，普遍為多專案組成的複雜應用程式 (multi-project solutions)，本地開發時往往需要手動啟動多個服務（如 WebSite、ApiControllers、Hangfire、Redis、SQL Server）。當這些應用程式未來考慮向雲端遷移或採用更分散式架構時，部署與管理的複雜度將急劇上升。

.NET Aspire 旨在**極大化簡化**本地開發與雲端部署複雜的多服務 .NET 應用程式。它提供了一套工具與模式，用於：
*   **應用程式組成與協調 (Application Composition and Orchestration)：** 透過統一的設定檔 (AppHost)，將 Web 專案、API 專案、背景服務 (Hangfire)、資料庫 (SQL Server)、快取 (Redis) 等多個元件定義為一個應用程式的一部分。
*   **開發者體驗 (Developer Experience, DX)：** 提供一個視覺化的儀表板 (Dashboard)，讓開發者能一鍵啟動所有服務、監控服務狀態、查看日誌、環境變數、連線字串等，大幅提升本地開發效率.
*   **雲端部署準備 (Cloud Deployment Readiness)：** Aspire 的模型可直接轉換為雲原生部署描述符（如 Docker Compose、Kubernetes manifests），為未來向 Azure Container Apps 或 Kubernetes 等雲平台遷移提供順暢的路徑.
*   **內建遙測 (Built-in Telemetry)：** 自動整合 OpenTelemetry，提供開箱即用的分散式追蹤 (distributed tracing)、指標 (metrics) 和日誌 (logging) 功能，提升應用程式的可觀測性.

#### 2.2 模組化單體 (Modular Monolith) 與垂直切片架構 (Vertical Slice Architecture)

**解決問題：** 用戶的專案，特別是 CSS 的 5 層架構 (View/Controller/Service/Logic/Domain) 或 ERP-Web 龐大的 BLL/Service 層 (167 個檔案，50 個模組目錄)，在管理、理解和修改時面臨挑戰。當一個功能橫跨多個層次時，其相關程式碼分散各處，導致「改動風險高」、「新功能開發慢」、「理解成本高」。傳統的分層架構，在專案規模擴大後，各層之間的強耦合與橫向切分反而成為瓶頸。

模組化單體與垂直切片架構旨在：
*   **降低複雜度：** 將應用程式按「業務功能」而非技術層次 (layer) 進行垂直切割。每個垂直切片 (vertical slice) 包含一個業務功能所需的全部層次（Controller、Service、Logic、DB Access），並盡量保持獨立.
*   **提升開發效率：** 開發新功能時，僅需關注特定的垂直切片，減少對其他部分的影響，實現「高內聚、低耦合」的目標.
*   **優化維護性：** 功能相關的程式碼集中管理，更易於理解、修改和測試。
*   **漸進式演進：** 模組化單體可以在未來根據業務需求，逐步將部分垂直切片拆分為獨立的微服務 (microservices)，提供平滑的演進路徑，而無需一次性重寫整個系統.

---

### (3). 核心原理：深入拆解運作機制

#### 3.1 .NET Aspire 核心原理

.NET Aspire 的核心是其「應用程式主機 (AppHost)」專案，它扮演著整個分散式應用程式的組態與協調者。

1.  **應用程式模型 (Application Model)：** 開發者在 AppHost 專案中，使用 C# 程式碼定義應用程式的所有資源 (resources)，例如：
    *   `builder.AddProject<Projects.MyWebApp>("mywebapp");` (添加 Web 專案)
    *   `builder.AddProject<Projects.MyApi>("myapi");` (添加 API 專案)
    *   `builder.AddPostgres("postgres").PublishAsContainer();` (添加 PostgreSQL 資料庫，可指定發布為 Docker 容器)
    *   `builder.AddRedis("redis");` (添加 Redis 快取)
    *   `builder.AddContainer("rabbitmq", "rabbitmq");` (添加 RabbitMQ 容器)
    這些資源定義了應用程式的拓撲結構和依賴關係。
2.  **儀表板與開發者工具 (Dashboard and Developer Tools)：** 當 AppHost 啟動時，它會啟動所有定義的資源，並開啟一個本地的 Aspire Dashboard。這個 Dashboard 會：
    *   顯示所有服務的啟動狀態、網址。
    *   集中呈現所有服務的日誌串流 (log stream)，並支援篩選。
    *   提供 OpenTelemetry 收集到的分散式追蹤和指標數據。
    *   展示環境變數與連線字串，方便開發與偵錯。
3.  **環境變數與連線字串自動注入 (Automatic Environment Variable and Connection String Injection)：** Aspire 會自動為每個服務生成並注入所需的環境變數和連線字串。例如，當 `MyWebApp` 需要連接 `redis` 時，Aspire 會自動生成一個 `ConnectionStrings:redis` 環境變數，並將 Redis 的連線資訊注入到 `MyWebApp` 的設定中，無需手動配置.
4.  **雲端部署整合 (Cloud Deployment Integration)：** Aspire 透過其發布機制，可以將 AppHost 中定義的應用程式模型轉換為雲端供應商可理解的部署描述符。例如，它可以生成 Docker Compose 檔案用於本地容器環境，或 Bicep/ARM 模板用於 Azure 部署.
5.  **OpenTelemetry 整合 (OpenTelemetry Integration)：** Aspire 的預設模板就集成了 OpenTelemetry SDK。所有透過 Aspire 啟動的 .NET 專案都會自動發送遙測數據 (traces, metrics, logs)，這些數據會被 Aspire Dashboard 收集並可視化，極大提高了應用程式的可觀測性。

#### 3.2 模組化單體與垂直切片架構核心原理

該架構模式主要體現在專案的組織與程式碼的切分方式上：

1.  **以業務模組劃分 (Business Module Partitioning)：** 應用程式不再按技術層（如 Application、Domain、Infrastructure）劃分，而是按高階業務功能（如「客戶管理」、「訂單處理」、「庫存管理」）劃分為獨立的模組 (modules)。這些模組在「程式碼層面」是相對獨立的，但仍部署在同一個單體應用程式中.
2.  **垂直切片 (Vertical Slices)：** 在每個業務模組內部，或是整個應用程式層面，將傳統橫向的層次 (horizontal layers) 切分為縱向的「切片」。每個切片代表一個特定的業務用例 (use case)，從請求入口 (Controller/Endpoint) 到資料庫存取 (Repository/ORM) 的完整路徑。例如，一個「創建訂單」的垂直切片可能包含 `CreateOrderController`、`CreateOrderCommand`、`CreateOrderCommandHandler` (使用 MediatR), 以及對應的 `Order` 實體和資料庫操作.
3.  **去除不必要的共享 (Eliminate Unnecessary Sharing)：** 核心原則是每個垂直切片只包含其所需的所有程式碼，盡量避免跨切片的緊密耦合。不同切片可以有自己獨立的資料模型 (ViewModels)、業務邏輯，甚至不同的資料存取方式 (儘管通常共享同一個 DbContext 和資料庫)。
4.  **使用 CQRS-lite 模式 (CQRS-lite Pattern)：** 垂直切片架構常常結合輕量級的 CQRS (Command Query Responsibility Segregation) 模式。對於寫入操作 (Commands)，使用命令物件和處理器；對於讀取操作 (Queries)，使用查詢物件和處理器。這有助於清晰地分離讀寫邏輯，進一步降低複雜度. 常用函式庫如 MediatR (用於處理 Command/Query) 或 Carter (微型 API 框架)。
5.  **內部通訊機制 (Internal Communication)：** 模組之間或切片之間需要通訊時，應避免直接依賴。常見的模式包括：
    *   **事件驅動 (Event-Driven)：** 透過領域事件 (Domain Events) 或整合事件 (Integration Events) 進行非同步通訊，解除耦合。
    *   **共享介面 (Shared Interfaces)：** 定義明確的介面供其他模組調用，但具體實現仍由各模組負責。

---

### (4). 實戰建議：為什麼這對用戶有用？

#### 4.1 .NET Aspire 對用戶的實戰建議

*   **大幅簡化本地開發環境設置與協作：** 用戶的 MESClient 和 CSS 都是前後端同 Web 專案，且有多個服務、快取 (Redis)、排程 (Hangfire) 等。ERP-Web 和 HKLogistics 更是多專案、多外部整合的巨型系統。Aspire 的 AppHost 可以將這些複雜的專案依賴（包括 SQL Server、Redis 容器）全部整合到一個啟動點。開發者無需手動啟動多個 `dotnet run` 或 IIS Express 實例，也無需管理複雜的 `launchSettings.json`，一鍵啟動整個解決方案，並透過 Aspire Dashboard 集中監控，極大地提升了開發者體驗與團隊協作效率.
*   **優化複雜應用程式的診斷與監控：** 專案目前使用 Elmah/Elastic APM 和 NLog 進行錯誤監控和日誌記錄。Aspire 內建的 OpenTelemetry 整合，可以為所有服務提供統一的分散式追蹤、指標和日誌收集。這對於診斷跨服務調用的性能瓶頸或錯誤流動尤其有效，例如追蹤一個前端請求在 MESClient 中經過 API Controller -> Service -> Logic -> EF Core 的完整鏈路.
*   **為未來架構演進提供清晰路徑：** 儘管目前多為單體應用，但隨著業務發展，部分核心功能可能需要拆分為獨立服務。Aspire 提供了一種模式，讓用戶可以在現有基礎上，逐步將子服務（例如 ERP-Web 中的特定外部 API 整合或 AI 服務）定義為獨立資源，並利用 Aspire 進行本地協調與雲端部署，為未來的微服務 (microservices) 或分散式應用 (distributed applications) 轉型鋪平道路. 對於 .NET Framework 的 ERP-Web 和 HKLogistics，Aspire 也是一個強大的推動力，鼓勵將業務模組升級到 .NET 8+ 以享受現代化的開發與部署優勢。

#### 4.2 模組化單體與垂直切片架構 對用戶的實戰建議

*   **解決大型 BLL/Service 層的維護夢魘：** ERP-Web 的 BLL 層有 167 個檔案，CSS 的 Service/Logic 層也相當龐大。傳統的分層架構導致單一業務功能程式碼分散。垂直切片架構能將類似「製程報工 (ManufactureProcess)」或「客戶案件 (CustomerIssue)」這樣的功能模組，從 Controller 到資料存取一次性切分，並將所有相關程式碼放在一個獨立的資料夾或命名空間下。這將大幅降低新進開發人員的學習曲線，並提高修改現有功能的信心與效率.
*   **提升開發速度與減少合併衝突：** 當多個開發者同時開發不同功能時，傳統分層架構容易導致在同一個 Service 或 Logic 檔案上產生大量合併衝突。垂直切片則能讓開發者在各自的切片內工作，減少跨檔案的衝突，加快開發速度.
*   **為前端應用帶來更清晰的 API 設計：** MESClient、CSS、LXKiosk 都大量使用 Kendo UI + jQuery + ES6。採用垂直切片後，每個業務功能模組可以定義自己專屬的 API 端點和資料模型 (ViewModel)，使前後端介面更加清晰與內聚，避免通用 API 變得臃腫。
*   **有利於未來部分業務模組的微服務化：** 對於 ERP-Web 中一些獨立性較高且需要頻繁迭代的模組（如「Agrigo 農業電商」或「AI 智能服務」），可以先以模組化單體的方式進行開發，未來再將這些「垂直切片」獨立部署為微服務，降低一次性大規模重構的風險。

---

### (5). Lab 提案（實作專案）：結合 Aspire 與模組化單體

#### 專案名稱：MES 報工模組現代化 PoC (MES Reporting Module Modernization PoC)

**目標：** 針對用戶現有 MESClient 專案中的「製程報工 (ManufactureProcess)」模組，利用 .NET Aspire 建立一個現代化的開發環境，並將該模組重構為一個獨立的「模組化單體」垂直切片，展示其在開發效率與維護性上的提升。

**預計時間：** 4 小時

**實作步驟：**

1.  **環境建置 (30 分鐘)：**
    *   安裝 .NET 8 SDK 及 .NET Aspire 工作負載 (`dotnet workload install aspire`)。
    *   使用 Aspire 模板建立一個新的解決方案：`dotnet new aspire --help`，然後 `dotnet new aspire -n MesReportingModernization`。
    *   新解決方案包含 `MesReportingModernization.AppHost` 和 `MesReportingModernization.ServiceDefaults` 專案。

2.  **核心業務模組提取與垂直切片重構 (2 小時)：**
    *   在 Aspire 解決方案中，添加一個新的 ASP.NET Core Web API 專案，命名為 `MesReportingModernization.ManufactureProcess`，模擬 MESClient 的「製程報工」模組。
    *   從 MESClient 專案中，**假想性地**提取「製程報工」相關的 Controller (例如 `ManufactureProcessController` 或相關 API Controller)、Service (`ManufactureProcessServices`)、Logic (`ManufactureProcessLogics`) 以及其依賴的 EF Core Model (Entities/ViewModels) 到新的 `MesReportingModernization.ManufactureProcess` 專案。
    *   **應用垂直切片概念：**
        *   移除傳統的 Service/Logic 分層，改為以「用例」為中心的垂直切片。例如，`ReportWorkOrderCommand` (命令) 和 `ReportWorkOrderCommandHandler` (處理器)。
        *   使用 MediatR (透過 `dotnet add package MediatR`) 在 `ManufactureProcess` 專案內實現命令/查詢處理。
        *   在該專案內部實現一個簡化的 EF Core DbContext 來存取「報工」相關的資料（可以使用 In-Memory Database 簡化設定）。
    *   創建一個前端頁面 (Razor View 或簡單的 HTML/JS) 在 `MesReportingModernization.Web` (由 Aspire 預設生成或手動添加一個 Web 專案) 中，呼叫 `MesReportingModernization.ManufactureProcess` 的 API。

3.  **Aspire 整合與協調 (1 小時)：**
    *   修改 `MesReportingModernization.AppHost` 專案，將 `MesReportingModernization.Web` 和 `MesReportingModernization.ManufactureProcess` 兩個專案定義為 Aspire 資源：
        ```csharp
        var builder = DistributedApplication.CreateBuilder(args);
        var cache = builder.AddRedis("cache");
        // 假設需要一個資料庫，可以添加 SQL Server 容器
        var db = builder.AddSqlServer("sqlserver").PublishAsContainer();

        var manufactureProcessApi = builder.AddProject<Projects.MesReportingModernization_ManufactureProcess>("manufactureprocessapi")
                                            .WithReference(db) // API 依賴資料庫
                                            .WithReference(cache); // API 依賴快取

        builder.AddProject<Projects.MesReportingModernization_Web>("webfrontend")
               .WithReference(manufactureProcessApi); // 前端依賴 API

        builder.Build().Run();
        ```
    *   配置 `manufactureprocessapi` 專案的 `appsettings.json` 以接收 Aspire 注入的連線字串。
    *   運行 `MesReportingModernization.AppHost` 專案，觀察 Aspire Dashboard 顯示的服務狀態、日誌、環境變數。

4.  **驗證與觀察 (30 分鐘)：**
    *   透過 Aspire Dashboard 確保所有服務（Web Frontend, ManufactureProcess API, Redis, SQL Server）都能正常啟動。
    *   測試前端頁面能否成功調用 `ManufactureProcess` API 並顯示資料。
    *   觀察 Aspire Dashboard 中的日誌和追蹤，理解請求如何流經不同服務。
    *   體會透過 Aspire 統一管理多服務的便捷性，以及垂直切片在程式碼組織上的清晰度。

**預期成果：**
*   一個能夠透過 Aspire 統一啟動和監控的簡單多服務應用。
*   「製程報工」模組作為一個獨立的垂直切片，展示其高內聚的程式碼組織方式。
*   理解 Aspire 如何簡化複雜應用程式的本地開發與診斷。
*   對模組化單體與垂直切片架構的實踐方式有初步概念。

---

### (6). 參考文獻：

1.  **.NET Aspire 官方文件：** Learn about .NET Aspire.
    `https://learn.microsoft.com/en-us/dotnet/aspire/`
2.  **Modular Monoliths with .NET - Jimmy Bogard：** A foundational article discussing the benefits of modular monoliths.
    `https://jimmybogard.com/the-modular-monolith-with-net/`
3.  **Deploy .NET Aspire apps to Azure Container Apps：** Official guide on deploying Aspire apps.
    `https://learn.microsoft.com/en-us/dotnet/aspire/deployment/azure/aca`
4.  **Vertical Slice Architecture - Jimmy Bogard：** Another key article by Jimmy Bogard on vertical slice architecture.
    `https://jimmybogard.com/vertical-slice-architecture/`
5.  **What is .NET Aspire and how does it help build distributed applications?：** An overview of Aspire's features and benefits.
    `https://www.infoworld.com/article/3714571/what-is-net-aspire-and-how-does-it-help-build-distributed-applications.html`
6.  **ASP.NET Core Vertical Slice Architecture with MediatR：** A practical guide to implementing vertical slice architecture in ASP.NET Core.
    `https://medium.com/itnext/asp-net-core-vertical-slice-architecture-with-mediatr-a5796a587ce9`
7.  **Microsoft .NET Aspire has reached general availability：** News on Aspire's GA release.
    `https://azure.microsoft.com/en-us/updates/microsoft-net-aspire-has-reached-general-availability/`
8.  **.NET Aspire GitHub Repository：**
    `https://github.com/dotnet/aspire`
9.  **MediatR GitHub Repository：**
    `https://github.com/jbogard/MediatR`

---