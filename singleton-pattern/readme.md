

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
