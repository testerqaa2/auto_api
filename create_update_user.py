import random
from playwright.sync_api import sync_playwright
from faker import Faker

class create_update_user:
    BASE_URL = "https://reqres.in/api/users"
    HEADERS = {
        "x-api-key": "reqres-free-v1",
        "Content-Type": "application/json"
    }
    
    def __init__(self):
        self.fake = Faker()
        self.created_user_id = None
        self.original_user_data = None
    
    def generate_user_data(self):
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        return {
            "name": f"{first_name} {last_name}",
            "job": self.fake.job()
        }
    
    def test_create_user(self):
        with sync_playwright() as p:
            api_context = p.request.new_context(
                extra_http_headers=self.HEADERS
            )
            
            try:
                user_data = self.generate_user_data()
                self.original_user_data = user_data.copy()
                
                request_body = {
                    "name": user_data["name"],
                    "job": user_data["job"]
                }
                
                print(f"1. Creating a new user \n")
                print(f"------------ Request Data ------------")
                print(f"   Name: {user_data['name']}")
                print(f"   Job : {user_data['job']}")
                
                response = api_context.post(
                    self.BASE_URL,
                    data=request_body
                )
                
                assert response.status == 201, f"Expected 201, got {response.status}"
                response_json = response.json()

                self.created_user_id = response_json["id"]
                
                assert response_json["name"] == user_data["name"]
                assert response_json["job"] == user_data["job"]
                assert "id" in response_json
                assert "createdAt" in response_json

                print(f"\n------------ Output ------------------")
                print("✅ Success create a new user")
                print(f"   User ID   : {response_json['id']}")
                print(f"   User Name : {response_json['name']}")
                print(f"   User Job  : {response_json['job']}")
                print(f"   Created At: {response_json['createdAt']} \n")

                return True
                
            except Exception as e:
                print(f"❌ FAILED to Create a new user: {str(e)}")
                return False
            
            finally:
                api_context.dispose()

    def test_update_user(self):
        if not self.created_user_id:
            print("❌ Can't run update user - No user ID available from create test case")
            return False
        
        with sync_playwright() as p:
            api_context = p.request.new_context(
                extra_http_headers=self.HEADERS
            )
            
            try:
                new_user_data = self.generate_user_data()
                
                request_body = {
                    "name": new_user_data["name"],
                    "job": new_user_data["job"]
                }
                
                print(f"2. Updating user ID: {self.created_user_id} \n")
                print(f"---------------------- Previous Data -----------------")
                print(f"   Name: {self.original_user_data['name']}")
                print(f"   Job : {self.original_user_data['job']}")
                print(f"---------------------- New Data ----------------------")
                print(f"   Name: {new_user_data['name']}")
                print(f"   Job : {new_user_data['job']} \n")

                response = api_context.put(
                    f"{self.BASE_URL}/{self.created_user_id}",
                    data=request_body
                )
                
                assert response.status == 200, f"Expected 200, got {response.status}"
                response_json = response.json()
                
                assert response_json["name"] == new_user_data["name"]
                assert response_json["job"] == new_user_data["job"]
                assert "updatedAt" in response_json
                        
                print(f"---------------------- Output ------------------------")
                print("✅ Success update existing user data")
                print(f"   User ID   : {self.created_user_id}")
                print(f"   User Name : {response_json['name']}")
                print(f"   User Job  : {response_json['job']}")
                print(f"   Updated At: {response_json['updatedAt']} \n")
                
                return True
                
            except Exception as e:
                print(f"❌ FAILED to Update existing user: {str(e)}")
                return False
            
            finally:
                api_context.dispose()

    def test_complete_flow(self):

        print("\n TEST CREATE AND UPDATE USER DATA \n")
        
        create_success = self.test_create_user()
        
        if not create_success:
            print("❌ CREATE USER FAILED ")
            return False
        
        update_success = self.test_update_user()
        
        if create_success and update_success:
            print(f"✅ Successfully create and update user data with ID =  {self.created_user_id} ")
        else:
            print("❌ FAILED - Some tests didn't pass")
            if not create_success:
                print("   ❌ Create a new user test is failed")
            if not update_success:
                print("   ❌ Update the existing user test is failed")
        
        return create_success and update_success

def main():
    test = create_update_user()
    test.test_complete_flow()

if __name__ == "__main__":
    main()