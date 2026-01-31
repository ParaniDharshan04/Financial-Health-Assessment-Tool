"""
Test Plaid API connection and credentials
Run this to diagnose Plaid configuration issues
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 50)
print("PLAID CONNECTION TEST")
print("=" * 50)
print()

# Check environment variables
print("1. Checking environment variables...")
client_id = os.getenv('PLAID_CLIENT_ID', '')
secret = os.getenv('PLAID_SECRET', '')
env = os.getenv('PLAID_ENV', 'https://sandbox.plaid.com')

print(f"   PLAID_CLIENT_ID: {'✓ Set' if client_id else '✗ Missing'} ({client_id[:10]}... if set)")
print(f"   PLAID_SECRET: {'✓ Set' if secret else '✗ Missing'} ({secret[:10]}... if set)")
print(f"   PLAID_ENV: {env}")
print()

if not client_id or not secret:
    print("❌ ERROR: Plaid credentials not configured!")
    print("   Please add to backend/.env:")
    print("   PLAID_CLIENT_ID=your_client_id")
    print("   PLAID_SECRET=your_secret")
    print("   PLAID_ENV=https://sandbox.plaid.com")
    exit(1)

# Try importing Plaid
print("2. Checking Plaid SDK installation...")
try:
    import plaid
    from plaid.api import plaid_api
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.products import Products
    from plaid.model.country_code import CountryCode
    from plaid import ApiClient, Configuration
    print("   ✓ Plaid SDK imported successfully")
    print(f"   Plaid version: {plaid.__version__ if hasattr(plaid, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"   ✗ Failed to import Plaid SDK: {e}")
    print("   Run: pip install plaid-python")
    exit(1)
print()

# Try creating Plaid client
print("3. Creating Plaid API client...")
try:
    configuration = Configuration(
        host=env,
        api_key={
            'clientId': client_id,
            'secret': secret,
        }
    )
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    print("   ✓ Plaid client created successfully")
except Exception as e:
    print(f"   ✗ Failed to create client: {e}")
    exit(1)
print()

# Try creating link token
print("4. Testing link token creation...")
try:
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id="test_user_123"
        ),
        client_name="SME Financial Platform Test",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en"
    )
    
    response = client.link_token_create(request)
    link_token = response['link_token']
    
    print("   ✓ Link token created successfully!")
    print(f"   Link token: {link_token[:20]}...")
    print(f"   Expiration: {response.get('expiration', 'N/A')}")
    print()
    print("=" * 50)
    print("✅ SUCCESS! Plaid is configured correctly!")
    print("=" * 50)
    
except Exception as e:
    print(f"   ✗ Failed to create link token")
    print(f"   Error: {str(e)}")
    print()
    print("=" * 50)
    print("❌ FAILED! Plaid configuration issue")
    print("=" * 50)
    print()
    print("Possible causes:")
    print("1. Invalid credentials - Check your Plaid dashboard")
    print("2. Incorrect environment - Should be 'https://sandbox.plaid.com' for testing")
    print("3. API version mismatch - Try: pip install --upgrade plaid-python")
    print("4. Network issue - Check internet connection")
    print()
    print("Full error details:")
    print(str(e))
    exit(1)
