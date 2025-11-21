class AuthService:
    """微服務 A: 負責驗證"""
    def verify_token(self, token: str) -> dict:
        if token == "valid-token":
            return {"user": "Alice", "role": "admin", "is_valid": True}
        return {"is_valid": False}

class LLMBackend:
    """微服務 B: 負責 LLM 運算"""
    def generate_text(self, user_role: str, prompt: str):
        if user_role != "admin":
            return "Error: 403 Forbidden"
        return f"LLM Response for '{prompt}'"

# ==========================================
# ❌ Bad Practice: Client 直接呼叫各個微服務
# ==========================================
class ClientDirect:
    def __init__(self):
        # Client 必須知道所有後端服務的細節，耦合度極高
        self.auth_service = AuthService()
        self.llm_service = LLMBackend()

    def do_work(self, token: str, prompt: str):
        print("\n[Client Direct] Starting work...")
        
        # 1. Client 自己要負責去呼叫 Auth
        auth_result = self.auth_service.verify_token(token)
        if not auth_result["is_valid"]:
            print("  -> Auth Failed")
            return

        # 2. Client 自己要把 Auth 的結果傳給 LLM
        # 如果以後 LLM 改網址或改參數，Client 就要跟著改 (這就是前後端耦合)
        result = self.llm_service.generate_text(auth_result["role"], prompt)
        print(f"  -> Result: {result}")

# ==========================================
# ✅ Good Practice: API Gateway
# ==========================================
class APIGateway:
    """
    這就是 Nginx 在做的事。
    它是所有後端服務的單一入口。
    """
    def __init__(self):
        self.auth_service = AuthService()
        self.llm_service = LLMBackend()

    def handle_request(self, path: str, token: str, data: dict):
        # Gateway 統一處理驗證 (Authentication)
        # 這模擬了 Nginx 的 `auth_request`
        user_info = self.auth_service.verify_token(token)
        if not user_info["is_valid"]:
            return "401 Unauthorized"

        # Gateway 統一處理路由 (Routing)
        if path == "/api/v1/work":
            # Gateway 負責將使用者資訊注入請求 (Header Injection)
            return self.llm_service.generate_text(user_info["role"], data["prompt"])
        
        return "404 Not Found"

class ClientWithGateway:
    def __init__(self):
        self.gateway = APIGateway()

    def do_work(self, token: str, prompt: str):
        print("\n[Client with Gateway] Starting work...")
        # Client 只知道 Gateway，根本不知道後面有幾個微服務
        result = self.gateway.handle_request("/api/v1/work", token, {"prompt": prompt})
        print(f"  -> Result: {result}")

# --- Execution ---
if __name__ == "__main__":
    # 1. 沒有 Gateway：Client 很忙，邏輯很雜
    client_bad = ClientDirect()
    client_bad.do_work("valid-token", "Hello World")

    # 2. 有 Gateway：Client 很輕鬆，只要對口一個人
    client_good = ClientWithGateway()
    client_good.do_work("valid-token", "Hello World")