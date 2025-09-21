"""
MongoDB Database Service for GathaFeed
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
import logging
from pymongo import MongoClient
from bson import ObjectId

logger = logging.getLogger(__name__)

class MongoDBService:
    """MongoDB service for GathaFeed"""
    
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        self.db = self.client.gathafeed
        self.users = self.db.users
        self.conversations = self.db.conversations
        self.gatha_panels = self.db.gatha_panels
        self.mood_entries = self.db.mood_entries
        
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        try:
            user_data['created_at'] = datetime.now()
            user_data['mood_history'] = []
            user_data['conversations'] = []
            user_data['gatha_panels'] = []
            user_data['wellness_score'] = 0
            user_data['total_conversations'] = 0
            user_data['total_gatha_panels'] = 0
            
            result = self.users.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            user = self.users.find_one({"email": email.lower()})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            user = self.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def add_conversation(self, user_id: str, conversation_data: Dict[str, Any]) -> str:
        """Add a conversation"""
        try:
            conversation_data['user_id'] = user_id
            conversation_data['created_at'] = datetime.now()
            
            result = self.conversations.insert_one(conversation_data)
            
            # Update user's conversation count
            self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"total_conversations": 1}}
            )
            
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error adding conversation: {e}")
            raise
    
    def add_gatha_panel(self, user_id: str, panel_data: Dict[str, Any]) -> str:
        """Add a Gatha panel"""
        try:
            panel_data['user_id'] = user_id
            panel_data['created_at'] = datetime.now()
            
            result = self.gatha_panels.insert_one(panel_data)
            
            # Update user's panel count
            self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"total_gatha_panels": 1}}
            )
            
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error adding Gatha panel: {e}")
            raise
    
    def add_mood_entry(self, user_id: str, mood_data: Dict[str, Any]) -> str:
        """Add a mood entry"""
        try:
            mood_data['user_id'] = user_id
            mood_data['created_at'] = datetime.now()
            
            result = self.mood_entries.insert_one(mood_data)
            
            # Update user's mood history
            self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$push": {"mood_history": mood_data}}
            )
            
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error adding mood entry: {e}")
            raise
    
    def get_user_feed(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's feed with panels and wisdom"""
        try:
            # Get personal Gatha panels
            personal_panels = list(self.gatha_panels.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit))
            
            # Convert ObjectId to string
            for panel in personal_panels:
                panel['_id'] = str(panel['_id'])
                panel['type'] = 'personal_gatha'
            
            # Get wisdom panels (mock data for now)
            wisdom_panels = self._get_wisdom_panels(limit // 2)
            
            # Combine and sort
            all_panels = personal_panels + wisdom_panels
            all_panels.sort(key=lambda x: x['created_at'], reverse=True)
            
            return all_panels[:limit]
        except Exception as e:
            logger.error(f"Error getting user feed: {e}")
            return []
    
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get user analytics"""
        try:
            # Get mood history
            mood_history = list(self.mood_entries.find(
                {"user_id": user_id}
            ).sort("created_at", -1))
            
            # Get conversations
            conversations = list(self.conversations.find(
                {"user_id": user_id}
            ).sort("created_at", -1))
            
            # Get Gatha panels
            gatha_panels = list(self.gatha_panels.find(
                {"user_id": user_id}
            ).sort("created_at", -1))
            
            # Calculate mood distribution
            mood_counts = {}
            for entry in mood_history:
                mood = entry.get('mood', 'unknown')
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            # Recent activity (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            recent_conversations = len([c for c in conversations 
                                     if c['created_at'] > week_ago])
            
            # Wellness score calculation
            wellness_score = min(100, len(conversations) * 5 + len(gatha_panels) * 10)
            
            return {
                "total_conversations": len(conversations),
                "total_gatha_panels": len(gatha_panels),
                "mood_distribution": mood_counts,
                "recent_activity": {
                    "conversations_this_week": recent_conversations,
                    "last_conversation": conversations[0]['created_at'] if conversations else None
                },
                "wellness_score": wellness_score,
                "mood_history": mood_history[-30:]  # Last 30 entries
            }
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            return {}
    
    def _get_wisdom_panels(self, count: int) -> List[Dict[str, Any]]:
        """Get wisdom panels (mock data)"""
        wisdom_quotes = [
            "Breathe in peace, breathe out stress. You are enough.",
            "A calm mind is the best investment for a brighter tomorrow.",
            "Movement is a celebration of what your body can do. Keep going!",
            "The present moment is the only time over which we have dominion.",
            "You are not your thoughts. You are the observer of your thoughts.",
            "Every breath is a new beginning, every moment a fresh start.",
            "The mind is everything. What you think you become.",
            "Peace comes from within. Do not seek it without.",
            "Your mental health is a priority. Your happiness is essential.",
            "It's okay to not be okay. It's okay to ask for help.",
            "Progress, not perfection. Every step forward counts.",
            "You are stronger than you know, braver than you believe.",
            "Self-care is not selfish. It's necessary.",
            "Your feelings are valid. Your experiences matter.",
            "Healing is not linear. Be patient with yourself."
        ]
        
        panels = []
        for i in range(count):
            panels.append({
                "_id": f"wisdom_{i}_{int(datetime.now().timestamp())}",
                "type": "wisdom",
                "quote": random.choice(wisdom_quotes),
                "author": "Ancient Wisdom",
                "created_at": datetime.now() - timedelta(days=random.randint(0, 30)),
                "theme": random.choice(["general", "motivation", "peace", "growth"])
            })
        
        return panels

# Initialize MongoDB service
MONGODB_URI = "mongodb+srv://vamshibaldewar_db_user:kPVeybqmzpHaG9Pa@cluster0.bte5jzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    db_service = MongoDBService(MONGODB_URI)
    logger.info("MongoDB connected successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    db_service = None
