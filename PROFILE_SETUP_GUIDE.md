# Profile Page Setup Guide

## Overview
A new Profile page has been added to the application where users can view and update their personal and company information.

## Features Added

### 1. Profile Page (`frontend/src/pages/Profile.jsx`)
- **Basic Information Section**
  - Email (read-only)
  - Phone number

- **Company Information Section**
  - Company name
  - Industry (dropdown with 10 options)
  - Company size (Micro/Small/Medium/Large)
  - Registration date
  - GSTIN (15 characters)
  - PAN (10 characters)
  - Annual revenue

- **Address Information Section**
  - Full address (textarea)
  - City
  - State
  - Pincode (6 digits)

### 2. Backend API Endpoints
- `GET /api/auth/profile` - Get current user profile
- `PUT /api/auth/profile` - Update user profile

### 3. Database Schema Updates
New columns added to `users` table:
- phone
- address
- city
- state
- pincode
- gstin
- pan
- registration_date
- company_size
- annual_revenue

### 4. UI Updates
- Profile icon added to Dashboard header (right side of logout button)
- Consistent design matching other pages
- Multi-language support (English, Hindi, Tamil)

## Setup Instructions

### Step 1: Database Migration
Run the migration script to add new columns to the users table:

```bash
cd backend
python update_user_profile_fields.py
```

### Step 2: Restart Backend Server
If the backend is running, restart it to load the new API endpoints:

```bash
# Stop the current server (Ctrl+C)
# Then restart
uvicorn app.main:app --reload
```

Or use the PowerShell script:
```powershell
.\restart_servers.ps1
```

### Step 3: Access Profile Page
1. Login to the application
2. Click the "Profile" button in the Dashboard header (next to Logout)
3. Update your profile information
4. Click "Save Changes"

## Navigation Flow
```
Dashboard → Profile Icon (Header) → Profile Page
Profile Page → Back Arrow or Cancel → Dashboard
```

## API Usage Examples

### Get Profile
```javascript
const token = localStorage.getItem('token')
const response = await axios.get('/api/auth/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

### Update Profile
```javascript
const token = localStorage.getItem('token')
const response = await axios.put('/api/auth/profile', {
  company_name: "My Company",
  phone: "+91 98765 43210",
  industry: "technology",
  // ... other fields
}, {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

## Validation Rules
- **Email**: Cannot be changed (read-only)
- **GSTIN**: Maximum 15 characters
- **PAN**: Maximum 10 characters, auto-uppercase
- **Pincode**: Maximum 6 characters
- **Phone**: Free format (supports international)

## Design Consistency
The Profile page follows the same design pattern as other pages:
- Glass-morphism cards (`metric-card` class)
- Neon gradient text for headings
- Consistent input styling (`input-glass` class)
- Responsive grid layout
- Icon-based section headers
- Smooth animations

## Multi-language Support
Translations added for:
- English: "Profile", "Manage your profile and company information"
- Hindi: "प्रोफ़ाइल", "अपनी प्रोफ़ाइल और कंपनी की जानकारी प्रबंधित करें"
- Tamil: "சுயவிவரம்", "உங்கள் சுயவிவரம் மற்றும் நிறுவன தகவலை நிர்வகிக்கவும்"

## Files Modified/Created

### Frontend
- ✅ `frontend/src/pages/Profile.jsx` (NEW)
- ✅ `frontend/src/App.jsx` (Updated - added route)
- ✅ `frontend/src/pages/Dashboard.jsx` (Updated - added profile button)
- ✅ `frontend/src/i18n.js` (Updated - added translations)

### Backend
- ✅ `backend/app/db/models.py` (Updated - added profile fields)
- ✅ `backend/app/schemas/user.py` (Updated - added UserUpdate schema)
- ✅ `backend/app/api/auth.py` (Updated - added profile endpoints)
- ✅ `backend/update_user_profile_fields.py` (NEW - migration script)

## Troubleshooting

### Profile button not showing
- Clear browser cache and reload
- Check if User icon is imported in Dashboard.jsx

### Profile data not saving
- Check backend logs for errors
- Verify database migration ran successfully
- Ensure .env file has correct DATABASE_URL

### Fields not appearing
- Run the migration script again
- Check database schema: `SELECT * FROM information_schema.columns WHERE table_name = 'users'`

## Future Enhancements
- Profile picture upload
- Password change functionality
- Two-factor authentication
- Email verification
- Company logo upload
- Document attachments (GST certificate, PAN card)
