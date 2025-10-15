"""
Cloud-optimized OmniMind Server
Designed for free cloud deployment (Railway, Render, Heroku, etc.)
"""

import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Import existing API endpoints
from api_server import app as api_app

# Create new cloud-optimized app
app = FastAPI(title="OmniMind Cloud", description="Global AI Assistant")

# Enable CORS for all origins (cloud deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for global access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all API routes from api_server
app.mount("/api", api_app)

@app.get("/")
async def serve_frontend():
    """Serve the React frontend"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "OmniMind Cloud API", "status": "running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """Health check for cloud platforms"""
    return {"status": "healthy", "service": "omnimind"}

# Cloud platform detection and configuration
def get_cloud_config():
    """Detect cloud platform and configure accordingly"""
    config = {
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", 8000)),
        "reload": False
    }
    
    # Railway
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        config["port"] = int(os.environ.get("PORT", 8000))
        print("Detected Railway deployment")
    
    # Render
    elif os.environ.get("RENDER"):
        config["port"] = int(os.environ.get("PORT", 10000))
        print("Detected Render deployment")
    
    # Heroku
    elif os.environ.get("DYNO"):
        config["port"] = int(os.environ.get("PORT", 8000))
        print("Detected Heroku deployment")
    
    # Vercel/Netlify (serverless)
    elif os.environ.get("VERCEL") or os.environ.get("NETLIFY"):
        print("Detected serverless deployment")
    
    else:
        print("Local or generic cloud deployment")
    
    return config

if __name__ == "__main__":
    config = get_cloud_config()
    print(f"Starting OmniMind Cloud on {config['host']}:{config['port']}")
    uvicorn.run(app, **config)