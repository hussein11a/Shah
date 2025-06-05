
import requests
import sys
import json

class NetlifyCMSAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except json.JSONDecodeError:
                    return success, {"content": response.text}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    return False, response.json()
                except json.JSONDecodeError:
                    return False, {"error": response.text}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {"error": str(e)}

    def test_api_root(self):
        """Test the API root endpoint"""
        return self.run_test(
            "API Root Endpoint",
            "GET",
            "api",
            200
        )
    
    def test_status_endpoint(self):
        """Test the status endpoint"""
        return self.run_test(
            "Status Endpoint",
            "GET",
            "api/status",
            200
        )
    
    def test_create_status(self):
        """Test creating a status check"""
        return self.run_test(
            "Create Status Check",
            "POST",
            "api/status",
            200,
            data={"client_name": "test_client"}
        )

def main():
    # Get backend URL from environment
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                backend_url = line.strip().split('=')[1].strip('"')
                break
    
    print(f"Testing backend API at: {backend_url}")
    
    # Setup tester
    tester = NetlifyCMSAPITester(backend_url)
    
    # Run tests
    api_root_success, api_root_response = tester.test_api_root()
    if api_root_success:
        print(f"API Root Response: {api_root_response}")
    
    status_success, status_response = tester.test_status_endpoint()
    if status_success:
        print(f"Status Endpoint Response: {status_response}")
    
    create_success, create_response = tester.test_create_status()
    if create_success:
        print(f"Create Status Response: {create_response}")
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
      