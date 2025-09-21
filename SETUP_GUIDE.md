# 🚀 GathaFeed Setup Guide

Complete setup instructions for the GathaFeed MVP.

## 📋 Prerequisites

- **Python 3.8+** installed
- **Node.js 18+** installed
- **Google Cloud API Key** (provided: `AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs`)
- **Modern web browser** (Chrome recommended for voice features)

## 🎯 Quick Start (5 minutes)

### Step 1: Start Backend
```bash
# Navigate to backend directory
cd backend

# Windows: Double-click start.bat or run:
start.bat

# Linux/Mac: Run:
./start.sh
```

### Step 2: Start Frontend
```bash
# Open new terminal, navigate to frontend
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 3: Test the System
1. Open `http://localhost:3000` in your browser
2. Click "Get Started" or "Sign Up"
3. Create an account with any email/password
4. Select your mood
5. Start talking with Bolचाल!

## 🔧 Detailed Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables**:
   ```bash
   # Windows:
   set GOOGLE_API_KEY=AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs
   set PROJECT_ID=gathafeed-ai
   
   # Linux/Mac:
   export GOOGLE_API_KEY=AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs
   export PROJECT_ID=gathafeed-ai
   ```

6. **Start the server**:
   ```bash
   python run.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd Frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

## 🧪 Testing

### Backend API Tests
```bash
cd backend
python test_api.py
```

### Frontend API Tests
1. Open `Frontend/test-api.html` in your browser
2. Click "Run All Tests" to test all endpoints

### Manual Testing
1. **Registration**: Create a new account
2. **Login**: Sign in with your credentials
3. **Mood Selection**: Choose your current mood
4. **Voice Chat**: Click the microphone and speak
5. **Text Chat**: Type a message and get AI response
6. **Feed**: View generated Gatha panels
7. **Dashboard**: Check analytics and mood tracking

## 🌟 Features to Test

### Core Features
- ✅ User registration and login
- ✅ Mood selection and tracking
- ✅ Voice-to-text processing
- ✅ AI companion responses (Bolचाल)
- ✅ Text-based chat
- ✅ Gatha panel generation
- ✅ Feed display
- ✅ Dashboard analytics

### Voice Features
- ✅ Speech recognition (Chrome recommended)
- ✅ Text-to-speech responses
- ✅ Indian English accent support
- ✅ Real-time conversation

### AI Features
- ✅ Empathetic responses
- ✅ Cultural context understanding
- ✅ Mood-aware conversations
- ✅ Narrative generation
- ✅ Artwork generation (placeholder)

## 🔍 Troubleshooting

### Backend Issues

**Port 5000 already in use**:
```bash
# Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

**Python dependencies issues**:
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Google Cloud API errors**:
- The API key is already configured
- Mock responses will be used if services are unavailable
- Check console logs for specific error messages

### Frontend Issues

**Port 3000 already in use**:
```bash
# Kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9
```

**Node modules issues**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection issues**:
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify API endpoints are accessible

### Voice Recognition Issues

**Speech recognition not working**:
- Use Chrome browser (best support)
- Ensure microphone permissions are granted
- Check if HTTPS is required (some browsers)
- Try refreshing the page

**No audio output**:
- Check browser audio settings
- Ensure speakers/headphones are connected
- Check browser console for audio errors

## 📱 User Flow Testing

1. **Landing Page**: Beautiful homepage with call-to-action
2. **Authentication**: Sign up or login
3. **Mood Selection**: Choose from 8 mood options
4. **Voice Interface**: Talk with Bolचाल AI
5. **Text Chat**: Alternative text-based interaction
6. **GathaFeed**: View generated panels and wisdom
7. **Dashboard**: Analytics and mood tracking

## 🎨 Customization

### Backend Customization
- Edit `backend/config.py` for configuration
- Modify `backend/app.py` for API endpoints
- Update `backend/requirements.txt` for dependencies

### Frontend Customization
- Edit `Frontend/lib/api.ts` for API configuration
- Modify components in `Frontend/components/`
- Update styling in `Frontend/app/globals.css`

## 🚀 Deployment Ready

The system is ready for deployment with:
- ✅ Production-ready Flask backend
- ✅ Next.js frontend with SSR
- ✅ Google Cloud AI integration
- ✅ Session-based authentication
- ✅ Error handling and logging
- ✅ CORS configuration
- ✅ Environment variable support

## 📞 Support

If you encounter any issues:
1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Ensure both backend and frontend are running
4. Test with the provided test files
5. Check the README.md for additional information

---

**GathaFeed** - Your voice-first mental wellness companion is ready! 🌟
