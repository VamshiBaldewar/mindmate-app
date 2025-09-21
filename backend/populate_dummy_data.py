#!/usr/bin/env python3
"""
Populate MongoDB with dummy data for 2 young minds accounts
"""

import os
import sys
from datetime import datetime, timedelta
import random
from database import MongoDBService

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_dummy_users():
    """Create 2 young minds accounts with realistic data"""
    
    # User 1: Priya - 19-year-old engineering student
    priya_data = {
        "email": "priya.sharma@example.com",
        "password": "priya123",
        "name": "Priya Sharma",
        "age": 19,
        "occupation": "Engineering Student",
        "location": "Hyderabad, India",
        "interests": ["studying", "music", "yoga", "reading"],
        "personality": "introverted, anxious, ambitious",
        "goals": ["ace engineering exams", "manage stress", "build confidence"]
    }
    
    # User 2: Arjun - 21-year-old college student
    arjun_data = {
        "email": "arjun.patel@example.com", 
        "password": "arjun123",
        "name": "Arjun Patel",
        "age": 21,
        "occupation": "College Student",
        "location": "Mumbai, India",
        "interests": ["gaming", "sports", "technology", "friends"],
        "personality": "extroverted, energetic, sometimes overwhelmed",
        "goals": ["balance studies and social life", "reduce anxiety", "find purpose"]
    }
    
    return [priya_data, arjun_data]

def generate_mood_entries(user_id: str, days: int = 28):
    """Generate 3-4 weeks of mood entries"""
    moods = [
        {"mood": "happy", "emoji": "😊", "intensity": 8},
        {"mood": "calm", "emoji": "😌", "intensity": 7},
        {"mood": "sad", "emoji": "😔", "intensity": 4},
        {"mood": "anxious", "emoji": "😰", "intensity": 6},
        {"mood": "angry", "emoji": "😡", "intensity": 5},
        {"mood": "tired", "emoji": "😴", "intensity": 6},
        {"mood": "confident", "emoji": "😎", "intensity": 8},
        {"mood": "neutral", "emoji": "😑", "intensity": 5}
    ]
    
    entries = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        
        # Create 1-3 mood entries per day
        daily_entries = random.randint(1, 3)
        for j in range(daily_entries):
            mood_data = random.choice(moods)
            entry_time = date.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59)
            )
            
            entries.append({
                "mood": mood_data["mood"],
                "emoji": mood_data["emoji"],
                "intensity": mood_data["intensity"],
                "notes": generate_mood_note(mood_data["mood"]),
                "created_at": entry_time,
                "user_id": user_id
            })
    
    return entries

def generate_mood_note(mood: str):
    """Generate realistic mood notes"""
    notes = {
        "happy": [
            "Had a great day at college!",
            "Aced my math test today",
            "Spent time with friends",
            "Got positive feedback from professor",
            "Feeling motivated and energetic"
        ],
        "calm": [
            "Peaceful morning meditation",
            "Feeling centered and balanced",
            "Had a relaxing day",
            "Good sleep last night",
            "Feeling content with life"
        ],
        "sad": [
            "Feeling homesick",
            "Struggling with studies",
            "Missing my family",
            "Had a difficult day",
            "Feeling lonely"
        ],
        "anxious": [
            "Worried about upcoming exams",
            "Feeling overwhelmed with assignments",
            "Stressed about future",
            "Can't stop overthinking",
            "Feeling pressure from parents"
        ],
        "angry": [
            "Frustrated with group project",
            "Had argument with friend",
            "Feeling misunderstood",
            "Stressed about deadlines",
            "Feeling unfair treatment"
        ],
        "tired": [
            "Pulled all-nighter for exam",
            "Feeling exhausted",
            "Too much work today",
            "Need more sleep",
            "Feeling drained"
        ],
        "confident": [
            "Nailed my presentation!",
            "Feeling proud of my progress",
            "Overcame a challenge today",
            "Feeling strong and capable",
            "Ready to take on anything"
        ],
        "neutral": [
            "Regular day, nothing special",
            "Feeling okay",
            "Just going through the motions",
            "Average day",
            "Nothing to report"
        ]
    }
    
    return random.choice(notes.get(mood, ["Feeling okay"]))

def generate_conversations(user_id: str, days: int = 28):
    """Generate realistic conversations"""
    conversation_topics = [
        "I'm feeling stressed about my engineering exams. The pressure is getting to me.",
        "I had a fight with my best friend and I don't know how to fix it.",
        "My parents are putting too much pressure on me to get good grades.",
        "I feel like I'm not good enough compared to my classmates.",
        "I'm having trouble sleeping because I keep worrying about the future.",
        "I feel lonely even when I'm around people.",
        "I'm scared I'll fail my exams and disappoint everyone.",
        "I don't know what I want to do with my life after college.",
        "I feel like I'm always behind and can't catch up.",
        "I'm trying to stay positive but it's really hard sometimes.",
        "I had a good day today and I want to celebrate it.",
        "I'm learning to be more confident in myself.",
        "I had a breakthrough moment in my studies today.",
        "I'm grateful for the small things in life.",
        "I'm working on managing my anxiety better.",
        "I feel more hopeful about the future now.",
        "I'm proud of the progress I've made.",
        "I'm learning to be kinder to myself.",
        "I had a meaningful conversation with someone today.",
        "I'm trying to find balance in my life."
    ]
    
    ai_responses = [
        "I understand you're going through a challenging time. Remember, it's okay to feel overwhelmed sometimes. Take a deep breath and know that you're stronger than you think.",
        "It sounds like you're carrying a lot of weight on your shoulders. You don't have to face everything alone. What would help you feel more supported right now?",
        "I can hear the pain in your words. It takes courage to share these feelings. You're not alone in this journey, and it's okay to ask for help.",
        "Your feelings are completely valid. It's natural to feel this way when facing such pressure. What small step could you take today to care for yourself?",
        "I'm proud of you for reaching out and sharing this. It shows strength, not weakness. Let's work through this together, one step at a time.",
        "It sounds like you're being really hard on yourself. Remember, you're doing the best you can with what you have. That's enough.",
        "I can sense the fear in your words, and I want you to know that it's okay to feel scared. You're not alone, and we'll get through this together.",
        "Your honesty about these feelings is really brave. It's okay to not have all the answers right now. What matters is that you're taking care of yourself.",
        "I hear you, and I want you to know that your feelings matter. You're not alone in this struggle, and it's okay to take things one day at a time.",
        "It sounds like you're going through a lot right now. Remember, it's okay to feel this way. What would help you feel a little better today?"
    ]
    
    conversations = []
    for i in range(days * 2):  # 2 conversations per day on average
        date = datetime.now() - timedelta(days=random.randint(0, days-1))
        conversation_time = date.replace(
            hour=random.randint(9, 21),
            minute=random.randint(0, 59)
        )
        
        topic = random.choice(conversation_topics)
        ai_response = random.choice(ai_responses)
        
        conversations.append({
            "user_input": topic,
            "ai_response": ai_response,
            "mood": random.choice(["anxious", "sad", "neutral", "happy", "calm"]),
            "created_at": conversation_time,
            "user_id": user_id,
            "session_duration": random.randint(5, 30)  # minutes
        })
    
    return conversations

def generate_gatha_panels(user_id: str, days: int = 28):
    """Generate Gatha panels from conversations"""
    gatha_narratives = [
        "In the quiet moments of reflection, our thoughts become the seeds of our personal epic. Today's conversation reveals the strength that lies within vulnerability, the courage found in sharing our truth.",
        "Every challenge we face is a chapter in our story of growth. Like a river carving through stone, our struggles shape us into who we are meant to become.",
        "The journey of self-discovery is not always easy, but it is always worth it. Each conversation is a step forward on the path to understanding ourselves better.",
        "In the tapestry of life, our emotions are the threads that create the most beautiful patterns. Today's reflection shows the intricate beauty of the human experience.",
        "The mind is a garden where thoughts bloom into wisdom. Through honest conversation, we cultivate the seeds of self-awareness and growth.",
        "Every moment of struggle is a moment of strength in disguise. Our conversations reveal the resilience that lives within each of us.",
        "The path to peace begins with a single step of self-compassion. Today's reflection shows the gentle power of being kind to ourselves.",
        "In the symphony of life, our emotions are the notes that create the most beautiful melodies. Each conversation adds harmony to our personal song.",
        "The journey inward is the most important adventure we can take. Through honest dialogue, we discover the treasures hidden within our own hearts.",
        "Every conversation is a bridge between where we are and where we want to be. Today's reflection shows the power of connection and understanding."
    ]
    
    panels = []
    for i in range(days):  # One panel per day
        date = datetime.now() - timedelta(days=i)
        panel_time = date.replace(
            hour=random.randint(10, 20),
            minute=random.randint(0, 59)
        )
        
        panels.append({
            "title": f"Chapter {i+1}: A Moment of Reflection",
            "narrative": random.choice(gatha_narratives),
            "artwork_url": f"https://placeholder-image-service.onrender.com/image/500x300?prompt=meditation%20serene%20pastel%20background&id=gatha-panel-{i}",
            "conversation_excerpt": "A meaningful conversation about personal growth and self-discovery...",
            "type": "personal_gatha",
            "created_at": panel_time,
            "user_id": user_id,
            "theme": random.choice(["growth", "peace", "strength", "wisdom", "hope"])
        })
    
    return panels

def populate_database():
    """Main function to populate the database"""
    print("🚀 Starting database population...")
    
    # Initialize database service
    from database import db_service
    
    if not db_service:
        print("❌ Database connection failed!")
        return
    
    # Create users
    users_data = create_dummy_users()
    user_ids = []
    
    for user_data in users_data:
        print(f"👤 Creating user: {user_data['name']}")
        user_id = db_service.create_user(user_data)
        user_ids.append(user_id)
        print(f"✅ User created with ID: {user_id}")
    
    # Generate data for each user
    for i, user_id in enumerate(user_ids):
        user_name = users_data[i]['name']
        print(f"\n📊 Generating data for {user_name}...")
        
        # Generate mood entries (28 days)
        print("😊 Generating mood entries...")
        mood_entries = generate_mood_entries(user_id, 28)
        for entry in mood_entries:
            db_service.add_mood_entry(user_id, entry)
        print(f"✅ Created {len(mood_entries)} mood entries")
        
        # Generate conversations (28 days)
        print("💬 Generating conversations...")
        conversations = generate_conversations(user_id, 28)
        for conv in conversations:
            db_service.add_conversation(user_id, conv)
        print(f"✅ Created {len(conversations)} conversations")
        
        # Generate Gatha panels (28 days)
        print("📖 Generating Gatha panels...")
        panels = generate_gatha_panels(user_id, 28)
        for panel in panels:
            db_service.add_gatha_panel(user_id, panel)
        print(f"✅ Created {len(panels)} Gatha panels")
        
        print(f"🎉 Completed data generation for {user_name}")
    
    print("\n🌟 Database population completed successfully!")
    print(f"📊 Created {len(user_ids)} users with comprehensive data")
    print("🔗 You can now test the application with realistic data")

if __name__ == "__main__":
    populate_database()
