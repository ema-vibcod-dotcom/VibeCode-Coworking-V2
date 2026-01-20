import requests
import datetime
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
    # 1. Login User
    print("--- 1. Login User ---")
    login_url = f"{BASE_URL}/usuario/login"
    resp = SESSION.post(login_url, data={'nombre': 'UserVerify', 'password': 'user'}, allow_redirects=True)
    if 'Reservar Espacio' in resp.text:
        print_result("User Login", True)
    else:
        print_result("User Login", False, "Could not login.")

    # 2. Check Dashboard (Empty state)
    print("--- 2. Dashboard Empty State ---")
    dash_url = f"{BASE_URL}/usuario/dashboard"
    resp = SESSION.get(dash_url)
    if "Estado Actual:" in resp.text and "Ingreso registrado" not in resp.text:
        print_result("Empty Dashboard", True)
    else:
        print_result("Empty Dashboard", False)

    # 3. Create Reservation for NOW
    print("--- 3. Create Reservation for NOW ---")
    create_url = f"{BASE_URL}/reserva/crear"
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    start_time = (now - datetime.timedelta(minutes=5)).strftime('%H:%M')
    end_time = (now + datetime.timedelta(hours=1)).strftime('%H:%M')
    
    data = {'espacio_id': 1, 'fecha': today, 'hora_inicio': start_time, 'hora_fin': end_time}
    resp = SESSION.post(create_url, data=data, allow_redirects=True)
    
    # 4. Check-in (Should link to reservation)
    print("--- 4. Check-in linked to reservation ---")
    checkin_url = f"{BASE_URL}/usuario/checkin"
    resp = SESSION.post(checkin_url, allow_redirects=True)
    if "Asociado a tu reserva" in resp.text:
        print_result("Linked Check-in", True)
    else:
        print_result("Linked Check-in", False)

    # 5. Dashboard (Active state with reservation)
    print("--- 5. Dashboard with reservation ---")
    resp = SESSION.get(dash_url)
    if "Ingreso registrado:" in resp.text and "Coworking General" in resp.text:
        print_result("Dashboard Detail", True)
    else:
        print_result("Dashboard Detail", False)

    # 6. Check-out
    print("--- 6. Check-out ---")
    checkout_url = f"{BASE_URL}/usuario/checkout"
    resp = SESSION.post(checkout_url, allow_redirects=True)
    if "Check-out exitoso" in resp.text:
        print_result("Check-out", True)
    else:
        print_result("Check-out", False)

    print("\nALL DASHBOARD TESTS PASSED")

if __name__ == "__main__":
    run_verification()
