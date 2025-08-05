from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_db, get_current_user
from typing import List
from app import models, schemas_tasks
from app.logging_config import logger

router = APIRouter()

##### CRUD Logic ######
# 📌 Create Task
@router.post("/createTask", response_model=schemas_tasks.TaskOut)
def create_task(
    task: schemas_tasks.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logger.info("Creating TASK.....")
    db_task = models.Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info("Task Created")
    return db_task

# 📌 Get all tasks of current user
@router.get("/getAllTasks", response_model=List[schemas_tasks.TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logger.info("Getting all TASKS ....")


    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()


# 📌 Update a task
@router.put("/updateTask/{task_id}", response_model=schemas_tasks.TaskOut)
def update_task(
    task_id: int,
    updated_task: schemas_tasks.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):  
    logger.info("Updating TASK .....")
    
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    
    task.title = updated_task.title
    task.description = updated_task.description
    db.commit()
    db.refresh(task)
    logger.info("Task updated")
    return task

# 📌 Delete a task
@router.delete("/deleteTask/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logging.info("Deleting TASK .....")
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    logger.info("Task Deleted")
    return {"detail": "Task deleted successfully"}