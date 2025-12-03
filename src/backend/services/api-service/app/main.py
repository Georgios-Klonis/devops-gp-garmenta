from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import router
from common.errors import APIError

# Create FastAPI app
app = FastAPI(
    title="Api Service",
    description="Service for managing all apis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Health check endpoint
@app.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    return {"status": "ok", "service": "api-service"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Api Service is running"}

# Error Handler
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Return JSON response based on APIError.* sub-classes."""
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict()) 