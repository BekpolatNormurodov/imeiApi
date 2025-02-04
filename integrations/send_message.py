import requests

# Eskiz API uchun login ma'lumotlari
EMAIL = "abdulbosit19980204@gmail.com"
# PASSWORD = "19980204"
PASSWORD = "XFd3a0W2n1sBim9hf0uIKRNstbe6ArQafNiDm62O"
BASE_URL = "https://notify.eskiz.uz/api"


def get_token():
    """Eskiz uchun autentifikatsiya tokenini olish."""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["data"]["token"]
    else:
        raise Exception(f"Token olishda xato: {response.json()}")


def send_sms(phone_number, message):
    """SMS yuborish."""
    token = get_token()
    url = f"{BASE_URL}/message/sms/send"
    user = requests.post(f"{BASE_URL}/user", headers={"Authorization": f"Bearer {token}"})
    print(user.json())
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "mobile_phone": phone_number,
        "message": message,
        "from": "4546"  # Eskiz'dan ruxsat olingan yuboruvchi nomi
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"SMS muvaffaqiyatli yuborildi: {response.json()}")
    else:
        print(f"SMS yuborishda xato: {response.json()}")

# Test qilish
# send_sms("900066639", "Bu Eskiz dan test")
