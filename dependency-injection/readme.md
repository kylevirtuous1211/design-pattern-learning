Dependency Injection (DI) Pattern

1. 最小可行的範例 (Minimal Working Example)

請參考同目錄下的 example.py。
我們展示了 UserController 如何不再自己建立 EmailService，而是透過 __init__ 接收外部傳入的 Service。

改成 Dependency Injection 的 `UserControllerGood` class，可以自由地用dependency 調換使用的 class 或 function，而不用重新改程式碼

2. 使用該 Pattern 的原因 (Why)

核心目的是 解耦 (Decoupling) 與 控制反轉 (Inversion of Control)。

可測試性：這是最重要的原因。在單元測試中，我們不希望真的寄信、真的扣款或真的連線資料庫。透過 DI，我們可以輕鬆注入一個「假的 (Mock)」物件來進行測試。

靈活性：如果今天要把 EmailService 換成 SMSService，我們只需要在程式啟動的地方修改傳入的物件，而不用修改 UserController 內部的程式碼。

3. 在真實專案的常見使用場景

FastAPI Depends()：
這是最經典的例子。當我們寫 def get_user(db = Depends(get_db)) 時，FastAPI 框架充當了「Injector」，它幫我們建立了 db 連線並注入給函式使用。我們不需要在每個 API 函式裡面寫 SessionLocal()。

1. 不使用此 Pattern 的壞處 (For MR Description)

如果在類別內部直接實例化依賴物件（例如 self.db = Database()）：

無法測試：單元測試會被迫連線真實的資料庫或 API，導致測試變慢、資料髒亂，甚至誤觸真實的付費服務。

高耦合：如果要更換底層實作（例如從 MySQL 換成 PostgreSQL），必須深入修改每一個使用到資料庫的類別，違反了開閉原則 (Open-Closed Principle)。