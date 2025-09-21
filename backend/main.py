import os
from app import app as flask_app
from netlify_lambda_wsgi import handle_request

def handler(event, context):
    return handle_request(flask_app, event, context)
