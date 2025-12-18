# 🚀 Quick Deployment Guide - Ava Chatbot

Get your chatbot live in 15 minutes!

## What You Need

1. **GitHub Account** - Already have your repo set up ✅
2. **Gemini API Key** - From Google AI Studio (https://aistudio.google.com)
3. **Render Account** - For backend (https://render.com)
4. **Vercel Account** - For frontend (https://vercel.com)

---

## 🎯 Quick Start (TL;DR)

### Backend (Render) - 5 minutes

1. Go to https://render.com → Sign up with GitHub
2. Click "New Web Service" → Select your repo
3. **Build Command:** `pip install -r backend/requirements.txt`
4. **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app`
5. Add environment variable: `GEMINI_API_KEY=your_key_here`
6. Deploy → Copy your backend URL (e.g., `https://ava-backend.onrender.com`)

### Frontend (Vercel) - 5 minutes

1. Go to https://vercel.com → Sign up with GitHub
2. Click "Import Project" → Select your repo
3. **Root Directory:** `frontend`
4. **Build Command:** `npm run build`
5. **Output:** `dist`
6. Add Environment Variable:
   - **Name:** `VITE_API_URL`
   - **Value:** Your backend URL from above
7. Deploy → Copy your frontend URL (e.g., `https://ava-chatbot.vercel.app`)

### WordPress Integration - 5 minutes

Add to your WordPress footer (theme or custom HTML widget):

```html
<div id="root"></div>
<script type="module" src="https://YOUR_VERCEL_URL/dist/index.js"></script>
<link rel="stylesheet" href="https://YOUR_VERCEL_URL/dist/index.css">
```

---

## 📊 Expected URLs

After deployment, you'll have:

- **Backend API:** `https://ava-backend.onrender.com/`
  - Test it: Visit `https://ava-backend.onrender.com/`
  
- **Frontend:** `https://ava-chatbot.vercel.app/`
  - Live demo
  
- **WordPress Integration:** `https://tarsgroup.co/`
  - Add chatbot widget here

---

## ✅ Testing Checklist

After deployment:

- [ ] Backend responds to API calls
  ```bash
  curl https://your-backend-url/
  ```

- [ ] Frontend loads without CORS errors
  - Open browser DevTools → Console
  
- [ ] Chat sends/receives messages
  - Type a message in the chat widget
  - Verify response from Gemini API

- [ ] WordPress integration works
  - Chatbot appears on your site
  - Can send messages

---

## 🔑 Environment Variables

### Backend (Set in Render)
```
GEMINI_API_KEY=AIzaSy...  # Your actual API key
```

### Frontend (Set in Vercel)
```
VITE_API_URL=https://ava-backend.onrender.com
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to backend" | Verify VITE_API_URL in Vercel settings |
| "API key error" | Confirm GEMINI_API_KEY is set in Render |
| "CORS errors" | Backend is configured, check frontend URL |
| "Chatbot won't load on WordPress" | Update script URL to your Vercel domain |
| "Cold start delays" | Normal on Render free tier (first request takes 30s) |

---

## 📱 For Production Traffic

The free tier should handle moderate traffic. For more:

- **Upgrade Render** to paid tier ($7+/month)
- **Add caching** with Cloudflare
- **Scale backend** to multiple instances

---

## 🎓 Detailed Guide

For step-by-step instructions with screenshots, see:
- **Full Deployment Guide:** `DEPLOYMENT.md`
- **Integration Guide:** `INTEGRATION.md`
- **README:** `README.md`

---

## 🎉 You're Done!

Your Ava chatbot is now live! 

**Next steps:**
1. Monitor your deployment logs
2. Gather user feedback
3. Iterate and improve

---

**Need help?** Check the logs:
- Render: Dashboard → Service → Logs
- Vercel: Deployments → View Logs
