"""
GathaFeed Backend - Flask Application
A voice-first mental wellness platform powered by Google Cloud AI
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import json
import base64
import io
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any

# Google Cloud imports
import google.generativeai as genai
from google.cloud import speech
from google.cloud import texttospeech
from google.cloud import firestore
from google.cloud import storage
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai

# Import configuration
from config import config
from database import db_service

# Initialize Flask app
app = Flask(__name__)
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
CORS(app, supports_credentials=True, origins=app.config['ALLOWED_ORIGINS'])
Session(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Cloud Configuration
GOOGLE_API_KEY = app.config['GOOGLE_API_KEY']
PROJECT_ID = app.config['PROJECT_ID']
REGION = app.config['REGION']

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Google Cloud clients
try:
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=REGION)
    
    # Initialize clients
    speech_client = speech.SpeechClient()
    tts_client = texttospeech.TextToSpeechClient()
    db = firestore.Client(project=PROJECT_ID)
    storage_client = storage.Client(project=PROJECT_ID)
    
    logger.info("Google Cloud services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Google Cloud services: {e}")
    # For development, we'll use mock services
    speech_client = None
    tts_client = None
    db = None
    storage_client = None

# Initialize Gemini model
try:
    gemini_model = genai.GenerativeModel('gemini-pro')
    imagen_model = GenerativeModel("imagen-3.0-generate-001")
    logger.info("AI models initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI models: {e}")
    gemini_model = None
    imagen_model = None

# Database service is now imported from database.py

MOCK_WISDOM_QUOTES = [
    "Breathe in peace, breathe out stress. You are enough.",
    "A calm mind is the best investment for a brighter tomorrow.",
    "Movement is a celebration of what your body can do. Keep going!",
    "The present moment is the only time over which we have dominion.",
    "You are not your thoughts. You are the observer of your thoughts.",
    "Every breath is a new beginning, every moment a fresh start.",
    "The mind is everything. What you think you become.",
    "Peace comes from within. Do not seek it without."
]

class GathaFeedAI:
    """Main AI service class for GathaFeed with Reinforcement Learning"""
    
    def __init__(self):
        self.conversation_context = {}
        self.user_patterns = {}  # Store user behavior patterns
        self.learning_models = {}  # Store personalized learning models
        
    def process_voice_input(self, audio_data: bytes, user_id: str) -> Dict[str, Any]:
        """Process voice input and return text transcript"""
        try:
            if speech_client is None:
                # Mock response for development
                return {
                    "transcript": "I'm feeling stressed about my exams and need some guidance.",
                    "confidence": 0.95
                }
            
            # Configure speech recognition
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-IN",
                alternative_language_codes=["en-US", "hi-IN"],
                enable_automatic_punctuation=True,
                model="latest_long"
            )
            
            # Perform speech recognition
            response = speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                transcript = result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence
                
                return {
                    "transcript": transcript,
                    "confidence": confidence
                }
            else:
                return {"error": "No speech detected"}
                
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return {"error": "Speech recognition failed"}
    
    def generate_ai_response(self, user_input: str, user_id: str, mood: str = "neutral") -> str:
        """Generate empathetic AI response using Gemini Pro"""
        try:
            if gemini_model is None:
                # Enhanced mock response based on mood and context
                return self._generate_contextual_response(user_input, mood)
            
            # Get conversation context
            context = self.conversation_context.get(user_id, [])
            
            # Build conversation history
            conversation_history = ""
            for msg in context[-5:]:  # Last 5 messages
                conversation_history += f"User: {msg['user']}\nBolचाल: {msg['ai']}\n\n"
            
            # Create prompt for empathetic response
            prompt = f"""
            You are Bolचाल, a compassionate AI companion designed to help young adults in India with their mental wellness. 
            You speak in warm, supportive Indian English and understand the cultural context of academic pressure, family expectations, and social challenges.
            
            Current mood context: {mood}
            
            Previous conversation:
            {conversation_history}
            
            User's current message: {user_input}
            
            Respond as Bolचाल with:
            - Empathy and understanding
            - Practical, gentle advice
            - Cultural sensitivity
            - Encouragement without being preachy
            - Keep responses conversational and warm (2-3 sentences max)
            - Use Indian English expressions naturally
            
            Response:"""
            
            response = gemini_model.generate_content(prompt)
            ai_response = response.text.strip()
            
            # Update conversation context
            if user_id not in self.conversation_context:
                self.conversation_context[user_id] = []
            
            self.conversation_context[user_id].append({
                "user": user_input,
                "ai": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 10 conversations
            if len(self.conversation_context[user_id]) > 10:
                self.conversation_context[user_id] = self.conversation_context[user_id][-10:]
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI response generation error: {e}")
            return self._generate_contextual_response(user_input, mood)
    
    def _generate_contextual_response(self, user_input: str, mood: str) -> str:
        """Generate contextual responses based on mood and user input"""
        user_lower = user_input.lower()
        
        # Mood-based responses
        mood_responses = {
            'happy': [
                "That's wonderful! I can feel your positive energy through your words! What's been making you feel so good today?",
                "Your happiness is absolutely contagious! Tell me more about what's bringing you such joy!",
                "I love hearing about your positive experiences! What's been the highlight of your day so far?",
                "That's fantastic! Your positive energy is shining through. What other good things have been happening?",
                "I can feel your joy radiating through your words! What's been the best part of your day?"
            ],
            'sad': [
                "I'm really sorry you're going through this. You're not alone, and it's okay to feel this way. What's been weighing on your heart?",
                "I can hear the pain in your words, and I want you to know that I'm here for you. What's been making you feel this way?",
                "It takes courage to share when you're hurting. I'm listening, and I care about what you're going through. Tell me more.",
                "I can sense you're carrying a heavy burden. You don't have to carry it alone. What's been on your mind?",
                "Your feelings are valid, and I'm here to support you through this. What's been the hardest part lately?"
            ],
            'anxious': [
                "I can feel the worry in your words, and that's completely understandable. What's been making you feel anxious? Let's work through this together.",
                "Anxiety can be overwhelming, but you're doing great by talking about it. What specific things have been worrying you?",
                "I'm here to help you work through these anxious feelings. What's been on your mind that's causing you stress?",
                "It's okay to feel anxious - many people experience this. What's been triggering these feelings for you?",
                "I can sense your nervous energy. Let's take this one step at a time. What's been making you feel this way?"
            ],
            'angry': [
                "I can hear the frustration in your words, and I understand why you'd feel this way. What's been bothering you?",
                "Anger is a natural emotion, and it's good that you're expressing it. What's been making you feel this way?",
                "I can feel your anger, and I'm here to listen without judgment. What's been frustrating you lately?",
                "It sounds like you've been dealing with some difficult situations. What's been making you feel so angry?",
                "I can sense your frustration. Sometimes it helps to talk about what's bothering us. What's been on your mind?"
            ],
            'calm': [
                "I love the peaceful energy you're bringing today. What's helping you feel so centered and relaxed?",
                "Your calmness is really soothing to be around. What's been helping you maintain this peaceful state?",
                "It's wonderful to see you in such a serene mood. What's been contributing to your sense of calm?",
                "I can feel your inner peace radiating through your words. What's been bringing you this tranquility?",
                "Your peaceful energy is beautiful. What's been helping you stay so grounded and relaxed?"
            ],
            'tired': [
                "I can sense the exhaustion in your words. It's okay to feel tired - we all have those days. What's been draining your energy?",
                "You sound like you've been through a lot. What's been making you feel so tired lately?",
                "I can hear the fatigue in your words. What's been wearing you down? Let's talk about how we can help you recharge.",
                "It sounds like you've been pushing yourself hard. What's been taking up most of your energy lately?",
                "I can feel your tiredness, and I want to help. What's been the most draining part of your day or week?"
            ],
            'confident': [
                "I love the confidence I'm hearing in your words! What's been giving you this sense of strength and capability?",
                "Your confidence is inspiring! Tell me more about what's been making you feel so empowered lately.",
                "I can feel your self-assurance radiating through your words. What's been contributing to this positive mindset?",
                "It's wonderful to hear such confidence in your voice! What's been helping you feel so capable and strong?",
                "Your self-belief is really shining through! What's been the source of this newfound confidence?"
            ]
        }
        
        # Get mood-specific responses
        responses = mood_responses.get(mood, mood_responses['happy'])
        
        # Check for specific keywords in user input for more targeted responses
        if any(word in user_lower for word in ['work', 'job', 'career', 'office']):
            return "I can hear that work is on your mind. What's been happening at work that's affecting how you feel?"
        elif any(word in user_lower for word in ['family', 'parents', 'mother', 'father', 'siblings']):
            return "Family relationships can be complex and emotional. What's been happening with your family that you'd like to talk about?"
        elif any(word in user_lower for word in ['friend', 'friends', 'social', 'lonely', 'alone']):
            return "Social connections are so important for our wellbeing. What's been happening with your friendships or social life?"
        elif any(word in user_lower for word in ['study', 'exam', 'college', 'university', 'academic']):
            return "Academic pressure can be really overwhelming. What's been challenging you in your studies lately?"
        elif any(word in user_lower for word in ['love', 'relationship', 'boyfriend', 'girlfriend', 'dating']):
            return "Relationships can bring both joy and challenges. What's been happening in your love life that you'd like to discuss?"
        elif any(word in user_lower for word in ['future', 'career', 'dreams', 'goals', 'plans']):
            return "Thinking about the future can be both exciting and anxiety-provoking. What's been on your mind about your future?"
        else:
            # Return a random response from the mood category
            import random
            return random.choice(responses)
    
    def generate_gatha_panel(self, conversation: str, user_id: str, mood: str = "neutral") -> Dict[str, Any]:
        """Generate a Gatha panel with narrative and artwork inspired by ancient texts"""
        try:
            if gemini_model is None or imagen_model is None:
                # Mock response for development with ancient wisdom
                ancient_wisdom = self._get_ancient_wisdom_for_mood(mood)
                return {
                    "narrative": ancient_wisdom["narrative"],
                    "artwork_url": "https://placeholder-image-service.onrender.com/image/500x300?prompt=ancient%20wisdom%20meditation%20serene%20background&id=gatha-panel",
                    "title": ancient_wisdom["title"],
                    "ancient_reference": ancient_wisdom["reference"],
                    "created_at": datetime.now().isoformat()
                }
            
            # Generate narrative using Gemini with ancient text inspiration
            narrative_prompt = f"""
            Based on this conversation: "{conversation}"
            User's current mood: {mood}
            
            Create a short, poetic narrative (2-3 sentences) that transforms this personal moment into a meaningful chapter inspired by ancient Indian epics (Mahabharata, Ramayana).
            
            Draw inspiration from these themes:
            - For sadness/depression: Arjuna's doubt before Kurukshetra, Draupadi's resilience, Sita's strength in exile
            - For stress/anxiety: Krishna's guidance to Arjuna, Rama's calm in adversity, Yudhishthira's patience
            - For general struggles: The Pandavas' journey through exile, Rama's path of righteousness, Hanuman's devotion and strength
            
            Write it as if it's part of an epic poem (Gatha) about personal growth and resilience, using the wisdom of these ancient stories.
            Use beautiful, inspiring language that celebrates the user's journey while connecting to timeless wisdom.
            Focus on themes of growth, strength, dharma (righteousness), and personal transformation.
            
            Narrative:"""
            
            narrative_response = gemini_model.generate_content(narrative_prompt)
            narrative = narrative_response.text.strip()
            
            # Generate artwork using Imagen with ancient Indian aesthetic
            art_prompt = f"Create a serene, meditative artwork inspired by ancient Indian epics and this conversation: {conversation[:100]}... Use soft pastel colors, peaceful imagery, ancient Indian aesthetic, and a calming design suitable for mental wellness. Include subtle references to Indian mythology and wisdom."
            
            try:
                image_response = imagen_model.generate_images(
                    prompt=art_prompt,
                    number_of_images=1,
                    language="en",
                    style="photographic"
                )
                
                # For now, we'll use a placeholder URL
                # In production, you'd upload the generated image to Cloud Storage
                artwork_url = "https://placeholder-image-service.onrender.com/image/500x300?prompt=ancient%20indian%20wisdom%20meditation%20serene%20background&id=gatha-panel"
                
            except Exception as e:
                logger.error(f"Image generation error: {e}")
                artwork_url = "https://placeholder-image-service.onrender.com/image/500x300?prompt=ancient%20indian%20wisdom%20meditation%20serene%20background&id=gatha-panel"
            
            # Get ancient wisdom reference
            ancient_wisdom = self._get_ancient_wisdom_for_mood(mood)
            
            gatha_panel = {
                "id": f"gatha_{user_id}_{int(datetime.now().timestamp())}",
                "narrative": narrative,
                "artwork_url": artwork_url,
                "title": ancient_wisdom["title"],
                "ancient_reference": ancient_wisdom["reference"],
                "conversation_excerpt": conversation[:100] + "..." if len(conversation) > 100 else conversation,
                "created_at": datetime.now().isoformat(),
                "type": "personal_gatha",
                "mood": mood
            }
            
            return gatha_panel
            
        except Exception as e:
            logger.error(f"Gatha panel generation error: {e}")
            ancient_wisdom = self._get_ancient_wisdom_for_mood(mood)
            return {
                "narrative": ancient_wisdom["narrative"],
                "artwork_url": "https://placeholder-image-service.onrender.com/image/500x300?prompt=ancient%20indian%20wisdom%20meditation%20serene%20background&id=gatha-panel",
                "title": ancient_wisdom["title"],
                "ancient_reference": ancient_wisdom["reference"],
                "created_at": datetime.now().isoformat()
            }
    
    def _get_ancient_wisdom_for_mood(self, mood: str) -> Dict[str, str]:
        """Get ancient wisdom references based on mood"""
        wisdom_data = {
            'sad': {
                "narrative": "Like Arjuna on the battlefield of Kurukshetra, you stand at the crossroads of your own journey. In your moment of doubt and sadness, remember that even the greatest warriors face darkness before finding their light. Your tears water the seeds of your future strength.",
                "title": "The Warrior's Path",
                "reference": "Mahabharata - Arjuna's doubt before the great war, finding strength through Krishna's guidance"
            },
            'depressed': {
                "narrative": "In the depths of your darkness, remember Sita's resilience during her exile. Like the earth itself, she remained unbroken despite the storms. Your depression is not your weakness—it is the soil from which your greatest strength will grow.",
                "title": "The Earth's Resilience",
                "reference": "Ramayana - Sita's strength and resilience during her exile, finding inner power in difficult times"
            },
            'stressed': {
                "narrative": "Like Rama facing the challenges of his journey, you too are navigating the path of dharma. In your stress, remember that even the greatest kings faced overwhelming odds. Your anxiety is the mind's way of preparing you for the battles ahead.",
                "title": "The Path of Dharma",
                "reference": "Ramayana - Rama's calm leadership and righteous path through adversity"
            }
        }
        
        return wisdom_data.get(mood, {
            "narrative": "In the quiet moments of reflection, our thoughts become the seeds of our personal epic. Today's conversation reveals the strength that lies within vulnerability, the courage found in sharing our truth.",
            "title": "The Journey Within",
            "reference": "Ancient wisdom - Every conversation is a step forward in your journey of self-discovery"
        })
    
    def update_user_patterns(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update user patterns using reinforcement learning"""
        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = {
                'mood_history': [],
                'conversation_topics': [],
                'response_preferences': {},
                'improvement_trends': [],
                'engagement_levels': [],
                'learning_progress': 0
            }
        
        # Update mood patterns
        if 'mood' in interaction_data:
            self.user_patterns[user_id]['mood_history'].append({
                'mood': interaction_data['mood'],
                'timestamp': datetime.now().isoformat(),
                'context': interaction_data.get('context', '')
            })
        
        # Update conversation topics
        if 'conversation_topic' in interaction_data:
            self.user_patterns[user_id]['conversation_topics'].append(
                interaction_data['conversation_topic']
            )
        
        # Update response preferences based on user feedback
        if 'response_rating' in interaction_data:
            rating = interaction_data['response_rating']
            topic = interaction_data.get('conversation_topic', 'general')
            
            if topic not in self.user_patterns[user_id]['response_preferences']:
                self.user_patterns[user_id]['response_preferences'][topic] = []
            
            self.user_patterns[user_id]['response_preferences'][topic].append(rating)
        
        # Calculate improvement trends
        self._calculate_improvement_trends(user_id)
        
        # Update learning progress
        self._update_learning_progress(user_id)
    
    def _calculate_improvement_trends(self, user_id: str):
        """Calculate improvement trends using reinforcement learning"""
        mood_history = self.user_patterns[user_id]['mood_history']
        
        if len(mood_history) < 2:
            return
        
        # Define mood scores for trend calculation
        mood_scores = {
            'sad': 2,
            'depressed': 1,
            'stressed': 3,
            'neutral': 5,
            'calm': 7,
            'happy': 9
        }
        
        # Calculate recent vs older mood scores
        recent_moods = mood_history[-7:] if len(mood_history) >= 7 else mood_history
        older_moods = mood_history[-14:-7] if len(mood_history) >= 14 else []
        
        if older_moods:
            recent_score = sum(mood_scores.get(m['mood'], 5) for m in recent_moods) / len(recent_moods)
            older_score = sum(mood_scores.get(m['mood'], 5) for m in older_moods) / len(older_moods)
            
            improvement = (recent_score - older_score) * 100
            self.user_patterns[user_id]['improvement_trends'].append({
                'improvement': improvement,
                'timestamp': datetime.now().isoformat()
            })
    
    def _update_learning_progress(self, user_id: str):
        """Update learning progress based on user engagement"""
        patterns = self.user_patterns[user_id]
        
        # Calculate progress based on various factors
        conversation_count = len(patterns['conversation_topics'])
        mood_consistency = len(set(m['mood'] for m in patterns['mood_history']))
        improvement_trend = patterns['improvement_trends'][-1]['improvement'] if patterns['improvement_trends'] else 0
        
        # Learning progress formula
        progress = min(100, (conversation_count * 5) + (mood_consistency * 3) + max(0, improvement_trend * 2))
        
        patterns['learning_progress'] = progress
    
    def get_personalized_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized recommendations using reinforcement learning"""
        if user_id not in self.user_patterns:
            return self._get_default_recommendations()
        
        patterns = self.user_patterns[user_id]
        
        # Analyze user patterns
        dominant_mood = self._get_dominant_mood(patterns['mood_history'])
        improvement_trend = patterns['improvement_trends'][-1]['improvement'] if patterns['improvement_trends'] else 0
        conversation_depth = len(patterns['conversation_topics'])
        
        # Generate personalized recommendations
        recommendations = []
        
        # Mood-based recommendations
        if dominant_mood in ['sad', 'depressed']:
            recommendations.append({
                'type': 'activity',
                'title': 'Gentle Movement Practice',
                'description': 'Start with 5 minutes of gentle stretching or walking. Like Hanuman\'s devotion, small consistent actions build great strength.',
                'priority': 'high',
                'reason': 'Physical movement releases endorphins and helps regulate mood',
                'estimated_time': '5-10 minutes'
            })
            
            recommendations.append({
                'type': 'reflection',
                'title': 'Gratitude Journaling',
                'description': 'Write down 3 things you\'re grateful for each day. Like Draupadi\'s resilience, gratitude helps you find strength in difficult times.',
                'priority': 'medium',
                'reason': 'Gratitude practice has been shown to improve mood and mental health',
                'estimated_time': '5 minutes'
            })
        
        elif dominant_mood == 'stressed':
            recommendations.append({
                'type': 'breathing',
                'title': 'Mindful Breathing',
                'description': 'Practice box breathing: 4 counts in, 4 hold, 4 out, 4 hold. Like Rama\'s calm in adversity, this centers your mind.',
                'priority': 'high',
                'reason': 'Controlled breathing activates your parasympathetic nervous system',
                'estimated_time': '3-5 minutes'
            })
        
        # Progress-based recommendations
        if improvement_trend > 20:
            recommendations.append({
                'type': 'celebration',
                'title': 'Progress Celebration',
                'description': 'Your improvement trend shows you\'re on the right path! Like the Pandavas\' journey through exile, every step forward builds your inner strength.',
                'priority': 'medium',
                'reason': 'Acknowledging progress reinforces positive patterns',
                'estimated_time': '2 minutes'
            })
        
        # Engagement-based recommendations
        if conversation_depth > 10:
            recommendations.append({
                'type': 'deep_reflection',
                'title': 'Deep Reflection Practice',
                'description': 'Your consistent conversations show deep self-awareness. Like Krishna guiding Arjuna, you\'re developing the wisdom to navigate life\'s challenges.',
                'priority': 'medium',
                'reason': 'Deep reflection practices will enhance your natural strength',
                'estimated_time': '10-15 minutes'
            })
        
        return {
            'recommendations': recommendations,
            'learning_progress': patterns['learning_progress'],
            'improvement_trend': improvement_trend,
            'dominant_mood': dominant_mood,
            'conversation_depth': conversation_depth
        }
    
    def _get_dominant_mood(self, mood_history: List[Dict]) -> str:
        """Get the dominant mood from user's history"""
        if not mood_history:
            return 'neutral'
        
        mood_counts = {}
        for mood_entry in mood_history:
            mood = mood_entry['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        return max(mood_counts, key=mood_counts.get)
    
    def _get_default_recommendations(self) -> Dict[str, Any]:
        """Get default recommendations for new users"""
        return {
            'recommendations': [
                {
                    'type': 'general',
                    'title': 'Welcome to Your Journey',
                    'description': 'Start by sharing how you\'re feeling today. Every conversation is a step forward in your personal growth.',
                    'priority': 'high',
                    'reason': 'Begin your wellness journey with self-reflection',
                    'estimated_time': '5 minutes'
                }
            ],
            'learning_progress': 0,
            'improvement_trend': 0,
            'dominant_mood': 'neutral',
            'conversation_depth': 0
            }
    
    def get_wisdom_panel(self, theme: str = "general") -> Dict[str, Any]:
        """Get a curated wisdom panel based on theme"""
        import random
        
        quote = random.choice(MOCK_WISDOM_QUOTES)
        
        return {
            "id": f"wisdom_{int(datetime.now().timestamp())}",
            "quote": quote,
            "author": "Ancient Wisdom",
            "type": "wisdom",
            "created_at": datetime.now().isoformat(),
            "theme": theme
        }

# Initialize AI service
ai_service = GathaFeedAI()

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "speech_to_text": speech_client is not None,
            "text_to_speech": tts_client is not None,
            "ai_model": gemini_model is not None,
            "database": db is not None
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        if not db_service:
            return jsonify({"error": "Database not available"}), 500
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        email = data['email'].lower()
        
        # Check if user already exists
        existing_user = db_service.get_user_by_email(email)
        if existing_user:
            return jsonify({"error": "User already exists"}), 409
        
        # Create new user
        user_data = {
            "email": email,
            "password": data['password'],  # In production, hash this
            "name": data['name']
        }
        
        user_id = db_service.create_user(user_data)
        
        # Set session
        session['user_id'] = user_id
        session['email'] = email
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user_id,
                "email": email,
                "name": data['name']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": "Registration failed"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        if not db_service:
            return jsonify({"error": "Database not available"}), 500
            
        data = request.get_json()
        
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Check user credentials
        user = db_service.get_user_by_email(email)
        if user and user['password'] == password:
            # Set session
            session['user_id'] = user['_id']
            session['email'] = email
            
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user['_id'],
                    "email": user['email'],
                    "name": user['name']
                }
            })
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get current user information"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    if not db_service:
        return jsonify({"error": "Database not available"}), 500
    
    user = db_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user['_id'],
        "email": user['email'],
        "name": user['name'],
        "created_at": user['created_at'].isoformat() if isinstance(user['created_at'], datetime) else user['created_at']
    })

@app.route('/api/voice/process', methods=['POST'])
def process_voice():
    """Process voice input and return AI response"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Get audio data
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        
        # Get mood context
        mood = request.form.get('mood', 'neutral')
        
        # Process voice input
        voice_result = ai_service.process_voice_input(audio_data, user_id)
        
        if 'error' in voice_result:
            return jsonify({"error": voice_result['error']}), 400
        
        transcript = voice_result['transcript']
        
        # Generate AI response
        ai_response = ai_service.generate_ai_response(transcript, user_id, mood)
        
        # Update user's conversation history
        if db_service:
            db_service.add_conversation(user_id, {
                "user_input": transcript,
                "ai_response": ai_response,
                "mood": mood
            })
        
        return jsonify({
            "transcript": transcript,
            "ai_response": ai_response,
            "confidence": voice_result.get('confidence', 0.0)
        })
        
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        return jsonify({"error": "Voice processing failed"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Text-based chat endpoint"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        data = request.get_json()
        user_input = data.get('text', '')
        mood = data.get('mood', 'neutral')
        
        if not user_input:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate AI response
        ai_response = ai_service.generate_ai_response(user_input, user_id, mood)
        
        # Update user's conversation history
        if db_service:
            db_service.add_conversation(user_id, {
                "user_input": user_input,
                "ai_response": ai_response,
                "mood": mood
            })
        
        return jsonify({
            "reply": ai_response
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": "Chat failed"}), 500

@app.route('/api/gatha/generate', methods=['POST'])
def generate_gatha_panel():
    """Generate a Gatha panel from conversation with ancient wisdom"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        data = request.get_json()
        conversation = data.get('conversation', '')
        mood = data.get('mood', 'neutral')
        
        if not conversation:
            return jsonify({"error": "No conversation provided"}), 400
        
        # Generate Gatha panel with mood and ancient wisdom
        gatha_panel = ai_service.generate_gatha_panel(conversation, user_id, mood)
        
        # Store in user's data
        if db_service:
            db_service.add_gatha_panel(user_id, gatha_panel)
        
        return jsonify(gatha_panel)
        
    except Exception as e:
        logger.error(f"Gatha generation error: {e}")
        return jsonify({"error": "Gatha generation failed"}), 500

@app.route('/api/feed', methods=['GET'])
def get_feed():
    """Get user's GathaFeed with panels and wisdom"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        if not db_service:
            return jsonify({"error": "Database not available"}), 500
        
        # Get user's feed from database
        panels = db_service.get_user_feed(user_id, 20)
        
        return jsonify({
            "panels": panels,
            "total_count": len(panels)
        })
        
    except Exception as e:
        logger.error(f"Feed retrieval error: {e}")
        return jsonify({"error": "Feed retrieval failed"}), 500

@app.route('/api/mood/track', methods=['POST'])
def track_mood():
    """Track user's mood"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        data = request.get_json()
        mood = data.get('mood', '')
        emoji = data.get('emoji', '')
        notes = data.get('notes', '')
        
        if not mood:
            return jsonify({"error": "Mood is required"}), 400
        
        # Add mood entry to database
        if db_service:
            mood_entry = {
                "mood": mood,
                "emoji": emoji,
                "notes": notes
            }
            db_service.add_mood_entry(user_id, mood_entry)
        
        return jsonify({
            "message": "Mood tracked successfully",
            "mood_entry": mood_entry
        })
        
    except Exception as e:
        logger.error(f"Mood tracking error: {e}")
        return jsonify({"error": "Mood tracking failed"}), 500

@app.route('/api/mood/history', methods=['GET'])
def get_mood_history():
    """Get user's mood history"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        if not db_service:
            return jsonify({"error": "Database not available"}), 500
        
        # Get mood history from database
        analytics = db_service.get_user_analytics(user_id)
        mood_history = analytics.get('mood_history', [])
        
        return jsonify({
            "mood_history": mood_history
        })
        
    except Exception as e:
        logger.error(f"Mood history error: {e}")
        return jsonify({"error": "Mood history retrieval failed"}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get user analytics and insights with reinforcement learning"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        if not db_service:
            return jsonify({"error": "Database not available"}), 500
        
        # Get analytics from database
        analytics = db_service.get_user_analytics(user_id)
        
        # Add personalized recommendations using reinforcement learning
        personalized_recommendations = ai_service.get_personalized_recommendations(user_id)
        analytics['personalized_recommendations'] = personalized_recommendations
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return jsonify({"error": "Analytics retrieval failed"}), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get personalized recommendations using reinforcement learning"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        # Get personalized recommendations
        recommendations = ai_service.get_personalized_recommendations(user_id)
        
        return jsonify(recommendations)
        
    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        return jsonify({"error": "Recommendations failed"}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for reinforcement learning"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        data = request.get_json()
        feedback_data = {
            'response_rating': data.get('rating'),
            'conversation_topic': data.get('topic', 'general'),
            'mood': data.get('mood'),
            'context': data.get('context', '')
        }
        
        # Update user patterns with feedback
        ai_service.update_user_patterns(user_id, feedback_data)
        
        return jsonify({"message": "Feedback recorded successfully"})
        
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        return jsonify({"error": "Feedback submission failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
