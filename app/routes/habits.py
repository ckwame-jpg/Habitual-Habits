from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(prefix="/habits", tags=["Habits"])


def get_user_habit_or_404(db: Session, habit_id: int, user_id: int) -> models.Habit:
    habit = (
        db.query(models.Habit)
        .filter(models.Habit.id == habit_id, models.Habit.user_id == user_id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("/", response_model=schemas.Habit)
def create_habit(
    habit: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_habit = models.Habit(**habit.model_dump(), user_id=current_user.id)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit


@router.get("/", response_model=list[schemas.Habit])
def get_habits(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Habit).filter(models.Habit.user_id == current_user.id).all()


@router.get("/{habit_id}", response_model=schemas.Habit)
def get_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_user_habit_or_404(db, habit_id, current_user.id)


@router.put("/{habit_id}", response_model=schemas.Habit)
def update_habit(
    habit_id: int,
    updated: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    habit = get_user_habit_or_404(db, habit_id, current_user.id)

    for key, value in updated.model_dump().items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}")
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    habit = get_user_habit_or_404(db, habit_id, current_user.id)
    db.delete(habit)
    db.commit()
    return {"detail": "Habit deleted"}


@router.post("/{habit_id}/complete", response_model=schemas.HabitCompletion)
def complete_habit(
    habit_id: int,
    completion: schemas.HabitCompletionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    get_user_habit_or_404(db, habit_id, current_user.id)

    db_completion = models.HabitCompletion(
        habit_id=habit_id,
        user_id=current_user.id,
        date_completed=completion.date_completed,
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


@router.get("/{habit_id}/streak")
def get_streak(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    habit = get_user_habit_or_404(db, habit_id, current_user.id)

    completions = sorted([completion.date_completed for completion in habit.completions], reverse=True)
    if not completions:
        return {"streak": 0}

    streak = 0
    expected_day = date.today()

    for completed_day in completions:
        if completed_day != expected_day:
            break
        streak += 1
        expected_day -= timedelta(days=1)

    return {"streak": streak}
