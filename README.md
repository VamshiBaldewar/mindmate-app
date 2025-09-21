# GathaFeed - Voice-First Mental Wellness Platform

A private, voice-first digital sanctuary where young adults can work on their mental wellness by turning their personal thoughts into a heroic journey. Built with Google Cloud AI services and modern web technologies.

## 🌟 Features

### Core Features
- **Mood-First Entry**: Users begin by selecting their current mood via emoji
- **Bolचाल Vocal Companion**: Voice-activated AI companion with localized Indian English persona
- **Generative GathaFeed**: Horizontal, right-to-left scrolling feed with:
  - Personal Gatha Panels: Generated from conversations with unique AI art
  - Curated Wisdom Panels: Inspirational quotes and poetry
- **Voice Processing**: Real-time speech-to-text and text-to-speech
- **Mood Tracking**: Comprehensive mood analytics and history
- **Dashboard**: Analytics, insights, and wellness tracking

### Technology Stack
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Flask, Python 3.8+
- **AI Services**: Google Cloud AI (Gemini Pro, Speech-to-Text, Text-to-Speech, Imagen)
- **Database**: Google Cloud Firestore
- **Authentication**: Session-based with Flask-Session

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Google Cloud API Key (provided)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Run the startup script**:
   - **Windows**: Double-click `start.bat` or run `start.bat` in command prompt
   - **Linux/Mac**: Run `./start.sh` in terminal

3. **Manual setup** (if scripts don't work):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set environment variables
   set GOOGLE_API_KEY=AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs
   set PROJECT_ID=gathafeed-ai
   
   # Start server
   python run.py
   ```

The backend will be available at `http://localhost:5000`

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

The frontend will be available at `http://localhost:3000`

## 📱 User Journey

1. **Homepage**: Users land on the beautiful landing page
2. **Authentication**: Login or signup to access the platform
3. **Mood Selection**: Choose current mood from emoji options
4. **Voice Interface**: Talk with Bolचाल AI companion
5. **GathaFeed**: View generated panels and wisdom content
6. **Dashboard**: Track mood, view analytics, and insights

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Voice & Chat
- `POST /api/voice/process` - Process voice input
- `POST /api/chat` - Text-based chat
- `POST /api/gatha/generate` - Generate Gatha panel

### Feed & Analytics
- `GET /api/feed` - Get user's GathaFeed
- `POST /api/mood/track` - Track mood
- `GET /api/mood/history` - Get mood history
- `GET /api/analytics` - Get user analytics

### Health
- `GET /api/health` - Health check

## 🎨 Design Philosophy

GathaFeed follows three core principles:

1. **No Social Comparison**: Private mirror, not public window
2. **Encourage Reflection**: Calm, minimalist UI with thoughtful consumption
3. **Voice-First**: Prioritize voice interaction for authenticity

## 🧠 AI Integration

### Google Cloud Services Used
- **Gemini Pro**: AI companion responses and narrative generation
- **Speech-to-Text**: Convert voice to text with Indian English support
- **Text-to-Speech**: Generate natural-sounding responses
- **Imagen**: Create unique artwork for Gatha panels
- **Firestore**: Store user data and conversations

### AI Features
- **Contextual Responses**: Maintains conversation context
- **Cultural Sensitivity**: Understands Indian cultural context
- **Empathetic Dialogue**: Warm, supportive responses
- **Personalized Content**: Tailored to user's mood and history

## 📊 Analytics & Insights

- Mood tracking and visualization
- Conversation history
- Wellness score calculation
- Personal growth insights
- Activity suggestions

## 🔒 Privacy & Security

- All conversations are private and encrypted
- No public profiles or social features
- Session-based authentication
- Data stored securely in Google Cloud

## 🛠️ Development

### Project Structure
```
MindMate/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── run.py              # Startup script
│   ├── requirements.txt    # Python dependencies
│   └── start.bat/.sh       # Startup scripts
├── Frontend/               # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   ├── lib/                # Utilities and API client
│   └── public/             # Static assets
└── README.md               # This file
```

### Key Components
- **VocalPage**: Voice interface with speech recognition
- **MoodSelector**: Mood selection interface
- **GathaFeed**: Feed display with panels
- **DashboardPage**: Analytics and insights
- **API Client**: Backend communication

## 🚀 Deployment

### Backend Deployment
1. Deploy to Google Cloud Run or similar platform
2. Set up environment variables
3. Configure Google Cloud services
4. Set up Firestore database

### Frontend Deployment
1. Build the Next.js application
2. Deploy to Vercel, Netlify, or similar platform
3. Configure API endpoints
4. Set up environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Cloud AI services
- Next.js and React communities
- Mental health advocates and researchers
- Indian cultural context and language support

## 📞 Support

For support or questions, please contact the development team.

---

**GathaFeed** - Where your thoughts become your story. 🌟
