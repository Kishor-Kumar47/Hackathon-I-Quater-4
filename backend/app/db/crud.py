from typing import Dict, Optional
from backend.app.db.schemas import UserCreate, UserInDB
from backend.app.core.security import get_password_hash

# In-memory database for demonstration purposes
# In a real application, this would interact with a persistent database (e.g., PostgreSQL)
users_db: Dict[str, UserInDB] = {}
next_user_id = 1

def get_user_by_email(email: str) -> Optional[UserInDB]:
    return users_db.get(email)

def create_user(user: UserCreate) -> UserInDB:
    global next_user_id
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        id=next_user_id,
        email=user.email,
        hashed_password=hashed_password,
        programming_level=user.programming_level,
        hardware_background=user.hardware_background,
        ai_knowledge=user.ai_knowledge,
        ros_experience=user.ros_experience,
    )
    users_db[user.email] = user_in_db
    next_user_id += 1
    return user_in_db
