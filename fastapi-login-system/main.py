from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base

# ✅ Routers
from routers import (
    token,        # /auth
    users_1,      # /users1
    users,        # /users
    students,     # /students
    leave_types,  # /leave-types
    leave_details,# /leave-details
    remaining_leaves,  # /remaining-leaves
    leave_applications, # /leave-applications
    combined_tables,    # /combined
    profile,
    leave_operations
)

app = FastAPI()

# ✅ CORS middleware - must be BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB Table creation
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# ✅ Include routers
app.include_router(token.router, prefix="/auth", tags=["Authentication"])
app.include_router(users_1.router, prefix="/users1", tags=["Users v1"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(leave_types.router, prefix="/leave-types", tags=["Leave Types"])
app.include_router(leave_details.router, prefix="/leave-details", tags=["Leave Details"])
app.include_router(remaining_leaves.router, prefix="/remaining-leaves")
app.include_router(leave_applications.router, prefix="/leave-applications", tags=["Leave Applications"])
app.include_router(combined_tables.router)
app.include_router(profile.router, tags=["Profile"])
app.include_router(leave_operations.router,prefix="/api/leaves",tags=["leave-operations"]
)

# ✅ Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "FastAPI Authentication System",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "students": "/students",
            "leave_applications": "/leave-applications",
            "leave_types": "/leave-types",
            "remaining_leaves": "/remaining-leaves"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
