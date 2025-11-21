# Decorator Pattern (裝飾者模式)

1. 最小可行的範例 (Minimal Working Example)

請參考同目錄下的 example.py。

我們建立了一個 @require_admin 的裝飾器。

Bad Practice：在 delete_user 和 export_report 函式內部，重複撰寫 if token != "admin" 的檢查邏輯。

Good Practice：將檢查邏輯抽取出來變成 Decorator。原本的函式上方只需加上 @require_admin，函式內部只剩下純粹的商業邏輯。

2. 使用該 Pattern 的原因 (Why)

核心目的是 分離關注點 (Separation of Concerns) 與 遵守 DRY 原則 (Don't Repeat Yourself)。

橫切關注點 (Cross-Cutting Concerns)：驗證、Log 紀錄、快取 (Cache)、計時等功能，通常會出現在系統的各個角落。Decorator 讓我們把這些邏輯集中管理，而不是散落在每個商業邏輯函式中。

開放封閉原則：我們不需要修改既有的 delete_user 程式碼，就能為它加上「權限檢查」的功能。

3. 在真實專案的常見使用場景

FastAPI / Flask Routing：
@app.get("/users") 就是一個 Decorator，它把你的函式「註冊」到 Web Server 的路由表中。

Authentication & Authorization：
在 Django 中常見的 @login_required，或是在我們專案中 FastAPI 的 Depends() 機制（雖然實作略有不同，但精神是透過 Dependency Injection 達到類似 Decorator 的效果，即在進入函式前先執行驗證）。

Logging & Timing：
建立一個 @timeit 裝飾器，自動計算並 print 出任何函式的執行時間，用於效能分析。

4. 不使用此 Pattern 的壞處 (For MR Description)

如果在每個 Endpoint 函式中直接撰寫驗證或 Log 邏輯：

程式碼重複：if check_auth(): ... 這種程式碼會被複製貼上幾百次。

容易遺漏：開發新功能時，容易忘記加上驗證邏輯，導致嚴重的安全漏洞（Security Hole）。

閱讀困難：商業邏輯（由 5 行程式碼組成）被淹沒在驗證與 Log 邏輯（由 20 行程式碼組成）之中，難以閱讀核心邏輯。