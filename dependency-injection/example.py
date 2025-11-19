from dataclasses import dataclass

# --- 1. Dependencies (The Tools) ---

class EmailService:
    def send_email(self, message: str):
        print(f"[Real Email] Sending to SMTP server: {message}")

class MockEmailService:
    """A fake email service for testing."""
    def send_email(self, message: str):
        print(f"[Mock Email] Pretending to send: {message}")

# ==========================================
# ❌ Bad Practice: Hard-coded Dependency
# ==========================================
class UserControllerBad:
    def __init__(self):
        # The controller creates the service ITSELF.
        # We are stuck with 'EmailService'. We cannot use MockEmailService.
        self.email_service = EmailService() 

    def register(self, username: str):
        print(f"Registering {username}...")
        self.email_service.send_email(f"Welcome {username}!")

# ==========================================
# ✅ Good Practice: Dependency Injection
# ==========================================
class UserControllerGood:
    def __init__(self, email_service):
        # The controller ASKS for the service.
        # It doesn't care if it's real or mock, as long as it has a .send_email() method.
        self.email_service = email_service

    def register(self, username: str):
        print(f"Registering {username}...")
        self.email_service.send_email(f"Welcome {username}!")

# --- Execution ---
if __name__ == "__main__":
    print("--- Bad Practice Run ---")
    controller_bad = UserControllerBad()
    controller_bad.register("Alice") 
    # Problem: If I run this in a unit test, it actually sends an email! 😱

    print("\n--- Good Practice Run (Production) ---")
    real_service = EmailService()
    # We "Inject" the real service here
    controller_good_prod = UserControllerGood(real_service)
    controller_good_prod.register("Bob")

    print("\n--- Good Practice Run (Testing) ---")
    mock_service = MockEmailService()
    # We "Inject" the fake service here. Easy to test!
    controller_good_test = UserControllerGood(mock_service)
    controller_good_test.register("Charlie")