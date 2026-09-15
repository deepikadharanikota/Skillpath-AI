import os
import json
import logging
import random
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from redis_client import get_session
import models
from pydantic import BaseModel
from typing import List

try:
    from youtubesearchpython import VideosSearch
except ImportError:
    VideosSearch = None

from dqn_agent import DQNAgent
from environment import STATE_DIM, ACTION_DIM
from recommender import get_initial_recommendation, get_next_recommendation, evaluate_code
from agent_utils import extract_skills_from_text, compute_reward, get_module_status, compute_topic_knowledge
from data import ROLES, ROLE_SKILLS, TOPICS, MODULE_STRUCTURE, MODULE_KEYS, VIDEO_DB

router = APIRouter()

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "../dqn_weights.pkl")
agent = DQNAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM, seed=42)
if os.path.exists(WEIGHTS_PATH):
    try:
        agent.load(WEIGHTS_PATH)
    except Exception:
        pass

async def get_current_user(token: str = Header(...), db: AsyncSession = Depends(get_db)):
    user_id = await get_session(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    return user

class ResumeSubmit(BaseModel):
    resume_text: str
    target_role: str

@router.post("/start")
async def start_learning(payload: ResumeSubmit, user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    skills = extract_skills_from_text(payload.resume_text)
    role_skills = ROLE_SKILLS.get(payload.target_role, [])
    
    rec = get_initial_recommendation(agent, payload.target_role, skills, role_skills)
    topic = rec["topic"] if rec["topic"] in TOPICS else "Machine Learning"
    
    # Update UserState
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    if not user_state:
        user_state = models.UserState(user_id=user.id)
        db.add(user_state)
        
    user_state.target_role = payload.target_role
    user_state.extracted_skills = skills
    user_state.current_topic = topic
    user_state.current_difficulty = rec.get("difficulty", "beginner")
    user_state.current_module = "intro"
    user_state.module_progress = {topic: {"intro": "active", "core": "locked", "summary": "locked"}}
    user_state.fatigue = 0.0
    await db.commit()
    
    state_dict = {
        "target_role": user_state.target_role,
        "extracted_skills": user_state.extracted_skills,
        "current_topic": user_state.current_topic,
        "current_difficulty": user_state.current_difficulty,
        "current_module": user_state.current_module,
        "module_progress": user_state.module_progress,
        "fatigue": user_state.fatigue,
    }
    
    return {"recommendation": rec, "state": state_dict}

class CodeSubmit(BaseModel):
    code: str

@router.post("/evaluate_code")
async def eval_code(payload: CodeSubmit, user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    
    eval_result = evaluate_code(payload.code, user_state.current_topic, user_state.current_difficulty, user_state.current_module)
    return eval_result

class ModuleSubmit(BaseModel):
    quiz_score: float
    code_score: float

@router.post("/submit_module")
async def submit_module(payload: ModuleSubmit, user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    
    role_skills = ROLE_SKILLS.get(user_state.target_role, [])
    topic = user_state.current_topic
    module = user_state.current_module
    
    topic_alignment = 1.0 if topic in role_skills else 0.3
    mastery_gain = ((payload.quiz_score + payload.code_score) / 200) * 0.3
    new_fatigue = min(1.0, user_state.fatigue + 0.1)
    
    reward = compute_reward(payload.quiz_score, payload.code_score, mastery_gain, new_fatigue, topic_alignment)
    
    history_entry = models.QuizHistory(
        user_id=user.id,
        topic=topic,
        module_key=module,
        difficulty=user_state.current_difficulty,
        quiz_score=payload.quiz_score,
        code_score=payload.code_score,
        reward=reward
    )
    db.add(history_entry)
    
    # Update progress
    progress = user_state.module_progress or {}
    if topic not in progress:
        progress[topic] = {"intro": "locked", "core": "locked", "summary": "locked"}
    progress[topic][module] = "completed"
    
    idx = MODULE_KEYS.index(module)
    next_mod = MODULE_KEYS[idx + 1] if idx + 1 < len(MODULE_KEYS) else None
    if next_mod:
        progress[topic][next_mod] = "active"
        
    user_state.module_progress = progress
    user_state.fatigue = new_fatigue
    await db.commit()
    
    # We would ideally call the DQN step here if pending_state was stored.
    # For now, we fetch history and ask agent for next recommendation.
    history_res = await db.execute(select(models.QuizHistory).filter(models.QuizHistory.user_id == user.id).order_by(models.QuizHistory.id.desc()).limit(10))
    recent_history_objs = history_res.scalars().all()
    # reverse to chronological
    recent_history = [{"topic": h.topic, "quizScore": h.quiz_score} for h in reversed(recent_history_objs)]
    
    topic_mastery = {}
    for t in TOPICS:
        t_hist = [h for h in recent_history if h["topic"] == t]
        topic_mastery[t] = (sum(h["quizScore"] for h in t_hist) / len(t_hist) / 100) if t_hist else 0.0

    rec = get_next_recommendation(
        agent,
        target_role=user_state.target_role,
        completed_topic=topic,
        completed_module=module,
        quiz_score=payload.quiz_score,
        code_score=payload.code_score,
        difficulty=user_state.current_difficulty,
        topic_mastery=topic_mastery,
        recent_history=recent_history[-3:],
        fatigue=new_fatigue
    )
    
    next_topic = rec["topic"] if rec["topic"] in TOPICS else topic
    if next_topic == topic and next_mod:
        target_module = next_mod
    else:
        existing = progress.get(next_topic, {})
        target_module = next(
            (m for m in MODULE_KEYS if existing.get(m) != "completed"), "intro"
        )
        if next_topic not in progress:
            progress[next_topic] = {"intro": "locked", "core": "locked", "summary": "locked"}
        progress[next_topic][target_module] = "active"
        
    user_state.current_topic = next_topic
    user_state.current_difficulty = rec.get("difficulty", user_state.current_difficulty)
    user_state.current_module = target_module
    user_state.module_progress = progress
    await db.commit()
    
    return {"reward": reward, "next_recommendation": rec}

@router.get("/state")
async def get_state(user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    if not user_state:
        return None
    return {
        "target_role": user_state.target_role,
        "extracted_skills": user_state.extracted_skills,
        "current_topic": user_state.current_topic,
        "current_difficulty": user_state.current_difficulty,
        "current_module": user_state.current_module,
        "module_progress": user_state.module_progress,
        "fatigue": user_state.fatigue,
    }

def _fetch_youtube_videos(topic, difficulty, mod_key):
    if not VideosSearch:
        return []
    
    if mod_key == "intro":
        query = f"{topic} {difficulty} introduction tutorial"
    elif mod_key == "core":
        query = f"{topic} {difficulty} full course"
    else:
        query = f"{topic} {difficulty} crash course summary"
        
    try:
        search = VideosSearch(query, limit=2)
        results = search.result().get("result", [])
        
        vids = []
        for r in results:
            views_text = r.get("viewCount", {}).get("short", "0 views")
            if views_text:
                views_text = views_text.replace(" views", "").strip()
            else:
                views_text = "0"
            duration = r.get("duration", "0:00")
            title = r.get("title", "")
            url = r.get("link", "")
            channel = r.get("channel", {}).get("name", "")
            thumb = ""
            if r.get("thumbnails"):
                thumb = r["thumbnails"][0].get("url", "")
                
            vids.append({
                "title": title,
                "channel": channel,
                "duration": duration,
                "thumb": thumb,
                "url": url,
                "views": views_text
            })
        return vids
    except Exception as e:
        logging.error(f"YouTube search error for {query}: {e}")
        return []

@router.get("/videos")
async def get_videos(topic: str, difficulty: str, module: str, user_id: int = Depends(get_current_user)):
    all_videos = []
    
    # Dynamically fetch videos for all 3 modules
    for mod_key in ["intro", "core", "summary"]:
        mod_vids = _fetch_youtube_videos(topic, difficulty, mod_key)
        
        # Fallback to hardcoded DB if real-time search fails or is empty
        if not mod_vids:
            topic_videos = VIDEO_DB.get(topic, {})
            diff_videos = topic_videos.get(difficulty, {})
            mod_vids = diff_videos.get(mod_key, [])
            
        for v in mod_vids:
            video_copy = dict(v)
            video_copy["module"] = mod_key
            video_copy["is_current_module"] = (mod_key == module)
            all_videos.append(video_copy)
    
    # Find the "best" video by highest view count, prioritizing the current module
    best_idx = -1
    best_views = -1
    
    def parse_views(v_str):
        try:
            v_str_clean = v_str.replace(",", "").strip()
            if v_str_clean.upper().endswith("M"):
                return float(v_str_clean[:-1]) * 1_000_000
            elif v_str_clean.upper().endswith("K"):
                return float(v_str_clean[:-1]) * 1_000
            return float(v_str_clean)
        except (ValueError, TypeError):
            return 0

    # First pass: look only at current module videos
    for i, v in enumerate(all_videos):
        if not v.get("is_current_module"):
            continue
        num = parse_views(v.get("views", "0"))
        if num > best_views:
            best_views = num
            best_idx = i
            
    # Fallback: if no current module video, pick highest viewed overall
    if best_idx == -1:
        for i, v in enumerate(all_videos):
            num = parse_views(v.get("views", "0"))
            if num > best_views:
                best_views = num
                best_idx = i
    
    if best_idx >= 0:
        all_videos[best_idx]["recommended"] = True
    
    return {"videos": all_videos, "current_module": module}
