import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Plaid credentials
client_id = os.getenv('PLAID_CLIENT_ID', '').strip()
secret = os.getenv('PLAID_SECRET', '').strip()
env = os.getenv('PLAID_ENV', 'https://sandbox.plaid.com').strip()

print("=" * 60)
print("PLAID CONFIGURATION TEST")
print("=" * 60)
print(f"Client ID: {client_id[:10]}... (length: {len(client_id)})")
print(f"Secret: {secret[:10]}... (length: {len(secret)})")
print(f"Environment: {env}")
print(f"Is Configured: {bool(client_id and secret and len(client_id) > 10)}")
print("=" * 60)

# Try to import and configure Plaid
try:
    from plaid.api import plaid_api
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.products import Products
    from plaid.model.country_code import CountryCode
    from plaid import ApiClient, Configuration
    
    print("\n✅ Plaid library imported successfully")
    
    # Configure Plaid client
    configuration = Configuration(
        host=env,
        api_key={
            'clientId': client_id,
            'secret': secret,
        }
    )
    
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    
    print("✅ Plaid client configured successfully")
    
    # Try to create a test link token
    print("\n🔄 Testing link token creation...")
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
    print(f"✅ Link token created successfully!")
    print(f"   Token: {response['link_token'][:20]}...")
    print(f"   Expiration: {response['expiration']}")
    print("\n" + "=" * 60)
    print("✅ PLAID IS WORKING CORRECTLY!")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n❌ Error importing Plaid library: {e}")
    print("   Run: pip install plaid-python")
    
except Exception as e:
    print(f"\n❌ Error testing Plaid connection: {e}")
    print(f"   Error type: {type(e).__name__}")
    print("\n" + "=" * 60)
    print("❌ PLAID CONNECTION FAILED")
    print("=" * 60)
    print("\nPossible issues:")
    print("1. Invalid credentials - check PLAID_CLIENT_ID and PLAID_SECRET")
    print("2. Network connectivity issue")
    print("3. Plaid sandbox environment issue")
    print("4. Credentials might be for production, not sandbox")
