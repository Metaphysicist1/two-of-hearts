# 🚀 Valentine's Invitation Creator - FastAPI Backend

**Date:** February 12, 2026  
**Status:** ✅ PRODUCTION READY FOR RAILWAY.APP  
**Deadline:** February 14, 2026

---

## 📋 Project Overview

A romantic, full-stack web application for creating and sharing personalized Valentine's Day invitations.

### ✨ Features

✅ **Beautiful Frontend** (Jinja2 templates)

- Glassmorphism design
- Animated background with floating particles
- Responsive on all devices

✅ **Backend (FastAPI + SQLite)**

- Form submission → Save to database → Clean redirect
- Short invitation IDs (12 chars)
- Photo compression (canvas-free, uses Pillow)
- Base64 photo storage in DB

✅ **Sharing**

- Simple, shareable links: `/view/{invitation_id}`
- No URL parameters or sessionStorage hacks
- Works across devices, browsers, sessions
- Copy link button on viewer page

✅ **Database**

- SQLite file-based (no external DB needed)
- Auto-migrates on startup
- Stores: name, sender, message, theme, base64 photo

---

## 🏗️ Project Structure

```
valent-night/
├── main.py                      # FastAPI app, routes, database models
├── requirements.txt             # Python dependencies
├── Procfile                      # Railway deployment config
├── railway.toml                  # Railway settings
├── database.db                   # SQLite (auto-created)
└── templates/
    ├── index.html               # Creation form (Jinja2)
    ├── viewer.html              # Invitation display (Jinja2)
    └── error.html               # Error page (Jinja2)
```

---

## 🛠️ Setup & Local Testing

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. Run LocallyServe

```bash
python main.py
# or
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**

### 3. Test Flow

```
1. Go to http://localhost:8000/
2. Fill form (name, message, theme, optional photo)
3. Submit form
4. Auto-redirect to http://localhost:8000/view/{id}
5. Invitation displays with photo, theme styling, floating hearts
6. Click "Copy Link" → Link in clipboard
7. Share link with anyone → They see the same invitation
```

---

## 🗄️ Database Schema

### Invitations Table

```sql
CREATE TABLE invitations (
    id VARCHAR PRIMARY KEY,              -- short uuid (12 chars)
    recipient_name VARCHAR NOT NULL,      -- "Anna"
    sender_name VARCHAR,                  -- "John"
    message TEXT NOT NULL,                -- "Be my Valentine..."
    theme VARCHAR DEFAULT 'romantic',     -- one of: romantic/playful/elegant/minimalist
    photo_base64 TEXT                     -- "data:image/jpeg;base64,..." or NULL
);
```

---

## 🌐 API Routes

### GET `/`

- **Description:** Serve creation form
- **Response:** HTML form page (index.html)
- **Status:** 200

### POST `/create`

- **Description:** Create invitation and save to DB
- **Body:** multipart/form-data
  - `name` (required): recipient name
  - `sender` (optional): sender name
  - `message` (required): invitation message (max 500 chars)
  - `theme` (optional): `romantic|playful|elegant|minimalist`
  - `photo` (optional): image file

- **Response:** 303 Redirect to `/view/{id}`
- **Errors:**
  - 400: Photo too large (>5 MB)
  - 500: Database error

### GET `/view/{inv_id}`

- **Description:** Display invitation from database
- **Parameters:**
  - `inv_id` (required): 12-char invitation ID
- **Response:** HTML invitation page (viewer.html)
- **Errors:**
  - 404: Invitation not found

### GET `/health`

- **Description:** Health check (for deployment monitoring)
- **Response:** `{"status": "ok", "service": "valentines-invitation"}`

---

## 📸 Photo Handling

### Process

1. User uploads JPG/PNG/etc.
2. Check file size (error if >5 MB)
3. Open with PIL (Pillow)
4. Resize to max 800px width (proportional height)
5. Convert RGBA/LA/P to RGB
6. Compress to JPEG 70% quality
7. Encode to base64
8. Prefix with `data:image/jpeg;base64,`
9. Store in DB as TEXT
10. Display in viewer with `<img src="{photo_base64}">`

### File Sizes

- Original: 5 MB max
- After compression: ~200-400 KB base64
- DB storage: No issues (SQLite TEXT can handle MB)

---

## 🎨 Themes

### 1. Romantic 💕

- Pink gradient background
- Pink header text
- Gold floating hearts
- Default theme

### 2. Playful 🎉

- Gold dashed border
- Comic Sans font
- Vibrant colors
- Fun atmosphere

### 3. Elegant ✨

- Gold gradient
- Uppercase headers
- Playfair Display font
- Sophisticated

### 4. Minimalist 🤍

- White/light background
- Clean layout
- Subtle styling
- Simple elegance

---

## 🚀 Deploy to Railway.app

### Step 1: Prepare Code

```bash
# Git must be initialized
git init
git add .
git commit -m "Initial commit: FastAPI Valentine's Invitation"
git remote add origin https://github.com/USERNAME/valent-night.git
git branch -M main
git push -u origin main
```

### Step 2: Connect Railway

1. Go to [railway.app](https://railway.app)
2. Sign in / Sign up with GitHub
3. Click "New Project"
4. Select "GitHub repo"
5. Choose your repo: `valent-night`
6. Railway auto-detects FastAPI & Python

### Step 3: Configure (Optional)

- In Railway Dashboard → Settings
- Environment: Python 3.11+
- Start command: Pre-filled with Procfile

### Step 4: Deploy

- Click "Deploy"
- Wait 2-5 minutes
- Get live URL: `https://valent-night-production-xxxx.up.railway.app/`

### Step 5: Test Live

```bash
curl https://valent-night-production-xxxx.up.railway.app/health
# Should return: {"status":"ok","service":"valentines-invitation"}
```

---

## 📊 Performance & Limits

| Aspect            | Limit       | Notes                 |
| ----------------- | ----------- | --------------------- |
| Photo size        | 5 MB        | Compressed to ~300 KB |
| Message length    | 500 chars   | UI limit              |
| Invitation ID     | 12 chars    | Short & shareable     |
| Database          | SQLite file | Unlimited (on disk)   |
| Railway free tier | 5 GB disk   | Plenty for this app   |
| Concurrent users  | Unlimited\* | \*Railway scales auto |

---

## 🔒 Security & Privacy

✅ **No User Tracking**

- No cookies, no localStorage tracking
- No analytics
- Anonymous creation

✅ **Data Security**

- SQLite file-based (not exposed)
- Railway provides HTTPS by default
- No user auth needed (public by design)

✅ **Photo Handling**

- Stored as base64 in DB
- No external image storage
- All data in single SQLite file

---

## 🛠️ Troubleshooting

### Local Testing Issues

**"Module not found: fastapi"**

```bash
# Ensure venv activated
source venv/bin/activate
pip install -r requirements.txt
```

**"Port already in use"**

```bash
# Use different port
uvicorn main:app --port 8001
```

**"Photo not showing on viewer"**

- Check browser console for errors
- Verify photo_base64 starts with `data:image/`
- Try different image format

### Railway Deployment Issues

**"Build failed"**

- Check that `requirements.txt` exists
- Verify Python version (3.9+)
- Check Procfile syntax

**"App crashes after deploy"**

- Check Railway logs: `railway logs`
- Ensure PORT env var is used (already in main.py)
- Verify templates/ directory exists

**"Database locked"**

- SQLite concurrent write limit
- Railway scales each instance separately
- Each instance gets own database.db

---

## 📱 Testing Checklist

### Local

- [ ] Form loads at http://localhost:8000/
- [ ] Fill form and submit
- [ ] Redirect to /view/{id}
- [ ] Invitation shows with photo, message, theme
- [ ] Copy link button works
- [ ] Share link in new tab/incognito → same invitation

### Live (Railway)

- [ ] Health check passes: `/health`
- [ ] Form accessible
- [ ] Form submission works
- [ ] Invitation displays correctly
- [ ] Photo loads in invitation
- [ ] Theme styling applied
- [ ] Floating hearts animation works
- [ ] Copy link works
- [ ] Shared links work for friends

---

## 🚨 Production Checklist

Before launching to friends:

- [ ] Code committed & pushed to GitHub
- [ ] Railway deployment successful
- [ ] Health check passes
- [ ] All routes tested
- [ ] Photo upload works
- [ ] All themes display correctly
- [ ] Mobile responsive (tested on phone)
- [ ] Shared links work in fresh browser
- [ ] Error handling works (404, etc.)
- [ ] README documented

---

## 📞 Common Questions

**Q: Can I change colors/fonts?**  
A: Edit CSS in `templates/index.html` and `templates/viewer.html`.

**Q: How long do invitations last?**  
A: Forever! Stored in SQLite, no expiration.

**Q: Can I add more themes?**  
A: Yes! Add CSS class in template, update theme selector form.

**Q: How many invitations can I store?**  
A: Millions (SQLite scales to GB+). Railway free tier: 5 GB disk.

**Q: Can I export data?**  
A: Yes! Database is just `database.db` file. Download from Railway.

---

## 🎉 Launch Day!

**Friday, February 14, 2026**

### Share with friends:

```
"I built a Valentine's invitation maker! 💝

Create custom invitations with photos, messages, and beautiful themes.

No sign-up needed. Instant shareable links.

Try it: https://valent-night-production-xxxx.up.railway.app/"
```

---

## 📝 License

Free to use and modify. No restrictions.

---

**Good luck with your launch! 💕**
