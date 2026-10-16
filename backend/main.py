import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes.agent_routes import router as agent_router
from backend.config import settings, get_system_status

app = FastAPI(
    title="AI Newsletter Agent API",
    description="Autonomous Agentic Workflow for Researching, Writing, Critiquing, and Simulating Dispatch of AI Newsletters",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server and production clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent API routes
app.include_router(agent_router)

# Mount outputs directory for direct preview if desired
if os.path.exists(settings.OUTPUT_DIRECTORY):
    app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUT_DIRECTORY)), name="outputs")

@app.get("/health")
def health_check():
    return {"status": "ok", "system": get_system_status()}

# Serve built frontend if dist exists (for Docker & full-stack single-port deployment)
frontend_dist = os.path.join(settings.BASE_DIR, "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "service": "AI Newsletter Agent API",
            "version": "1.0.0",
            "status": "healthy",
            "docs": "/docs",
            "system": get_system_status()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
