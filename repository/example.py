from typing import List, Optional
from dataclasses import dataclass

# --- 1. 模擬資料庫 (Mock Database) ---
# 在真實世界中，這裡會是 SQLAlchemy 的 Session 或是 PostgreSQL 連線
class MockDatabase:
    def __init__(self):
        self.users = []  # 用 List 模擬 Table

    def select_all_users(self):
        return self.users

    def insert_user(self, user_data):
        self.users.append(user_data)

# 定義 User 資料結構
@dataclass
class User:
    id: int
    username: str
    email: str

# ==========================================
# ❌ Bad Practice: 直接在商業邏輯中操作資料庫
# ==========================================
class UserManagerBad:
    def __init__(self, db: MockDatabase):
        self.db = db

    def create_user(self, user_id, username, email):
        # 商業邏輯混合了資料存取邏輯
        # 如果以後資料庫從 List 改成 SQL，這裡整段都要重寫
        user_record = {"id": user_id, "username": username, "email": email}
        self.db.insert_user(user_record)
        print(f"[Bad] Created user: {username}")

    def get_all_users(self):
        # 直接依賴底層實作
        raw_data = self.db.select_all_users()
        return [User(**u) for u in raw_data]

# ==========================================
# ✅ Good Practice: Repository Pattern
# ==========================================

# 1. 定義 Repository 介面 (抽象層)
# 它的工作只有一個：單純地對 User 進行 CRUD，不包含複雜商業邏輯
class UserRepository:
    def __init__(self, db: MockDatabase):
        self.db = db

    def add(self, user: User):
        # 這裡封裝了「如何存入資料庫」的細節
        # 轉成 DB 格式 (Dict)
        record = {"id": user.id, "username": user.username, "email": user.email}
        self.db.insert_user(record)

    def list_all(self) -> List[User]:
        # 這裡封裝了「如何取出資料」的細節
        # 從 DB 格式轉回 Object
        raw_data = self.db.select_all_users()
        return [User(**u) for u in raw_data]

    def find_by_id(self, user_id: int) -> Optional[User]:
        raw_data = self.db.select_all_users()
        for u in raw_data:
            if u['id'] == user_id:
                return User(**u)
        return None

# 2. 商業邏輯層 (Service)
# 它只跟 Repository 對話，完全不知道資料庫是 List 還是 SQL
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_id: int, username: str, email: str):
        # 這裡只處理商業邏輯 (例如檢查 email 格式，或是建立物件)
        new_user = User(id=user_id, username=username, email=email)
        
        # 存檔的工作交給 Repo
        self.user_repo.add(new_user)
        print(f"[Good] Registered user via Repo: {username}")

# --- 執行測試 ---
if __name__ == "__main__":
    # 初始化 DB
    db = MockDatabase()

    # 使用 Pattern
    repo = UserRepository(db)
    service = UserService(repo)

    service.register_user(1, "Alice", "alice@example.com")
    service.register_user(2, "Bob", "bob@example.com")

    # 驗證
    users = repo.list_all()
    for user in users:
        print(f"Found user: {user}")