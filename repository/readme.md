# Repository Pattern (倉儲模式)

## 1. 最小可行的範例 (Minimal Working Example)

請參考同目錄下的 example.py。

我們模擬了一個資料庫，並建立了 UserRepository 來負責所有的資料存取操作。UserService (商業邏輯) 透過 Repository 來存取特定的User object，而不是直接在service操作新增一串 dictionary 到資料庫。

## 2. 使用該 Pattern 的原因 (Why)

Repository Pattern 的核心目的是 將「商業邏輯」與「資料存取邏輯」分離 (Decoupling)。

抽象化：商業邏輯不需要知道底層DB是 SQL、NoSQL 還是純文字檔。

可測試性：測試商業邏輯時，可以輕鬆換成一個「假」的 Repository (Mock)，而不需要真的連連資料庫。

集中管理：所有的 SQL 查詢都集中在一個地方。如果資料庫欄位改名了，只要改 Repository 一個檔案，不用改遍所有程式碼。

## 3. 在真實專案的常見使用場景

FastAPI + SQLAlchemy：
在 Web 後端開發中，我們通常會建立 crud.py 或 repositories/user.py。
API Endpoint (Controller) 呼叫 Repository，Repository 呼叫 SQLAlchemy Session。

更換資料源：
專案初期使用 SQLite，後期遷移到 PostgreSQL；或者某些資料從資料庫移到了 Redis 快取。使用此模式時，上層的程式碼完全不用修改。

## 4. 不使用此 Pattern 的壞處 (Also for MR)

如果我們不使用 Repository Pattern，而是在 API function 裡面直接寫 SQL 查詢或 ORM 操作：

* 程式碼重複：同樣的 SELECT * FROM users WHERE ... 查詢可能會散落在專案的十幾個地方。

* 難以維護：一旦資料庫 Schema 變更（例如 user_name 改成 username），必須全域搜尋並修改所有檔案。

* 難以測試：要測試 API 時，必須真的架設一個測試用資料庫，測試速度變慢且環境建置困難。

### Example

* 不用寫：SELECT * FROM users WHERE id = 1 (這句 parameter 寫在外面)
* 只要寫：repo.find_by_id(1) (這句乾淨清爽)
* 以及換資料庫種類時，可以直接改 DB 的程式，使其也能使用 User Object type