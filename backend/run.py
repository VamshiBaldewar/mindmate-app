"""
GathaFeed Backend Startup Script
"""

import os
import sys
from app import app, logger

def main():
    """Main startup function"""
    try:
        # Set environment variables if not already set
        if not os.environ.get('SECRET_KEY'):
            os.environ['SECRET_KEY'] = 'gathafeed-secret-key-2024'
        
        if not os.environ.get('GOOGLE_API_KEY'):
            os.environ['GOOGLE_API_KEY'] = 'AIzaSyAqyOxS65ZeQz9r3zajaosNtShqZnbSqbs'
        
        if not os.environ.get('PROJECT_ID'):
            os.environ['PROJECT_ID'] = 'gathafeed-ai'
        
        # Start the Flask application
        logger.info("Starting GathaFeed Backend Server...")
        logger.info("Available endpoints:")
        logger.info("  - GET  /api/health")
        logger.info("  - POST /api/auth/register")
        logger.info("  - POST /api/auth/login")
        logger.info("  - POST /api/auth/logout")
        logger.info("  - GET  /api/auth/me")
        logger.info("  - POST /api/voice/process")
        logger.info("  - POST /api/chat")
        logger.info("  - POST /api/gatha/generate")
        logger.info("  - GET  /api/feed")
        logger.info("  - POST /api/mood/track")
        logger.info("  - GET  /api/mood/history")
        logger.info("  - GET  /api/analytics")
        
        app.run(
            debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
