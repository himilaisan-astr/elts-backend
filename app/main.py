from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api
from .docs import custom_openapi

app = FastAPI(
    title="ELTS API",
    description="English Language Training School API",
    version="1.0.0",
    openapi_tags=[],  # Remove default tags
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas by default
        "displayOperationId": False,  # Hide operation IDs
        "filter": True,  # Enable filtering
        "tagsSorter": "alpha"  # Sort tags alphabetically
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes without the /api prefix and with tags
app.include_router(
    api.router,
    tags=[]  # Ensure no default tags are added
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Health check endpoint
@app.get("/health", tags=["Dashboard"])
async def health_check():
    return {"status": "healthy"}
