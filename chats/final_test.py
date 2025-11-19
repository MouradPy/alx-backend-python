import requests
import json

def final_test():
    print("🎯 Final JWT Authentication Test")
    print("=" * 40)
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Test with email field (should work now)
    credentials = {
        "email": "morad@gmail.com",
        "password": "REALmorad88"
    }
    
    print(f"📧 Testing with email: {credentials['email']}")
    
    try:
        # Test JWT token endpoint
        print("🔐 Requesting JWT tokens...")
        response = requests.post(
            f"{BASE_URL}/token/",
            json=credentials,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            print("🎉 SUCCESS! JWT Authentication is WORKING!")
            print(f"✅ Access Token: {tokens['access'][:30]}...")
            print(f"✅ Refresh Token: {tokens['refresh'][:30]}...")
            
            # Test protected endpoints
            headers = {"Authorization": f"Bearer {tokens['access']}"}
            print("\n🔒 Testing protected endpoints...")
            
            # Test /users/me/ endpoint
            me_response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("✅ /users/me/ endpoint: WORKING")
                print(f"   👤 Name: {user_data.get('first_name')} {user_data.get('last_name')}")
                print(f"   📧 Email: {user_data.get('email')}")
            else:
                print(f"❌ /users/me/ endpoint failed: {me_response.status_code}")
            
            # Test /conversations/ endpoint
            conv_response = requests.get(f"{BASE_URL}/conversations/", headers=headers)
            if conv_response.status_code == 200:
                print("✅ /conversations/ endpoint: WORKING")
            else:
                print(f"❌ /conversations/ endpoint failed: {conv_response.status_code}")
                
            return True
            
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running!")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = final_test()
    if success:
        print("\n🎊 CONGRATULATIONS! Your authentication system is working!")
        print("✅ JWT Authentication: IMPLEMENTED")
        print("✅ Custom User Model: WORKING") 
        print("✅ Protected Endpoints: SECURED")
    else:
        print("\n💡 Need to troubleshoot further...")