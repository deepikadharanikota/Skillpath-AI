"""
resume.py
---------
Router for persistent resume management, skill extraction, and skill gap analysis.
Enforces: ONE USER = ONE ACTIVE RESUME.
"""

import os
import io
import shutil
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from database import get_db
from redis_client import get_session
import models
from skills_service import extract_skills_from_text, categorize_skills, compute_skill_gap
from data import ROLES, ROLE_SKILLS

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../uploads/resumes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_current_user(token: str = Header(...), db: AsyncSession = Depends(get_db)):
    user_id = await get_session(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def _extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """Extracts text from PDF, DOCX, or plain text."""
    lower = filename.lower()
    text = ""
    if lower.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")
    elif lower.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text from DOCX: {str(e)}")
    else:
        # Fallback to UTF-8 text decoding
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
    return text.strip()

@router.post("/upload")
async def upload_resume(
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    target_role: Optional[str] = Form(None),
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload or replace a user's resume.
    Ensures ONE active resume per user by replacing previous stored files and data.
    """
    final_text = ""
    saved_filename = "pasted_resume.txt"
    saved_path = None

    if file and file.filename:
        saved_filename = file.filename
        file_bytes = await file.read()
        final_text = _extract_text_from_bytes(file_bytes, file.filename)
        
        # Save to disk: one user = one file (prefixed by user_id)
        # Remove any old file for this user first
        for old_file in os.listdir(UPLOAD_DIR):
            if old_file.startswith(f"user_{user.id}_"):
                try:
                    os.remove(os.path.join(UPLOAD_DIR, old_file))
                except Exception:
                    pass

        safe_name = f"user_{user.id}_{file.filename}"
        saved_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(saved_path, "wb") as f:
            f.write(file_bytes)
    elif resume_text:
        final_text = resume_text.strip()
    else:
        raise HTTPException(status_code=400, detail="No resume file or text provided")

    if not final_text:
        raise HTTPException(status_code=400, detail="Could not extract readable text from provided resume.")

    # Extract & Categorize Skills
    skills = extract_skills_from_text(final_text)
    categorized = categorize_skills(skills)

    # Get or create UserState
    res = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = res.scalars().first()
    if not user_state:
        user_state = models.UserState(user_id=user.id)
        db.add(user_state)

    selected_role = target_role or user_state.target_role or "ML Engineer"
    now_str = datetime.utcnow().strftime("%d %b %Y")

    # Update state fields
    user_state.target_role = selected_role
    user_state.resume_filename = saved_filename
    user_state.resume_uploaded_at = now_str
    user_state.resume_file_path = saved_path
    user_state.resume_text = final_text[:5000] # store preview / text
    user_state.extracted_skills = skills
    user_state.extracted_skills_categorized = categorized

    # Log activity
    act = models.LearningActivity(
        user_id=user.id,
        activity_type="uploaded_resume",
        title="Uploaded Resume & Extracted Skills",
        description=f"Identified {len(skills)} technical skills for {selected_role}",
        topic=None,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(act)

    await db.commit()
    await db.refresh(user_state)

    gap_data = compute_skill_gap(skills, selected_role)

    return {
        "success": True,
        "message": "Resume uploaded and skills extracted successfully",
        "resume": {
            "filename": saved_filename,
            "uploaded_at": now_str,
            "skills_count": len(skills),
            "target_role": selected_role
        },
        "extracted_skills": skills,
        "categorized_skills": categorized,
        "skill_gap": gap_data
    }

class TargetRoleUpdate(BaseModel):
    target_role: str

@router.put("/target-role")
async def update_target_role(
    payload: TargetRoleUpdate,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Updates target role and returns recalculation of skill gaps."""
    res = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = res.scalars().first()
    if not user_state:
        raise HTTPException(status_code=404, detail="User state not found")

    user_state.target_role = payload.target_role
    await db.commit()

    gap_data = compute_skill_gap(user_state.extracted_skills or [], payload.target_role)
    return {
        "success": True,
        "target_role": payload.target_role,
        "skill_gap": gap_data
    }

@router.get("")
async def get_resume_info(
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Returns the user's active resume and skill data."""
    res = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = res.scalars().first()
    if not user_state or not user_state.resume_filename:
        return {
            "has_resume": False,
            "resume": None,
            "extracted_skills": [],
            "categorized_skills": {},
            "target_role": user_state.target_role if user_state else "ML Engineer",
            "skill_gap": compute_skill_gap([], user_state.target_role if user_state else "ML Engineer")
        }

    gap_data = compute_skill_gap(user_state.extracted_skills or [], user_state.target_role or "ML Engineer")

    return {
        "has_resume": True,
        "resume": {
            "filename": user_state.resume_filename,
            "uploaded_at": user_state.resume_uploaded_at or "Unknown",
            "skills_count": len(user_state.extracted_skills or [])
        },
        "extracted_skills": user_state.extracted_skills or [],
        "categorized_skills": user_state.extracted_skills_categorized or {},
        "target_role": user_state.target_role,
        "skill_gap": gap_data
    }

@router.get("/skill-gap")
async def get_skill_gap(
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Returns comprehensive skill gap analysis."""
    res = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = res.scalars().first()
    if not user_state:
        return compute_skill_gap([], "ML Engineer")

    return compute_skill_gap(user_state.extracted_skills or [], user_state.target_role or "ML Engineer")
