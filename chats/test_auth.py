import requests
import json

# Base URL - your server is running here
BASE_URL = "http://127.0.0.1:8000/api"

def test_authentication():
    print("🔐 Testing JWT Authentication...")
    
    # Use the credentials you just created - with EMAIL field
    login_data = {
        "email": "morad@gmail.com",  # Changed from "username" to "email"
        "password": "REALmorad88"  # Use the password you set
    }
    
    # 1. Get JWT tokens
    print("\n1. Getting JWT tokens...")
    try:
        response = requests.post(
            f"{BASE_URL}/token/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            
            print("✅ Login successful!")
            print(f"Access token: {access_token[:50]}...")
            print(f"Refresh token: {refresh_token[:50]}...")
            
            # 2. Test protected endpoint - Conversations
            print("\n2. Testing protected endpoints...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test conversations endpoint
            conversations_response = requests.get(
                f"{BASE_URL}/conversations/",
                headers=headers
            )
            
            if conversations_response.status_code == 200:
                print("✅ Conversations endpoint access successful!")
                data = conversations_response.json()
                print(f"Conversations: {data}")
            else:
                print(f"❌ Conversations endpoint failed: {conversations_response.status_code}")
                print(f"Response: {conversations_response.text}")
            
            # Test users endpoint
            users_response = requests.get(
                f"{BASE_URL}/users/",
                headers=headers
            )
            
            if users_response.status_code == 200:
                print("✅ Users endpoint access successful!")
                users_data = users_response.json()
                print(f"Users data received")
            else:
                print(f"❌ Users endpoint failed: {users_response.status_code}")
                
            # 3. Test token refresh
            print("\n3. Testing token refresh...")
            refresh_response = requests.post(
                f"{BASE_URL}/token/refresh/",
                json={"refresh": refresh_token},
                headers={"Content-Type": "application/json"}
            )
            
            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                print("✅ Token refresh successful!")
                print(f"New access token: {new_tokens['access'][:50]}...")
            else:
                print(f"❌ Token refresh failed: {refresh_response.status_code}")
                
            # 4. Test current user endpoint
            print("\n4. Testing current user endpoint...")
            me_response = requests.get(
                f"{BASE_URL}/users/me/",
                headers=headers
            )
            
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("✅ Current user endpoint successful!")
                print(f"User: {user_data.get('first_name')} {user_data.get('last_name')} ({user_data.get('email')})")
            else:
                print(f"❌ Current user endpoint failed: {me_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            print("\n💡 Make sure you:")
            print("   - Used the correct password")
            print("   - Server is running on http://127.0.0.1:8000/")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_authentication()