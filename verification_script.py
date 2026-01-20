import requests
from bs4 import BeautifulSoup
import sys

BASE_URL = "http://127.0.0.1:5001"
SESSION = requests.Session()

def print_result(step, success, message=""):
    if success:
        print(f"[PASS] {step}")
    else:
        print(f"[FAIL] {step}: {message}")
        sys.exit(1)

def run_verification():
    # 1. Register/Login Admin
    print("--- 1. Admin Registration/Login ---")
    
    # Try to register first
    reg_url = f"{BASE_URL}/admin/registro_inicial"
    try:
        resp = SESSION.get(reg_url)
        if resp.status_code != 200:
             print_result("Get Registration Page", False, f"Status {resp.status_code}")
        
        # csrf? flask-wtf not used, so plain form
        
        # Attempt Register
        resp = SESSION.post(reg_url, data={'nombre': 'AdminVerify', 'password': 'admin'}, allow_redirects=True)
        
        # Should redirect to login or show error if admin exists
        # We assume we are redirected to login or we are there.
        # Let's try to login now. 
        # Note: If admin already exists, the post might accept it or flash error. We just try login.
    except Exception as e:
        print_result("Registration Request", False, str(e))

    # Login
    login_url = f"{BASE_URL}/admin/login"
    resp = SESSION.post(login_url, data={'nombre': 'AdminVerify', 'password': 'admin'}, allow_redirects=True)
    
    if '/admin/dashboard' in resp.url or '/admin/usuarios' in resp.url:
        print_result("Admin Login", True)
    else:
        # Try Login as 'Admin' (maybe created in previous step)
        resp = SESSION.post(login_url, data={'nombre': 'Admin', 'password': 'admin'}, allow_redirects=True)
        if '/admin/dashboard' in resp.url or '/admin/usuarios' in resp.url:
            print_result("Admin Login (Fallback)", True)
        else:
             print_result("Admin Login", False, "Could not login as AdminVerify or Admin")

    # 2. Create User
    print("--- 2. Create User ---")
    create_user_url = f"{BASE_URL}/admin/usuarios"
    resp = SESSION.post(create_user_url, data={'nombre': 'UserVerify', 'password': 'user'}, allow_redirects=True)
    
    if resp.status_code == 200 and 'UserVerify' in resp.text:
        print_result("Create User", True)
    else:
         print_result("Create User", False, "UserVerify not found in list")

    # 3. Logout Admin
    logout_url = f"{BASE_URL}/admin/logout"
    SESSION.get(logout_url)
    
    # 4. Login User
    print("--- 3. User Flow ---")
    user_login_url = f"{BASE_URL}/usuario/login"
    resp = SESSION.post(user_login_url, data={'nombre': 'UserVerify', 'password': 'user'}, allow_redirects=True)
    
    if '/usuario/dashboard' in resp.url:
        print_result("User Login", True)
    else:
        print_result("User Login", False, "Failed to login as UserVerify")
        
    if "FUERA" in resp.text.upper():
        print_result("Initial Status FUERA", True)
    else:
        print_result("Initial Status FUERA", False, "Status not found")

    # 5. Check-in
    checkin_url = f"{BASE_URL}/usuario/checkin"
    resp = SESSION.post(checkin_url, allow_redirects=True)
    
    if "DENTRO" in resp.text.upper():
         print_result("Check-in", True)
    else:
         print_result("Check-in", False, "Status did not change to DENTRO")

    # 6. Check-out
    checkout_url = f"{BASE_URL}/usuario/checkout"
    resp = SESSION.post(checkout_url, allow_redirects=True)
    
    if "FUERA" in resp.text.upper():
         print_result("Check-out", True)
    else:
         print_result("Check-out", False, "Status did not change to FUERA")
         
    # 7. Verify Log details
    print("--- 4. Verify Logs ---")
    SESSION.get(f"{BASE_URL}/usuario/logout")
    
    # Login Admin again
    resp = SESSION.post(login_url, data={'nombre': 'AdminVerify', 'password': 'admin'}, allow_redirects=True)
    # If failed, try Admin
    if '/admin' not in resp.url:
         resp = SESSION.post(login_url, data={'nombre': 'Admin', 'password': 'admin'}, allow_redirects=True)
         
    logs_url = f"{BASE_URL}/admin/registros"
    resp = SESSION.get(logs_url)
    
    if "UserVerify" in resp.text and "CERRADO" in resp.text.upper():
        print_result("Log Entry Found", True)
    else:
        print_result("Log Entry Found", False, "Log for UserVerify not found or not Closed")

    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    run_verification()
