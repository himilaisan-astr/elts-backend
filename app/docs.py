from fastapi.openapi.utils import get_openapi
from typing import Dict

def custom_openapi() -> Dict:
    """Generate custom OpenAPI schema with organized tags and descriptions."""
    
    from .main import app  # Import here to avoid circular import
    
    openapi_schema = get_openapi(
        title="ELTS API",
        version="1.0.0",
        description="English Language Training School API Documentation",
        routes=app.routes,
        tags=app.openapi_tags
    )
    
    # Remove default tag
    if "tags" in openapi_schema:
        openapi_schema["tags"] = [tag for tag in openapi_schema["tags"] if tag["name"] not in ["default", "api"]]

    # Define tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and registration operations"
        },
        {
            "name": "Dashboard",
            "description": "Dashboard statistics and system health endpoints"
        },
        {
            "name": "Students",
            "description": "Student management operations including CRUD and status updates"
        },
        {
            "name": "Teachers",
            "description": "Teacher management operations including CRUD and status updates"
        },
        {
            "name": "Courses",
            "description": "Course management operations including CRUD and status updates"
        },
        {
            "name": "Enrollments",
            "description": "Course enrollment operations and management"
        }
    ]

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Group endpoints by tags and remove default/api tags
    paths = openapi_schema["paths"]
    for path_url, path_item in paths.items():
        for method in path_item.values():
            # Always assign tags based on path, regardless of existing tags
            path_lower = path_url.lower()
            if "/token" in path_lower or "/users" in path_lower:
                method["tags"] = ["Authentication"]
            elif "/dashboard" in path_lower or "/health" in path_lower:
                method["tags"] = ["Dashboard"]
            elif "/students" in path_lower:
                method["tags"] = ["Students"]
            elif "/teachers" in path_lower:
                method["tags"] = ["Teachers"]
            elif "/courses" in path_lower:
                method["tags"] = ["Courses"]
            elif "/enrollments" in path_lower:
                method["tags"] = ["Enrollments"]
            else:
                # Hide any untagged endpoints by assigning them to a hidden group
                method["tags"] = ["hidden"]

    return openapi_schema
