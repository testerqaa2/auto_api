import random
from playwright.sync_api import sync_playwright
from faker import Faker

class create_user:
    BASE_URL = "https://reqres.in/api/users"
    HEADERS = {
        "x-api-key": "reqres-free-v1",
        "Content-Type": "application/json"
    }
    
    def __init__(self):
        self.fake = Faker()
    
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
                
                request_body = {
                    "name": user_data["name"],
                    "job": user_data["job"]
                }
                
                print(f"Creating a new user")
                print(f"------------Request Data------------")
                print(f"   Name: {user_data['name']}")
                print(f"   Job : {user_data['job']}")
                
                response = api_context.post(
                    self.BASE_URL,
                    data=request_body
                )
                
                assert response.status == 201
                response_json = response.json()
                
                assert response_json["name"] == user_data["name"]
                assert response_json["job"] == user_data["job"]
                assert "id" in response_json
                assert "createdAt" in response_json

                print(f"------------Output------------------")
                print("✅ Success create a new user")
                print(f"   User ID   : {response_json['id']}")
                print(f"   User Name : {response_json['name']}")
                print(f"   User Job  : {response_json['job']}")
                print(f"   Created At: {response_json['createdAt']}")
                
            finally:
                api_context.dispose()

if __name__ == "__main__":
    test = create_user()
    test.test_create_user()