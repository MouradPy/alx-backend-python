import requests
import json

def test_jwt_fixed():
    print("🔐 Testing JWT Authentication with UUID Fix")
    print("=" * 50)
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Test with both field names to see which one works
    credentials_attempts = [
        {"email": "morad@gmail.com", "password": "REALmorad88"},  # Try email field
        {"username": "morad@gmail.com", "password": "REALmorad88"}  # Try username field
    ]
    
    for i, credentials in enumerate(credentials_attempts, 1):
        field_used = list(credentials.keys())[0]
        print(f"\n📨 Attempt {i}: Using '{field_used}' field...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/token/",
                json=credentials,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                tokens = response.json()
                print("✅ SUCCESS! JWT authentication working!")
                print(f"🔑 Access Token: {tokens['access'][:30]}...")
                print(f"🔄 Refresh Token: {tokens['refresh'][:30]}...")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {tokens['access']}"}
                print("\n🔒 Testing protected endpoint...")
                
                me_response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
                if me_response.status_code == 200:
                    user_data = me_response.json()
                    print("✅ Protected endpoint working!")
                    print(f"👤 User: {user_data.get('first_name')} {user_data.get('last_name')}")
                    print(f"📧 Email: {user_data.get('email')}")
                    print(f"🆔 User ID: {user_data.get('user_id')}")
                else:
                    print(f"⚠️  Protected endpoint: {me_response.status_code}")
                    print(f"Response: {me_response.text}")
                break
                
            else:
                print(f"❌ Failed with {field_used}: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        print("\n💡 Both attempts failed. Creating custom JWT serializer...")

if __name__ == "__main__":
    test_jwt_fixed()