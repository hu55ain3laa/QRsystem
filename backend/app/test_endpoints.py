import requests
import json
from datetime import datetime
import time
import sys

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

# Admin credentials from .env file
admin_email = "admin@example.com"
admin_password = "adminpassword123"

# Test data for creation
test_apartment = {
    "building": 99,
    "floor": 9,
    "apt_no": 999,
    "user_id": 1,
    "area": 150,
    "meter_price": 2000,
    "full_price": 300000
}

test_payment_type = {
    "name": "Test Payment Type"
}

test_history_type = {
    "name": "Test History Type"
}

test_client = {
    "name": "Test Client",
    "id_no": 12345678,
    "issue_date": datetime.now().isoformat(),
    "m": "Test M",
    "z": "Test Z",
    "d": "Test D",
    "phone_number": "+201123456789",
    "job_title": "Test Job",
    "alt_name": "Alt Test",
    "alt_kinship": "Sibling",
    "alt_phone": "+201198765432",
    "alt_m": 1,
    "alt_z": 2,
    "alt_d": 3,
    "apt_id": 1  # Will be replaced with created apartment ID
}

test_payment = {
    "date_of_payment": datetime.now().isoformat(),
    "payment_type_id": 1,  # Will be replaced with created payment type ID
    "amount": 5000,
    "client_id": 1  # Will be replaced with created client ID
}

test_history_entry = {
    "type_id": 1,  # Will be replaced with created history type ID
    "datetime": datetime.now().isoformat()
}

created_ids = {
    "apartment": None,
    "client": None,
    "payment_type": None,
    "payment": None,
    "history_type": None,
    "history": None
}


def login():
    """Login and get access token"""
    print("\n==== Testing Authentication ====")
    url = f"{BASE_URL}/login/access-token"
    data = {
        "username": admin_email,
        "password": admin_password
    }
    
    response = requests.post(url, data=data)
    print(f"Login status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        sys.exit(1)
        
    token_data = response.json()
    return token_data["access_token"]


def test_apartments(headers):
    """Test CRUD operations for apartments"""
    print("\n==== Testing Apartments ====")
    
    # Create apartment
    url = f"{BASE_URL}/apartments/"
    response = requests.post(url, json=test_apartment, headers=headers)
    print(f"Create apartment: {response.status_code}")
    if response.status_code == 200:
        apartment = response.json()
        created_ids["apartment"] = apartment["id"]
        print(f"Created apartment with ID: {created_ids['apartment']}")
    else:
        print(f"Failed to create apartment: {response.text}")
    
    # Get all apartments
    response = requests.get(url, headers=headers)
    print(f"Get all apartments: {response.status_code}")
    
    # Get specific apartment
    if created_ids["apartment"]:
        response = requests.get(f"{url}{created_ids['apartment']}", headers=headers)
        print(f"Get specific apartment: {response.status_code}")
    
    # Update apartment
    if created_ids["apartment"]:
        update_data = {"building": 88, "floor": 8}
        response = requests.put(f"{url}{created_ids['apartment']}", json=update_data, headers=headers)
        print(f"Update apartment: {response.status_code}")
    
    # We'll delete at the end


def test_payment_types(headers):
    """Test CRUD operations for payment types"""
    print("\n==== Testing Payment Types ====")
    
    # Create payment type
    url = f"{BASE_URL}/payment-types/"
    response = requests.post(url, json=test_payment_type, headers=headers)
    print(f"Create payment type: {response.status_code}")
    if response.status_code == 200:
        payment_type = response.json()
        created_ids["payment_type"] = payment_type["id"]
        print(f"Created payment type with ID: {created_ids['payment_type']}")
    else:
        print(f"Failed to create payment type: {response.text}")
    
    # Get all payment types
    response = requests.get(url, headers=headers)
    print(f"Get all payment types: {response.status_code}")
    
    # Get specific payment type
    if created_ids["payment_type"]:
        response = requests.get(f"{url}{created_ids['payment_type']}", headers=headers)
        print(f"Get specific payment type: {response.status_code}")
    
    # Update payment type
    if created_ids["payment_type"]:
        update_data = {"name": "Updated Test Payment Type"}
        response = requests.put(f"{url}{created_ids['payment_type']}", json=update_data, headers=headers)
        print(f"Update payment type: {response.status_code}")
    
    # We'll delete at the end


def test_history_types(headers):
    """Test CRUD operations for history types"""
    print("\n==== Testing History Types ====")
    
    # Create history type
    url = f"{BASE_URL}/history-types"
    response = requests.post(url, json=test_history_type, headers=headers)
    print(f"Create history type: {response.status_code}")
    if response.status_code == 200:
        history_type = response.json()
        created_ids["history_type"] = history_type["id"]
        print(f"Created history type with ID: {created_ids['history_type']}")
    else:
        print(f"Failed to create history type: {response.text}")
    
    # Get all history types
    response = requests.get(url, headers=headers)
    print(f"Get all history types: {response.status_code}")
    
    # Get specific history type
    if created_ids["history_type"]:
        response = requests.get(f"{url}/{created_ids['history_type']}", headers=headers)
        print(f"Get specific history type: {response.status_code}")
    
    # Update history type
    if created_ids["history_type"]:
        update_data = {"name": "Updated Test History Type"}
        response = requests.put(f"{url}/{created_ids['history_type']}", json=update_data, headers=headers)
        print(f"Update history type: {response.status_code}")
    
    # We'll delete at the end


def test_clients(headers):
    """Test CRUD operations for clients"""
    print("\n==== Testing Clients ====")
    
    # Update client data with created apartment ID
    if created_ids["apartment"]:
        test_client["apt_id"] = created_ids["apartment"]
    
    # Create client
    url = f"{BASE_URL}/clients/"
    response = requests.post(url, json=test_client, headers=headers)
    print(f"Create client: {response.status_code}")
    if response.status_code == 200:
        client = response.json()
        created_ids["client"] = client["id"]
        print(f"Created client with ID: {created_ids['client']}")
    else:
        print(f"Failed to create client: {response.text}")
    
    # Get all clients
    response = requests.get(url, headers=headers)
    print(f"Get all clients: {response.status_code}")
    
    # Get specific client
    if created_ids["client"]:
        response = requests.get(f"{url}{created_ids['client']}", headers=headers)
        print(f"Get specific client: {response.status_code}")
    
    # Get clients by apartment
    if created_ids["apartment"]:
        response = requests.get(f"{url}by-apartment/{created_ids['apartment']}", headers=headers)
        print(f"Get clients by apartment: {response.status_code}")
    
    # Update client
    if created_ids["client"]:
        update_data = {"name": "Updated Test Client", "job_title": "Updated Job"}
        response = requests.put(f"{url}{created_ids['client']}", json=update_data, headers=headers)
        print(f"Update client: {response.status_code}")
    
    # We'll delete at the end


def test_payments(headers):
    """Test CRUD operations for payments"""
    print("\n==== Testing Payments ====")
    
    # Update payment data with created client and payment type IDs
    if created_ids["client"] and created_ids["payment_type"]:
        test_payment["client_id"] = created_ids["client"]
        test_payment["payment_type_id"] = created_ids["payment_type"]
    
    # Create payment
    url = f"{BASE_URL}/payments/"
    response = requests.post(url, json=test_payment, headers=headers)
    print(f"Create payment: {response.status_code}")
    if response.status_code == 200:
        payment = response.json()
        created_ids["payment"] = payment["id"]
        print(f"Created payment with ID: {created_ids['payment']}")
    else:
        print(f"Failed to create payment: {response.text}")
    
    # Get all payments
    response = requests.get(url, headers=headers)
    print(f"Get all payments: {response.status_code}")
    
    # Get specific payment
    if created_ids["payment"]:
        response = requests.get(f"{url}{created_ids['payment']}", headers=headers)
        print(f"Get specific payment: {response.status_code}")
    
    # Get payments by client
    if created_ids["client"]:
        response = requests.get(f"{url}by-client/{created_ids['client']}", headers=headers)
        print(f"Get payments by client: {response.status_code}")
    
    # Update payment
    if created_ids["payment"]:
        update_data = {"amount": 6000}
        response = requests.put(f"{url}{created_ids['payment']}", json=update_data, headers=headers)
        print(f"Update payment: {response.status_code}")
    
    # We'll delete at the end


def test_history_entries(headers):
    """Test CRUD operations for history"""
    print("\n==== Testing History ====")
    
    # Update history data with created history type ID
    if created_ids["history_type"]:
        test_history_entry["type_id"] = created_ids["history_type"]
    
    # Create history
    url = f"{BASE_URL}/history"
    response = requests.post(url, json=test_history_entry, headers=headers)
    print(f"Create history: {response.status_code}")
    if response.status_code == 200:
        history = response.json()
        created_ids["history"] = history["id"]
        print(f"Created history with ID: {created_ids['history']}")
    else:
        print(f"Failed to create history: {response.text}")
    
    # Get all history entries
    response = requests.get(url, headers=headers)
    print(f"Get all history entries: {response.status_code}")
    
    # Get specific history entry
    if created_ids["history"]:
        response = requests.get(f"{url}/{created_ids['history']}", headers=headers)
        print(f"Get specific history entry: {response.status_code}")
    
    # Get history entries by type
    if created_ids["history_type"]:
        response = requests.get(f"{url}/by-type/{created_ids['history_type']}", headers=headers)
        print(f"Get history entries by type: {response.status_code}")
    
    # Update history entry
    if created_ids["history"]:
        update_data = {"datetime": datetime.now().isoformat()}
        response = requests.put(f"{url}/{created_ids['history']}", json=update_data, headers=headers)
        print(f"Update history entry: {response.status_code}")
    
    # We'll delete at the end


def delete_created_entities(headers):
    """Delete all created test entities"""
    print("\n==== Cleaning Up ====")
    
    # Delete in reverse order of creation
    
    # Delete history
    if created_ids["history"]:
        response = requests.delete(f"{BASE_URL}/history/{created_ids['history']}", headers=headers)
        print(f"Delete history entry: {response.status_code}")
    
    # Delete history type
    if created_ids["history_type"]:
        response = requests.delete(f"{BASE_URL}/history-types/{created_ids['history_type']}", headers=headers)
        print(f"Delete history type: {response.status_code}")
    
    # Delete payment
    if created_ids["payment"]:
        response = requests.delete(f"{BASE_URL}/payments/{created_ids['payment']}", headers=headers)
        print(f"Delete payment: {response.status_code}")
    
    # Delete payment type
    if created_ids["payment_type"]:
        response = requests.delete(f"{BASE_URL}/payment-types/{created_ids['payment_type']}", headers=headers)
        print(f"Delete payment type: {response.status_code}")
    
    # Delete client
    if created_ids["client"]:
        response = requests.delete(f"{BASE_URL}/clients/{created_ids['client']}", headers=headers)
        print(f"Delete client: {response.status_code}")
    
    # Delete apartment
    if created_ids["apartment"]:
        response = requests.delete(f"{BASE_URL}/apartments/{created_ids['apartment']}", headers=headers)
        print(f"Delete apartment: {response.status_code}")


def test_unauthorized_access():
    """Test that unauthorized access is properly rejected"""
    print("\n==== Testing Unauthorized Access ====")
    
    # Try to access apartments without authentication
    url = f"{BASE_URL}/apartments/"
    response = requests.get(url)
    print(f"Unauthorized access to apartments: {response.status_code}")
    if response.status_code in [401, 403]:
        print("Unauthorized access properly rejected")
    else:
        print("WARNING: Endpoint does not properly enforce authentication")


def main():
    """Run all test functions"""
    print("=== Starting API Endpoint Tests ===")
    print(f"Using base URL: {BASE_URL}")
    
    # First test unauthorized access
    test_unauthorized_access()
    
    # Now login and get token
    token = login()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test each model
    test_apartments(headers)
    test_payment_types(headers)
    test_history_types(headers)
    test_clients(headers)
    test_payments(headers)
    test_history_entries(headers)
    
    # Clean up
    delete_created_entities(headers)
    
    print("\n=== API Endpoint Tests Completed ===")


if __name__ == "__main__":
    main() 