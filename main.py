from fastapi import FastAPI
from app import models
from app.database import engine
from app import user_routes, tasks_routes
from app.logging_config import logger

# Create all tables based on model definitions
# comment this line after 1st run, even though it won't recreate the table or overwrite the current one
# but still slows down the process
#models.Base.metadata.create_all(bind=engine)

logger.info("Starting the Application")
app = FastAPI()

# app.include_router(api_router)
app.include_router(user_routes.router, tags=["Users"])
app.include_router(tasks_routes.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def read_root():
 return {"message":"Welcome to the Task Manager API"}



