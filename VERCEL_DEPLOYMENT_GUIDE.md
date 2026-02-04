# Vercel Deployment Guide - Frontend

## Environment Variables for Vercel

For your frontend deployment on Vercel, you typically don't need many environment variables since the API proxy is configured in `vite.config.js`. However, if you're deploying to production, you'll need to configure the backend API URL.

### Option 1: Using Environment Variables (Recommended for Production)

Add these environment variables in Vercel:

```
Key: VITE_API_URL
Value: https://your-backend-api-url.com
```

Example:
```
Key: VITE_API_URL
Value: https://finance-backend.herokuapp.com
```

Or if using Railway/Render:
```
Key: VITE_API_URL
Value: https://your-app.railway.app
```

### Option 2: No Environment Variables (Development/Testing)

If your backend is not deployed yet, you can leave the environment variables empty for now. The app will use relative URLs (`/api/*`) which work with the Vite proxy during development.

## Vercel Configuration

### 1. Root Directory
- **Root Directory**: `frontend`
- This tells Vercel where your frontend code is located

### 2. Build Settings
- **Framework Preset**: Vite
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3. Node.js Version
- **Node Version**: 18.x or higher (recommended)

## Step-by-Step Deployment

### 1. Connect Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the repository: `Financial-Health-Assessment-Tool`

### 2. Configure Project
```
Project Name: finance-health-app (or your preferred name)
Framework Preset: Vite
Root Directory: frontend
```

### 3. Environment Variables (Optional for now)
If you have a deployed backend, add:
```
VITE_API_URL = https://your-backend-url.com
```

If not deployed yet, skip this step.

### 4. Deploy
Click "Deploy" button

## After Deployment

### Update Frontend Code (if using VITE_API_URL)

If you added the `VITE_API_URL` environment variable, update your axios configuration:

**Create/Update: `frontend/src/config.js`**
```javascript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

**Update: `frontend/src/context/AuthContext.jsx`**
```javascript
import { API_URL } from '../config'

// In login function:
const response = await axios.post(`${API_URL}/api/auth/login`, { email, password })

// In register function:
const response = await axios.post(`${API_URL}/api/auth/register`, {
  email, password, company_name, industry
})
```

## Quick Setup (Copy-Paste for Vercel)

### For Development/Testing (No Backend Yet)
**Leave Environment Variables Empty**

### For Production (With Deployed Backend)
```
VITE_API_URL=https://your-backend-url.com
```

## Vercel Build Configuration File (Optional)

Create `vercel.json` in the root directory:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-url.com/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

## Common Issues & Solutions

### Issue 1: API Calls Failing
**Solution**: Make sure your backend URL is correct and includes the protocol (https://)

### Issue 2: CORS Errors
**Solution**: Configure CORS in your backend to allow requests from your Vercel domain:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: Build Fails
**Solution**: 
1. Check Node.js version (use 18.x or higher)
2. Ensure all dependencies are in `package.json`
3. Check build logs for specific errors

## Testing Your Deployment

After deployment, test these features:
1. ✅ Login page loads
2. ✅ Registration works (if backend is connected)
3. ✅ Dashboard displays
4. ✅ Navigation works
5. ✅ Profile page loads

## Backend Deployment

Your backend needs to be deployed separately. Recommended platforms:
- **Railway** (easiest for Python/FastAPI)
- **Render** (free tier available)
- **Heroku** (requires credit card)
- **DigitalOcean App Platform**

## Next Steps

1. **Deploy Frontend to Vercel** (current step)
2. **Deploy Backend** to Railway/Render/Heroku
3. **Update VITE_API_URL** in Vercel with backend URL
4. **Update CORS** in backend to allow Vercel domain
5. **Test the full application**

## Quick Reference

### Vercel Environment Variables Format
```
Key                 Value
VITE_API_URL       https://your-backend.railway.app
```

### No Environment Variables Needed If:
- Backend is not deployed yet
- Testing the frontend UI only
- Using mock data

You can deploy the frontend first and add the backend URL later!
