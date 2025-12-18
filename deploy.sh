#!/bin/bash

# Ava Chatbot Deployment Script
# This script helps you quickly deploy to Render and Vercel

echo "========================================="
echo "Ava Chatbot - Deployment Helper"
echo "========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run this from the project root."
    exit 1
fi

echo "📦 Preparing for deployment..."
echo ""

# Step 1: Ensure code is committed
echo "Step 1: Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Commit them first:"
    echo "   git add ."
    echo "   git commit -m 'Your message'"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Git status good"
echo ""

# Step 2: Prepare frontend build
echo "Step 2: Building frontend..."
cd frontend
npm run build
if [ $? -eq 0 ]; then
    echo "✅ Frontend built successfully"
else
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..
echo ""

# Step 3: Show deployment instructions
echo "Step 3: Deployment Instructions"
echo "================================"
echo ""
echo "🚀 BACKEND DEPLOYMENT (FastAPI):"
echo ""
echo "Option A - Render (Recommended):"
echo "1. Go to https://render.com"
echo "2. Sign in with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select this repository"
echo "5. Configure:"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r backend/requirements.txt"
echo "   - Start Command: gunicorn -w 4 -b 0.0.0.0:\$PORT backend.main:app"
echo "6. Add Environment Variable:"
echo "   - GEMINI_API_KEY: [Your API Key]"
echo "7. Deploy and get your Backend URL"
echo ""
echo "Option B - Railway:"
echo "1. Go to https://railway.app"
echo "2. Sign in with GitHub"
echo "3. Create new project from this repo"
echo "4. Similar configuration as Render"
echo ""
echo "Option C - Google Cloud Run:"
echo "1. Install gcloud CLI"
echo "2. Run: gcloud builds submit --tag gcr.io/PROJECT-ID/ava-chatbot"
echo "3. Run: gcloud run deploy ava-chatbot --image gcr.io/PROJECT-ID/ava-chatbot"
echo ""

echo "🎨 FRONTEND DEPLOYMENT (React):"
echo ""
echo "Option A - Vercel (Recommended):"
echo "1. Go to https://vercel.com"
echo "2. Click 'Import Project'"
echo "3. Select this GitHub repository"
echo "4. Configure:"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: dist"
echo "5. Deploy and get your Frontend URL"
echo ""
echo "Option B - Netlify:"
echo "1. Go to https://netlify.com"
echo "2. Click 'Import an existing project'"
echo "3. Select this repository"
echo "4. Similar configuration as Vercel"
echo ""

echo "📝 AFTER DEPLOYMENT:"
echo ""
echo "1. Get your Backend URL from Render/Railway/Cloud Run"
echo "2. Get your Frontend URL from Vercel/Netlify"
echo "3. Update frontend environment:"
echo "   - Add VITE_API_URL=[Your Backend URL] in Vercel/Netlify settings"
echo "   - OR update frontend/.env locally for testing"
echo ""
echo "4. Test the deployment:"
echo "   - Visit your frontend URL"
echo "   - Test the chatbot"
echo "   - Check browser console for errors"
echo ""

echo "🌐 WORDPRESS INTEGRATION:"
echo ""
echo "Add to your WordPress site (https://tarsgroup.co/):"
echo ""
echo "Method 1 - Using a Plugin:"
echo "1. Create /wp-content/plugins/ava-chatbot/ava-chatbot.php"
echo "2. Add the code from DEPLOYMENT.md"
echo "3. Activate the plugin"
echo "4. Add shortcode [ava_chatbot] to any page"
echo ""
echo "Method 2 - Manual HTML:"
echo "1. Add to footer or custom widget:"
echo "   <div id=\"root\"></div>"
echo "   <script type=\"module\" src=\"[Your Frontend URL]/dist/index.js\"></script>"
echo "   <link rel=\"stylesheet\" href=\"[Your Frontend URL]/dist/index.css\">"
echo ""

echo "📚 DOCUMENTATION:"
echo "See DEPLOYMENT.md for detailed instructions"
echo ""
echo "========================================="
echo "Ready to deploy! Good luck! 🚀"
echo "========================================="
