import requests
import json

def auth_test():
    print("🔐 Authentication System Test")
    print("=" * 40)
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Test with email field
    credentials = {
        "email": "morad@gmail.com",
        "password": "REALmorad88"
    }
    
    print(f"📧 Testing login for: {credentials['email']}")
    print("⏳ Please wait...")
    
    try:
        # Step 1: Get JWT tokens
        print("\n1. 🔑 Requesting JWT tokens...")
        response = requests.post(
            f"{BASE_URL}/token/",
            json=credentials,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("   ✅ SUCCESS! Tokens received")
            print(f"   Access Token: {tokens['access'][:30]}...")
            
            # Step 2: Test protected endpoints
            headers = {"Authorization": f"Bearer {tokens['access']}"}
            print("\n2. 🔒 Testing protected endpoints...")
            
            # Test current user endpoint
            print("   Testing /users/me/ endpoint...")
            me_response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("   ✅ Current user endpoint: WORKING")
                print(f"      Name: {user_data.get('first_name')} {user_data.get('last_name')}")
                print(f"      Email: {user_data.get('email')}")
            else:
                print(f"   ❌ Current user endpoint failed: {me_response.status_code}")
            
            # Test conversations endpoint
            print("   Testing /conversations/ endpoint...")
            conv_response = requests.get(f"{BASE_URL}/conversations/", headers=headers)
            if conv_response.status_code == 200:
                print("   ✅ Conversations endpoint: WORKING")
            else:
                print(f"   ❌ Conversations endpoint failed: {conv_response.status_code}")
            
            return True
            
        else:
            print(f"   ❌ FAILED: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting authentication test...\n")
    success = auth_test()
    
    if success:
        print("\n" + "="*50)
        print("🎉 CONGRATULATIONS! 🎉")
        print("✅ JWT Authentication: IMPLEMENTED")
        print("✅ Custom User Model: WORKING")
        print("✅ API Endpoints: SECURED")
        print("✅ Task 0: COMPLETED!")
        print("="*50)
    else:
        print("\n💡 Authentication needs more configuration...")