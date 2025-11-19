# Singleton Pattern (單例模式)

## 1. 最小可行的範例 (Minimal Working Example)

請參考同目錄下的 example.py。

我們模擬了一個 MockCasbinEnforcer，它在初始化時需要耗費大量時間（模擬從資料庫讀取權限規則）。

Bad Practice：在每個 Request 中都建立新的 Enforcer，導致回應時間極慢。

Good Practice：在程式啟動時只建立一次 Enforcer，之後所有 Request 重複使用該實例。

## 2. 使用該 Pattern 的原因 (Why)

核心目的是 效能優化 與 資源共享。

昂貴的初始化：某些物件的建立成本很高（如讀取大檔案、建立資料庫連線池、載入 AI 模型）。如果每次用完就丟，系統效能會崩潰。

狀態一致性：確保系統中只有「一份」真理。例如設定檔（Config）載入後，全系統應該都讀到同一份設定。

## 3. 在真實專案的常見使用場景

Casbin Enforcer：
這是本專案最痛的點。Enforcer 需要把 DB 裡的 Policy 全部載入記憶體建立決策樹。我們必須確保這件事只發生在 App 啟動時（Startup Event），而不是 API 被呼叫時。

Database Connection Pool：
建立 TCP 連線是很慢的。我們通常會建立一個全域的連線池（SessionLocal），讓所有 API 共享這個池子。

Global Configuration (Config)：
讀取 .env 或 config.yaml 後，轉成一個全域物件供各處讀取。

## 測試結果 log
```
$ python example.py 
created an enforcer
test each with 3 requests

--- 1. Testing Bad Practice (3 requests) ---
Request 1:
created an enforcer
enforced  
Request 2:
created an enforcer
enforced  
Request 3:
created an enforcer
enforced
❌ Bad Practice Total Time: 9.01 seconds      

--- 2. Testing Good Practice (3 requests) ---
Request 1:
enforced
Request 2:
enforced
Request 3:
enforced
✅ Good Practice Total Time: 0.00 seconds    
```
