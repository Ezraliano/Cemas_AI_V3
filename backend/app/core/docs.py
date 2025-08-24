from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import FastAPI
from app.core.config import settings

def setup_docs(app: FastAPI) -> None:
    """
    Configure custom API documentation settings
    """
    # Custom title and description
    app.title = settings.APP_NAME
    app.description = f"""
    {settings.APP_DESCRIPTION}
    
    ## Features
    
    * **Authentication** - Secure JWT-based authentication
    * **User Management** - User registration and profile management
    * **AI Chat** - Conversations with AI assistant using Groq Cloud and Meta Llama
    * **Mental Health Insights** - AI-generated insights from conversations
    
    ## Authentication
    
    All API endpoints (except /docs, /redoc, and /auth/token) require authentication.
    Use the /auth/token endpoint to obtain a JWT token, then include it in the Authorization header:
    
    ```
    Authorization: Bearer your_token_here
    ```
    """
    
    app.version = settings.APP_VERSION
    
    # Additional metadata
    app.openapi_tags = [
        {
            "name": "Authentication",
            "description": "Operations related to user authentication and authorization",
        },
        {
            "name": "Users",
            "description": "User management operations",
        },
        {
            "name": "Chat",
            "description": "AI conversation and message operations",
        },
    ]
    
    # Contact info
    app.openapi_contact = {
        "name": "Cemas.AI Support",
        "url": "https://cemas-ai.vercel.app/contact",
        "email": "support@cemas-ai.com",
    }
    
    # License info
    app.openapi_license = {
        "name": "Proprietary",
        "url": "https://cemas-ai.vercel.app/terms",
    }