# Vercel Environment Variable Setup

## Critical: Frontend API Configuration

Your frontend is already configured to use environment variables, but Vercel needs them set in the dashboard.

### Required Environment Variable

**Variable Name:** `VITE_API_URL`  
**Value:** `https://financial-health-assessment-tool-15e2.onrender.com`

### How to Set in Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Select your frontend project
3. Click **Settings** (top navigation)
4. Click **Environment Variables** (left sidebar)
5. Click **Add New**
6. Enter:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://financial-health-assessment-tool-15e2.onrender.com`
   - **Environments:** Check all boxes (Production, Preview, Development)
7. Click **Save**
8. Go to **Deployments** tab
9. Click the three dots (...) on your latest deployment
10. Click **Redeploy** to apply the new environment variable

### Why This is Needed

Your `frontend/src/config.js` uses:
```javascript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

- **Local development:** Uses `http://localhost:8000` (fallback)
- **Production (Vercel):** Uses `VITE_API_URL` from environment variables

Without setting `VITE_API_URL` in Vercel, your production frontend tries to call `localhost:8000`, which fails with `ERR_BLOCKED_BY_CLIENT`.

### Verification

After redeploying:
1. Open your Vercel site
2. Open browser DevTools (F12)
3. Go to Console tab
4. Try to register/login
5. Check Network tab - API calls should go to `https://financial-health-assessment-tool-15e2.onrender.com`

### Backend CORS Configuration

Make sure your backend (Render) allows requests from your Vercel domain. Check `backend/app/main.py` has your Vercel URL in CORS origins.
