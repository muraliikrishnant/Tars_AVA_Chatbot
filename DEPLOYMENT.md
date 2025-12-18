# Deployment Guide for Ava Chatbot

This guide will help you deploy both the frontend and backend to production.

## 📋 Table of Contents
1. [Backend Deployment (FastAPI)](#backend-deployment)
2. [Frontend Deployment (React)](#frontend-deployment)
3. [WordPress Integration](#wordpress-integration)
4. [Environment Variables](#environment-variables)

---

## Backend Deployment

### Option 1: Render (Recommended - Easiest)

**Why Render?**
- Free tier with automatic deployments
- GitHub integration (auto-deploy on push)
- Easy environment variable management
- Good uptime for hobby projects

**Steps:**

1. **Connect GitHub Repository**
   - Go to https://render.com
   - Sign up with GitHub
   - Connect your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Select your `Tars_AVA_Chatbot` repository
   - Choose the repository

3. **Configure Service**
   - **Name**: `ava-chatbot-backend` (or any name)
   - **Region**: Choose closest to your users
   - **Runtime**: Python 3
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app
     ```

4. **Add Environment Variables**
   - In the Render dashboard, go to Environment
   - Add: `GEMINI_API_KEY` = `your_actual_api_key`
   - Save

5. **Deploy**
   - Click "Deploy Service"
   - Wait 2-3 minutes for deployment
   - Get your backend URL (e.g., `https://ava-chatbot-backend.onrender.com`)

### Option 2: Railway.app (Free Credits + Easy)

**Steps:**

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Start a New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app`
6. Add `GEMINI_API_KEY` in Variables
7. Deploy

**Backend URL** will be provided after deployment (e.g., `https://your-service.railway.app`)

### Option 3: Google Cloud Run (Generous Free Tier)

**Steps:**

1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable Cloud Run and Container Registry APIs
4. Deploy using Docker:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/ava-chatbot
   gcloud run deploy ava-chatbot \
     --image gcr.io/YOUR-PROJECT-ID/ava-chatbot \
     --platform managed \
     --region us-central1 \
     --set-env-vars GEMINI_API_KEY=your_api_key \
     --allow-unauthenticated
   ```

---

## Frontend Deployment

### Option 1: Vercel (Recommended for React)

**Why Vercel?**
- Optimized for React/Vite
- Lightning fast CDN
- Free tier is generous
- Easy GitHub integration
- 1-click deployment

**Steps:**

1. **Build the Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Push to GitHub**
   - Ensure your code is pushed to your repository

3. **Deploy on Vercel**
   - Go to https://vercel.com
   - Click "Import Project"
   - Select your GitHub repository
   - Configure:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

4. **Add Environment Variables** (if needed)
   - Add `VITE_API_URL` = your backend URL (e.g., `https://ava-chatbot-backend.onrender.com`)
   - This frontend doesn't need env vars, but good for future flexibility

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your frontend URL (e.g., `https://your-project.vercel.app`)

### Option 2: Netlify (Also Great)

**Steps:**

1. Go to https://netlify.com
2. Click "Import an existing project"
3. Select GitHub and your repository
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Deploy

**Frontend URL** (e.g., `https://your-project.netlify.app`)

---

## WordPress Integration

Now integrate the chatbot into your WordPress site at `https://tarsgroup.co/`

### Method 1: Custom Plugin (Recommended)

1. **Create Plugin File**
   - Create: `/wp-content/plugins/ava-chatbot/ava-chatbot.php`
   ```php
   <?php
   /*
   Plugin Name: Ava Chatbot
   Plugin URI: https://tarsgroup.co
   Description: Ava AI Chatbot for Tars Group
   Version: 1.0.0
   Author: Tars Group
   */

   if (!defined('ABSPATH')) {
       exit;
   }

   function ava_chatbot_enqueue_assets() {
       // Frontend app bundle
       wp_enqueue_script(
           'ava-chatbot-app',
           'https://your-vercel-url.vercel.app/dist/index.js',
           [],
           '1.0.0',
           true
       );
       
       wp_enqueue_style(
           'ava-chatbot-style',
           'https://your-vercel-url.vercel.app/dist/index.css',
           [],
           '1.0.0'
       );
   }
   add_action('wp_enqueue_scripts', 'ava_chatbot_enqueue_assets');

   function ava_chatbot_display() {
       echo '<div id="root"></div>';
   }
   add_shortcode('ava_chatbot', 'ava_chatbot_display');
   ?>
   ```

2. **Update Backend URL in Frontend**
   - Update [frontend/src/App.jsx](frontend/src/App.jsx) to use your backend URL:
   ```javascript
   const API_URL = "https://your-backend-url.onrender.com";
   ```

3. **Add to WordPress**
   - Use shortcode `[ava_chatbot]` anywhere on your site
   - Or add PHP code to your theme

### Method 2: Simple HTML/JS Embed (Easiest)

Add this to your WordPress footer or a custom HTML widget:

```html
<div id="root"></div>
<script type="module" src="https://your-vercel-url.vercel.app/dist/index.js"></script>
<link rel="stylesheet" href="https://your-vercel-url.vercel.app/dist/index.css">
```

---

## Environment Variables Setup

### Backend Environment Variables

**On Render/Railway/Cloud Run:**
- `GEMINI_API_KEY`: Your Google Gemini API key
- `PYTHONUNBUFFERED`: `true` (for better logging)

### Frontend Environment Variables

Update [frontend/vite.config.js](frontend/vite.config.js) or create a `.env` file:

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

Then in your React code (e.g., [frontend/src/App.jsx](frontend/src/App.jsx)):

```javascript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

---

## Deployment Checklist

- [ ] Backend deployed to Render/Railway/Cloud Run
  - URL: ____________________
  - GEMINI_API_KEY set in environment

- [ ] Frontend deployed to Vercel/Netlify
  - URL: ____________________
  - API_URL points to backend

- [ ] CORS enabled on backend (already done in `main.py`)

- [ ] WordPress integration tested
  - [ ] Shortcode added to page
  - [ ] Chat widget loads
  - [ ] API calls work

- [ ] Custom domain (optional)
  - [ ] Frontend connected to custom domain
  - [ ] Backend uses custom subdomain

---

## Monitoring & Updates

### Check Deployment Status
- **Render**: Dashboard → Your Service → Logs
- **Railway**: Dashboard → Deployments → View Logs
- **Vercel**: Deployments tab

### Update Code
After pushing changes to GitHub:
1. Render/Railway/Netlify auto-deploy (30 seconds - 2 min)
2. No manual action needed

### Scale Backend
- Render free tier: 0.5 CPU, 512 MB RAM
- For production traffic, upgrade to paid tier

---

## Troubleshooting

### "CORS errors" in Console
- ✅ Backend CORS is configured
- Check backend URL is correct in frontend

### "API not responding"
- Check backend deployment logs
- Verify GEMINI_API_KEY is set
- Verify backend URL is accessible

### "Frontend won't load"
- Verify Vercel build was successful
- Check build command in Vercel settings
- Clear browser cache

### "Chat not working"
- Verify backend is responding: `curl https://your-backend-url/`
- Check browser console for errors
- Verify API_URL in frontend matches deployed backend

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update backend URL in frontend code
4. ✅ Test chatbot on deployed versions
5. ✅ Integrate with WordPress
6. ✅ Go live! 🚀

For questions, check the main [README.md](../README.md) or [INTEGRATION.md](../INTEGRATION.md).
