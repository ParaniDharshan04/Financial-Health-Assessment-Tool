# Fix: Plaid Demo Mode Issue 🔧

## Problem
When clicking "Connect Bank Account", it shows "Using demo mode" instead of opening Plaid Link.

## Root Cause
Your Plaid credentials in `.env` file are incomplete or invalid:
```
PLAID_CLIENT_ID=697cec1ddf3d3500215dcff8  ✅ Looks OK
PLAID_SECRET=9446bfe19826bf7ad3a7a8f81d152f  ❌ INCOMPLETE!
```

Plaid secrets are typically **longer** (around 30-40 characters).

---

## Solution: Get Complete Plaid Credentials

### Step 1: Login to Plaid Dashboard
1. Go to: https://dashboard.plaid.com/
2. Login with your Plaid account
3. If you don't have an account, sign up (it's free for sandbox)

### Step 2: Get Your Credentials
1. Click on **"Team Settings"** (gear icon)
2. Go to **"Keys"** section
3. You'll see:
   - **client_id**: Copy this
   - **sandbox secret**: Copy this (NOT the development/production secret)

### Step 3: Update .env File
Open `backend/.env` and update:

```env
# Plaid Banking API
PLAID_CLIENT_ID=your_complete_client_id_here
PLAID_SECRET=your_complete_sandbox_secret_here
PLAID_ENV=https://sandbox.plaid.com
```

**Example (with fake credentials):**
```env
PLAID_CLIENT_ID=697cec1ddf3d3500215dcff8
PLAID_SECRET=9446bfe19826bf7ad3a7a8f81d152f1234567890abcdef
PLAID_ENV=https://sandbox.plaid.com
```

### Step 4: Restart Backend Server
```bash
# Stop current server (Ctrl+C)
cd backend
python check_and_start.py
```

### Step 5: Test Connection
1. Go to Banking page
2. Click "Connect Bank Account"
3. Should open Plaid Link modal (not demo mode!)
4. Select a test bank (e.g., "First Platypus Bank")
5. Use test credentials:
   - Username: `user_good`
   - Password: `pass_good`

---

## How to Get Plaid Account (If You Don't Have One)

### Option 1: Sign Up for Free Sandbox
1. Go to: https://dashboard.plaid.com/signup
2. Fill in:
   - Email
   - Company name
   - Password
3. Verify email
4. Complete onboarding
5. Get your sandbox credentials

### Option 2: Use Existing Account
If you already signed up:
1. Login to dashboard
2. Go to Keys section
3. Copy sandbox credentials

---

## Verify Credentials Are Correct

### Check 1: Length
- **client_id**: Should be 24 characters
- **secret**: Should be 30+ characters

### Check 2: Format
- No spaces
- No line breaks
- No quotes around values

### Check 3: Environment
- Use `sandbox` for testing
- Use `development` for real testing
- Use `production` for live (requires approval)

---

## Test Plaid Connection

### Method 1: Check Backend Logs
When you restart backend, you should see:
```
✅ Plaid configured - Environment: https://sandbox.plaid.com
```

If you see:
```
⚠️  Plaid not configured - missing CLIENT_ID or SECRET
```
Then credentials are still wrong.

### Method 2: Test API Directly
```bash
curl -X POST http://localhost:8000/api/banking/create-link-token \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

Should return:
```json
{
  "link_token": "link-sandbox-...",
  "is_demo": false
}
```

---

## Common Issues & Solutions

### Issue 1: "Invalid credentials"
**Solution:** 
- Make sure you're using **sandbox** secret (not development/production)
- Copy credentials again from dashboard
- Check for extra spaces or characters

### Issue 2: "API key not found"
**Solution:**
- Verify client_id is correct
- Ensure no typos
- Try regenerating keys in Plaid dashboard

### Issue 3: Still showing demo mode
**Solution:**
1. Check `.env` file has correct values
2. Restart backend server
3. Clear browser cache
4. Try in incognito mode

### Issue 4: "Rate limit exceeded"
**Solution:**
- Sandbox has rate limits
- Wait a few minutes
- Or upgrade to development environment

---

## Alternative: Use Demo Mode (For Now)

If you can't get Plaid credentials right now, demo mode still works:

### What Demo Mode Provides:
- ✅ Sample bank accounts
- ✅ Sample transactions
- ✅ All features work
- ✅ Good for testing UI/UX
- ❌ Not real bank data

### To Use Demo Mode:
1. Just click "Connect Bank Account"
2. It will show demo data automatically
3. You can test all features
4. Get real Plaid credentials later

---

## Production Checklist

Before going live:

- [ ] Get Plaid production credentials
- [ ] Update PLAID_ENV to production
- [ ] Complete Plaid verification process
- [ ] Set up webhook URL
- [ ] Test with real bank accounts
- [ ] Implement error handling
- [ ] Add logging and monitoring

---

## Quick Fix Summary

**Problem:** Incomplete PLAID_SECRET  
**Solution:** Get complete credentials from Plaid dashboard  
**Steps:**
1. Login to https://dashboard.plaid.com/
2. Go to Team Settings → Keys
3. Copy complete sandbox secret
4. Update backend/.env
5. Restart backend server
6. Test connection

**Time:** 5 minutes  
**Cost:** Free (sandbox)

---

## Need Help?

### Plaid Documentation:
- Getting Started: https://plaid.com/docs/quickstart/
- Sandbox Testing: https://plaid.com/docs/sandbox/
- API Reference: https://plaid.com/docs/api/

### Support:
- Plaid Support: support@plaid.com
- Plaid Community: https://community.plaid.com/

---

## Status Check

After fixing, you should see:

✅ Backend logs: "Plaid configured"  
✅ Click "Connect Bank Account" → Plaid Link opens  
✅ Can select test banks  
✅ Can connect accounts  
✅ No "demo mode" message

If you still see demo mode, credentials are still incorrect!
