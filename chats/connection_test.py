# save as connection_test.py
import requests

def test_connection():
    print("🔌 Testing Server Connection")
    print("=" * 30)
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Server is running! Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on port 8000")
        print("💡 Make sure to run: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()