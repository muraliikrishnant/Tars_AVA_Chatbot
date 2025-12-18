# Integration & Hosting Guide

## WordPress Integration

To add the Ava Chatbot to your WordPress site (`tarsgroup.co`), you have two main options:

### Option 1: Custom HTML/JS Snippet (Recommended for flexibility)
1.  **Build the Frontend**: Run `npm run build` in the `frontend` directory. This will create a `dist` folder with `index.html` and assets.
2.  **Host the Assets**: Upload the JS and CSS files from `dist/assets` to your WordPress media library or a CDN.
3.  **Add Snippet**: In your WordPress theme's `footer.php` or using a plugin like "Insert Headers and Footers", add the following script:

```html
<div id="root"></div>
<script type="module" src="https://your-site.com/path/to/assets/index.js"></script>
<link rel="stylesheet" href="https://your-site.com/path/to/assets/index.css">
```
*Note: You might need to adjust the React mounting point (`root` div) to avoid conflicts, or wrap the ChatWidget in a web component.*

### Option 2: Iframe
Host the frontend separately (e.g., Vercel, Netlify) and embed it via an iframe in a custom widget area.

## Free Backend Hosting

To host the FastAPI backend for free:

1.  **Render (Recommended)**:
    - Connect your GitHub repo.
    - Create a "Web Service".
    - Build Command: `pip install -r backend/requirements.txt`
    - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
    - Add Environment Variable: `GEMINI_API_KEY`.
    - Free tier spins down after inactivity (cold starts).

2.  **Railway / Fly.io**:
    - Similar setup, often have small free tiers or trial credits.

3.  **Google Cloud Run**:
    - Generous free tier, but requires containerization (Docker).

## Free Frontend Hosting
- **Vercel** or **Netlify**: Connect GitHub repo, set build command `npm run build` and output dir `dist`.
