#!/usr/bin/env python3
"""
Test Plaid Credentials
Quick script to verify if your Plaid credentials are valid
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

client_id = os.getenv('PLAID_CLIENT_ID', '')
secret = os.getenv('PLAID_SECRET', '')
env = os.getenv('PLAID_ENV', '')

print("=" * 60)
print("  🔍 Plaid Credentials Check")
print("=" * 60)

print(f"\n📋 Current Configuration:")
print(f"   PLAID_CLIENT_ID: {client_id}")
print(f"   PLAID_SECRET: {secret}")
print(f"   PLAID_ENV: {env}")

print(f"\n📏 Credential Lengths:")
print(f"   CLIENT_ID length: {len(client_id)} characters")
print(f"   SECRET length: {len(secret)} characters")
print(f"   ENV length: {len(env)} characters")

print(f"\n✅ Validation:")

# Check if credentials exist
if not client_id:
    print("   ❌ PLAID_CLIENT_ID is missing!")
else:
    print(f"   ✅ PLAID_CLIENT_ID exists")

if not secret:
    print("   ❌ PLAID_SECRET is missing!")
else:
    print(f"   ✅ PLAID_SECRET exists")
    if len(secret) < 30:
        print(f"   ⚠️  SECRET seems too short (only {len(secret)} chars)")
    elif len(secret) == 30:
        print(f"   ⚠️  SECRET is 30 chars - might be incomplete")
    else:
        print(f"   ✅ SECRET length looks good ({len(secret)} chars)")

if not env:
    print("   ❌ PLAID_ENV is missing!")
else:
    print(f"   ✅ PLAID_ENV exists")

print("\n" + "=" * 60)

# Try to test with Plaid API
try:
    from plaid.api import plaid_api
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.products import Products
    from plaid.model.country_code import CountryCode
    from plaid import ApiClient, Configuration
    
    print("\n🔌 Testing Plaid API Connection...")
    
    configuration = Configuration(
        host=env,
        api_key={
            'clientId': client_id,
            'secret': secret,
        }
    )
    
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    
    # Try to create a link token
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id="test_user_123"
        ),
        client_name="Test App",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en"
    )
    
    response = client.link_token_create(request)
    
    print("   ✅ SUCCESS! Plaid API connection works!")
    print(f"   ✅ Link token created: {response['link_token'][:20]}...")
    print("\n🎉 Your Plaid credentials are VALID and working!")
    
except Exception as e:
    print(f"   ❌ FAILED! Error: {str(e)}")
    print("\n❌ Your Plaid credentials are INVALID or incomplete!")
    print("\n📝 Next Steps:")
    print("   1. Login to https://dashboard.plaid.com/")
    print("   2. Go to Team Settings → Keys")
    print("   3. Copy the COMPLETE sandbox secret")
    print("   4. Update backend/.env file")
    print("   5. Run this test again")

print("\n" + "=" * 60)
