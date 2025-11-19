import time
from dataclasses import dataclass


class MockCasbinEnforcer:
    def __init__(self):
        # create enforcer needs a lot of time
        time.sleep(3.0)
        print("created an enforcer")
        
    def enforce(self, user: str, resource: str, method: str):
        print("enforced")
        
class BadAuthControl:
    def check_permission(self, user, resource, method):
        enforcer = MockCasbinEnforcer()
        return enforcer.enforce(user, resource, method)
        
shared_singleton_enforcer = MockCasbinEnforcer()

class GoodAuthControl:
    def check_permission(self, user, resource, method):
        enforcer = shared_singleton_enforcer
        return enforcer.enforce(user, resource, method)
        
if __name__ == "__main__":
    good_controller = GoodAuthControl()
    bad_controller = BadAuthControl()
    
    print("test each with 3 requests")
    print("\n--- 1. Testing Bad Practice (3 requests) ---")
    start_time = time.time()
    for i in range(3):
        print(f"Request {i+1}:")
        bad_controller.check_permission("alice", "data", "read")
    print(f"❌ Bad Practice Total Time: {time.time() - start_time:.2f} seconds")
    
    print("\n--- 2. Testing Good Practice (3 requests) ---")
    start_time = time.time()
    for i in range(3):
        print(f"Request {i+1}:")
        good_controller.check_permission("alice", "data", "read")
    print(f"✅ Good Practice Total Time: {time.time() - start_time:.2f} seconds")