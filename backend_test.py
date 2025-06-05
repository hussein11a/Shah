
import requests
import sys
import json
import yaml

class NetlifyCMSAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, is_json=True):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'} if is_json else {}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if is_json:
                    try:
                        return success, response.json()
                    except json.JSONDecodeError:
                        return success, {"content": response.text}
                else:
                    return success, {"content": response.text}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    return False, response.json() if is_json else {"error": response.text}
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
    
    def test_netlify_cms_admin_page(self):
        """Test the Netlify CMS admin page"""
        return self.run_test(
            "Netlify CMS Admin Page",
            "GET",
            "admin/index.html",
            200,
            is_json=False
        )
    
    def test_netlify_cms_config(self):
        """Test the Netlify CMS config file"""
        success, response = self.run_test(
            "Netlify CMS Config File",
            "GET",
            "admin/config.yml",
            200,
            is_json=False
        )
        
        if success:
            # Validate YAML syntax
            try:
                yaml_content = yaml.safe_load(response["content"])
                print("✅ YAML syntax is valid")
                
                # Check for duplicate editor keys
                if "collections" in yaml_content:
                    editors = []
                    for collection in yaml_content["collections"]:
                        if "fields" in collection:
                            for field in collection["fields"]:
                                if isinstance(field, dict) and "name" in field:
                                    editors.append(field["name"])
                    
                    # Check for duplicates within each collection
                    duplicates = set([x for x in editors if editors.count(x) > 1])
                    if duplicates:
                        print(f"❌ Found duplicate editor keys: {duplicates}")
                        success = False
                    else:
                        print("✅ No duplicate editor keys found")
                
                return success, {"content": yaml_content}
            except yaml.YAMLError as e:
                print(f"❌ Invalid YAML syntax: {str(e)}")
                return False, {"error": str(e)}
        
        return success, response

def main():
    # Get backend URL from environment
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                backend_url = line.strip().split('=')[1].strip('"')
                break
    
    # Extract the base URL without the protocol
    base_url_parts = backend_url.split('://')
    if len(base_url_parts) > 1:
        base_domain = base_url_parts[1]
    else:
        base_domain = base_url_parts[0]
    
    # For Netlify CMS tests, we need to use the frontend URL
    frontend_url = backend_url
    
    print(f"Testing backend API at: {backend_url}")
    print(f"Testing frontend at: {frontend_url}")
    
    # Setup tester
    backend_tester = NetlifyCMSAPITester(backend_url)
    frontend_tester = NetlifyCMSAPITester(frontend_url)
    
    # Run backend API tests
    print("\n=== Backend API Tests ===")
    api_root_success, api_root_response = backend_tester.test_api_root()
    if api_root_success:
        print(f"API Root Response: {api_root_response}")
    
    status_success, status_response = backend_tester.test_status_endpoint()
    if status_success:
        print(f"Status Endpoint Response: {status_response}")
    
    create_success, create_response = backend_tester.test_create_status()
    if create_success:
        print(f"Create Status Response: {create_response}")
    
    # Run Netlify CMS tests
    print("\n=== Netlify CMS Tests ===")
    admin_success, admin_response = frontend_tester.test_netlify_cms_admin_page()
    if admin_success:
        print("Netlify CMS Admin page loaded successfully")
        # Check if it contains the Netlify CMS script
        if "netlify-cms.js" in admin_response["content"]:
            print("✅ Netlify CMS script found in admin page")
        else:
            print("❌ Netlify CMS script not found in admin page")
            admin_success = False
    
    config_success, config_response = frontend_tester.test_netlify_cms_config()
    if config_success:
        print("Netlify CMS Config loaded and validated successfully")
    
    # Print results
    print("\n=== Test Results ===")
    print(f"Backend API Tests: {backend_tester.tests_passed}/{backend_tester.tests_run} passed")
    print(f"Netlify CMS Tests: {frontend_tester.tests_passed}/{frontend_tester.tests_run} passed")
    
    total_passed = backend_tester.tests_passed + frontend_tester.tests_passed
    total_run = backend_tester.tests_run + frontend_tester.tests_run
    print(f"\n📊 Total Tests: {total_passed}/{total_run} passed")
    
    return 0 if total_passed == total_run else 1

if __name__ == "__main__":
    sys.exit(main())
      