from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database import engine, Base
import models
import os
from routers import auth, quiz, learning, dashboard, resume
from contextlib import asynccontextmanager
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        migrations = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS resume_filename VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS resume_uploaded_at VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS resume_file_path VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS resume_text TEXT;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS extracted_skills_categorized JSON;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS video_progress JSON DEFAULT '{}'::json;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS topic_ability JSON DEFAULT '{}'::json;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS last_video_id VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS last_video_title VARCHAR;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS last_video_position_seconds FLOAT DEFAULT 0.0;",
            "ALTER TABLE user_states ADD COLUMN IF NOT EXISTS last_accessed_at VARCHAR;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS quiz_id VARCHAR;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS questions JSON;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS user_answers JSON;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS correct_answers JSON;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS score INTEGER DEFAULT 0;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS total_questions INTEGER DEFAULT 0;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS percentage FLOAT DEFAULT 0.0;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS unanswered INTEGER DEFAULT 0;",
            "ALTER TABLE quiz_history ADD COLUMN IF NOT EXISTS completed_at VARCHAR;",
        ]
        for stmt in migrations:
            try:
                await conn.execute(text(stmt))
            except Exception as err:
                print(f"Migration note: {err}")
    yield

app = FastAPI(title="SkillPath AI Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecretkey_change_me"))

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(learning.router, prefix="/learning", tags=["learning"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

from data import ROLES
from roles_config import ROLES_REGISTRY

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/roles")
def get_roles():
    return {
        "roles": ROLES,
        "roles_detail": ROLES_REGISTRY
    }

