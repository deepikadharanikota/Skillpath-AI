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
from typing import List, Optional, Dict

try:
    from youtubesearchpython import VideosSearch
except ImportError:
    VideosSearch = None

from dqn_agent import DQNAgent
from environment import STATE_DIM, ACTION_DIM
from recommender import get_initial_recommendation, get_next_recommendation, evaluate_code
from agent_utils import extract_skills_from_text, compute_reward, get_module_status, compute_topic_knowledge
from data import ROLES, ROLE_SKILLS, TOPICS, MODULE_STRUCTURE, MODULE_KEYS, VIDEO_DB
from roles_config import TOPIC_SYLLABUS, get_topic_syllabus, get_role_config, filter_gaps_with_prerequisites

router = APIRouter()

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "../dqn_weights.pkl")
agent = DQNAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM, seed=42)
if os.path.exists(WEIGHTS_PATH):
    try:
        agent.load(WEIGHTS_PATH)
        print(f"[RL Service] Loaded {getattr(agent, 'algorithm_version', 'Dueling Double DQN')} weights from {WEIGHTS_PATH}")
    except Exception as e:
        print(f"[RL Service] Warning loading weights: {e}. Agent initialized with fresh weights.")

@router.get("/agent-status")
async def get_agent_status():
    status_dict = {
        "status": "online",
        "algorithm": getattr(agent, "algorithm_name", "Double DQN"),
        "algorithm_version": getattr(agent, "algorithm_version", "DoubleDQN-v1"),
        "state_dim": agent.state_dim,
        "action_dim": agent.action_dim,
        "epsilon": float(agent.epsilon),
        "train_steps": int(agent._train_steps),
        "replay_buffer_size": len(agent.replay_buffer),
        "replay_buffer_type": "Uniform" if not hasattr(agent.replay_buffer, "beta") else "Prioritized",
    }
    if hasattr(agent.replay_buffer, "beta"):
        status_dict["replay_buffer_beta"] = float(agent.replay_buffer.beta)
    return status_dict

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

    # ── Dashboard: log "started course" activity ──
    from datetime import datetime
    activity = models.LearningActivity(
        user_id=user.id,
        activity_type="started_course",
        title=f"Started learning {topic}",
        description=f"Target role: {payload.target_role}",
        topic=topic,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(activity)

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

    # ── Dashboard tracking: activity log, hours, streak, badges ──
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    now_iso = now.isoformat()
    today_str = now.strftime("%Y-%m-%d")

    # 1. Log activity: module completed
    module_label = MODULE_STRUCTURE.get(module, {}).get("label", module)
    activity = models.LearningActivity(
        user_id=user.id,
        activity_type="completed_module",
        title=f"Completed {module_label} — {topic}",
        description=f"Quiz: {payload.quiz_score}% | Code: {payload.code_score}%",
        topic=topic,
        created_at=now_iso,
    )
    db.add(activity)

    # 2. Check if full topic just completed
    topic_prog = progress.get(topic, {})
    if all(topic_prog.get(m) == "completed" for m in MODULE_KEYS):
        topic_activity = models.LearningActivity(
            user_id=user.id,
            activity_type="completed_skill",
            title=f"Mastered {topic}!",
            description=f"All modules completed for {topic}",
            topic=topic,
            created_at=now_iso,
        )
        db.add(topic_activity)

    # 3. Update learning hours (+0.75 per module)
    user_state.total_learning_hours = (user_state.total_learning_hours or 0) + 0.75

    # 4. Update streak
    last_date = user_state.last_activity_date
    if last_date:
        try:
            last = datetime.strptime(last_date, "%Y-%m-%d").date()
            diff = (now.date() - last).days
            if diff == 1:
                user_state.current_streak = (user_state.current_streak or 0) + 1
            elif diff > 1:
                user_state.current_streak = 1
            # same day: streak unchanged
        except (ValueError, TypeError):
            user_state.current_streak = 1
    else:
        user_state.current_streak = 1
    user_state.last_activity_date = today_str

    # 5. Badge checks
    from routers.dashboard import check_and_award_badges
    from sqlalchemy import func as sa_func

    quiz_count_res = await db.execute(
        select(sa_func.count(models.QuizHistory.id)).filter(models.QuizHistory.user_id == user.id)
    )
    quiz_count = quiz_count_res.scalar() or 0
    new_badges = check_and_award_badges(user_state, quiz_count)

    # High scorer badge (90%+)
    if payload.quiz_score >= 90:
        existing_ids = {b["id"] for b in (user_state.badges or [])}
        if "high_scorer" not in existing_ids:
            new_badges.append({
                "id": "high_scorer",
                "name": "Quiz Champion",
                "icon": "🎯",
                "description": "Scored 90%+ on a quiz",
                "earned_at": now_iso,
            })

    if new_badges:
        all_badges = (user_state.badges or []) + new_badges
        user_state.badges = all_badges
        # Log badge activities
        for badge in new_badges:
            badge_activity = models.LearningActivity(
                user_id=user.id,
                activity_type="earned_badge",
                title=f"Earned: {badge['icon']} {badge['name']}",
                description=badge["description"],
                topic=None,
                created_at=now_iso,
            )
            db.add(badge_activity)

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

    # Feed transition into Dueling Double DQN + PER buffer
    try:
        from environment import build_state, encode_action
        prev_scores = [h["quizScore"] for h in recent_history[:-1][-3:]]
        s_prev = build_state(topic_mastery, prev_scores, user_state.fatigue)
        s_next = np.array(rec["state"])
        action_idx = rec["encoded_action"]
        is_done = bool(all(progress.get(topic, {}).get(m) == "completed" for m in MODULE_KEYS))
        agent.remember(s_prev, action_idx, reward, s_next, is_done)
        if len(agent.replay_buffer) >= agent.batch_size:
            agent.replay()
    except Exception as rl_err:
        pass
    
    return {"reward": reward, "next_recommendation": rec}

def calculate_course_progress(topic: str, user_state: Optional[models.UserState]) -> dict:
    if not user_state or not topic:
        return {
            "percentage": 0,
            "completed_modules": 0,
            "total_modules": len(MODULE_KEYS),
            "is_completed": False,
            "active_module": "intro",
            "completed_videos_count": 0,
            "total_videos_count": 6
        }

    progress = user_state.module_progress or {}
    topic_prog = progress.get(topic, {})
    
    completed_mods = sum(1 for m in MODULE_KEYS if topic_prog.get(m) == "completed")
    
    vid_prog = (user_state.video_progress or {}).get(topic, {})
    total_completed_vids = sum(len(vid_prog.get(m, [])) for m in MODULE_KEYS)
    
    # 4 modules total (25% each)
    percentage = completed_mods * 25
    
    active_mod = "intro"
    for m in MODULE_KEYS:
        if topic_prog.get(m) != "completed":
            active_mod = m
            break
            
    if completed_mods < len(MODULE_KEYS):
        req_vids = 2 if active_mod in ("core", "advanced") else 1
        active_vids = len(vid_prog.get(active_mod, []))
        partial = min(20, int((active_vids / req_vids) * 20)) if req_vids > 0 else 0
        percentage = min(99, percentage + partial)

    is_complete = (completed_mods == len(MODULE_KEYS))
    if is_complete:
        percentage = 100

    return {
        "percentage": percentage,
        "completed_modules": completed_mods,
        "total_modules": len(MODULE_KEYS),
        "is_completed": is_complete,
        "active_module": active_mod,
        "completed_videos_count": total_completed_vids,
        "total_videos_count": 6
    }

class PositionPayload(BaseModel):
    topic: str
    module: str
    video_id: str
    video_title: Optional[str] = ""
    position_seconds: float

@router.post("/position")
async def save_learning_position(
    payload: PositionPayload,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Saves playback progress, video id, title, and timestamp for exact continuation."""
    from datetime import datetime
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    if not user_state:
        user_state = models.UserState(user_id=user.id)
        db.add(user_state)

    user_state.current_topic = payload.topic
    user_state.current_module = payload.module
    user_state.last_video_id = payload.video_id
    if payload.video_title:
        user_state.last_video_title = payload.video_title
    user_state.last_video_position_seconds = payload.position_seconds
    user_state.last_accessed_at = datetime.utcnow().isoformat()

    await db.commit()
    prog = calculate_course_progress(payload.topic, user_state)

    return {
        "success": True,
        "topic": payload.topic,
        "module": payload.module,
        "video_id": payload.video_id,
        "video_title": user_state.last_video_title,
        "position_seconds": payload.position_seconds,
        "last_accessed_at": user_state.last_accessed_at,
        "course_progress": prog
    }

@router.get("/resume")
async def get_learning_resume(
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns:
    1. Priority 1 Continuation: Active course with exact video and position if unfinished.
    2. Next Recommended Course: Prerequisite-aware recommendation with dynamic rationale.
    3. Learning Path: Full roadmap for user's target role.
    4. All Topics: Catalog of all available topics with status.
    """
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()

    target_role = (user_state.target_role if user_state else None) or "DevOps Engineer"
    role_conf = get_role_config(target_role)
    roadmap = role_conf.get("roadmap", [])
    extracted_skills = user_state.extracted_skills or [] if user_state else []
    extracted_skills_lower = {s.lower().strip() for s in extracted_skills}

    current_topic = user_state.current_topic if user_state else None
    current_prog = calculate_course_progress(current_topic, user_state) if current_topic else None

    # Fetch user quizzes to evaluate mastery and difficulty
    quiz_res = await db.execute(select(models.QuizHistory).filter(models.QuizHistory.user_id == user.id))
    quizzes = quiz_res.scalars().all()
    topic_quiz_scores = {}
    for q in quizzes:
        topic_quiz_scores.setdefault(q.topic, []).append(q.quiz_score)
    avg_scores = {t: round(sum(scores) / len(scores), 1) for t, scores in topic_quiz_scores.items()}

    # Completed topics
    completed_topics = []
    if user_state:
        for t in TOPICS:
            if calculate_course_progress(t, user_state)["is_completed"]:
                completed_topics.append(t)

    # Priority 1: Current course continuation
    continue_course = None
    if current_topic and current_prog and not current_prog["is_completed"]:
        active_mod = user_state.current_module or current_prog["active_module"]
        v_title = user_state.last_video_title or f"{current_topic} - Module {active_mod.capitalize()}"
        pos_sec = float(user_state.last_video_position_seconds or 0.0)
        
        continue_course = {
            "topic": current_topic,
            "title": f"Continue {current_topic}",
            "current_module": active_mod,
            "video_id": user_state.last_video_id or "",
            "video_title": v_title,
            "position_seconds": pos_sec,
            "formatted_position": f"{int(pos_sec // 60):02d}:{int(pos_sec % 60):02d}",
            "progress": current_prog,
            "difficulty": user_state.current_difficulty or "beginner",
            "last_accessed_at": user_state.last_accessed_at,
            "action_url": f"/learning/{current_topic}?module={active_mod}&video={user_state.last_video_id or ''}&t={int(pos_sec)}",
            "syllabus": TOPIC_SYLLABUS.get(current_topic)
        }

    # Next Recommended Course
    next_candidate = None
    next_rationale = ""
    next_difficulty = "intermediate"

    for milestone in roadmap:
        t = milestone["topic"]
        t_lower = t.lower().strip()

        # Skip if it is the current unfinished course
        if continue_course and t == current_topic:
            continue

        # Skip if already completed
        if t in completed_topics:
            continue

        # Skip if already present in resume (unless score on quiz was poor < 60)
        is_in_resume = (t_lower in extracted_skills_lower) or any(t_lower in s for s in extracted_skills_lower)
        if is_in_resume and avg_scores.get(t, 100) >= 60:
            continue

        # Check prerequisites
        prereqs = milestone.get("prerequisites", [])
        unmet = [
            p for p in prereqs 
            if p not in completed_topics 
            and (p.lower().strip() not in extracted_skills_lower and not any(p.lower().strip() in s for s in extracted_skills_lower))
        ]

        if not unmet:
            # Satisfied all prerequisites!
            next_candidate = milestone
            if current_topic and current_prog and current_prog["is_completed"]:
                next_rationale = f"Because you've mastered {current_topic}, {t} is the logical next progression in your {target_role} roadmap."
            elif prereqs:
                next_rationale = f"With prerequisites in {', '.join(prereqs)} satisfied, {t} is your highest-priority next skill for {target_role}."
            elif is_in_resume:
                next_rationale = f"Your quiz score indicates {t} could use a refresher to meet full {target_role} standards."
            else:
                next_rationale = f"Foundational milestone for {target_role}: {milestone.get('description', '')}"

            if avg_scores.get(current_topic, 70) >= 85:
                next_difficulty = "advanced"
            elif avg_scores.get(current_topic, 70) < 60:
                next_difficulty = "beginner"
            else:
                next_difficulty = "intermediate"

            break
        else:
            # Recommend the first unmet prerequisite topic if it's a valid topic
            for p in unmet:
                if p in TOPICS and p not in completed_topics:
                    next_candidate = {
                        "topic": p,
                        "title": f"Learn {p} (Prerequisite)",
                        "description": f"Essential foundation required before learning {t} for {target_role}."
                    }
                    next_rationale = f"Required prerequisite: Master {p} before unlocking {t} on your {target_role} journey."
                    next_difficulty = "beginner"
                    break
            if next_candidate:
                break

    if not next_candidate:
        for t in TOPICS:
            if t not in completed_topics and (not continue_course or t != current_topic):
                next_candidate = {
                    "topic": t,
                    "title": f"Explore {t}",
                    "description": f"Broaden your expertise with {t}."
                }
                next_rationale = f"Expand your technical horizon with {t}."
                break

    next_course = None
    if next_candidate:
        cand_topic = next_candidate["topic"]
        next_course = {
            "topic": cand_topic,
            "title": next_candidate.get("title", f"Master {cand_topic}"),
            "description": next_candidate.get("description", f"Core skill for {target_role}"),
            "rationale": next_rationale or f"Key skill for your {target_role} path.",
            "target_role": target_role,
            "difficulty": next_difficulty,
            "target_module": "intro",
            "action_url": f"/learning/{cand_topic}?module=intro",
            "syllabus": TOPIC_SYLLABUS.get(cand_topic)
        }

    learning_path = []
    for milestone in roadmap:
        t = milestone["topic"]
        t_lower = t.lower().strip()
        t_prog = calculate_course_progress(t, user_state)
        
        is_completed = t_prog["is_completed"]
        is_in_resume = (t_lower in extracted_skills_lower) or any(t_lower in s for s in extracted_skills_lower)
        is_current = (current_topic == t and not is_completed)
        is_next = (next_course and next_course["topic"] == t)

        prereqs = milestone.get("prerequisites", [])
        unmet = [
            p for p in prereqs 
            if p not in completed_topics 
            and (p.lower().strip() not in extracted_skills_lower and not any(p.lower().strip() in s for s in extracted_skills_lower))
        ]

        if is_completed:
            status = "completed"
            action_label = "Review Course"
        elif is_current:
            status = "in_progress"
            action_label = "Continue Learning"
        elif is_next:
            status = "next_recommended"
            action_label = "Start Next Course"
        elif is_in_resume:
            status = "mastered_via_resume"
            action_label = "Review Advanced"
        elif len(unmet) > 0:
            status = "locked"
            action_label = f"Requires {', '.join(unmet)}"
        else:
            status = "ready_to_learn"
            action_label = "Start Course"

        learning_path.append({
            "topic": t,
            "title": milestone.get("title", t),
            "description": milestone.get("description", ""),
            "prerequisites": prereqs,
            "unmet_prerequisites": unmet,
            "progress": t_prog,
            "status": status,
            "action_label": action_label,
            "target_module": t_prog["active_module"],
            "navigate_url": f"/learning/{t}?module={t_prog['active_module']}",
            "syllabus": TOPIC_SYLLABUS.get(t)
        })

    all_topics_catalog = []
    for t in TOPICS:
        t_prog = calculate_course_progress(t, user_state)
        syl = TOPIC_SYLLABUS.get(t, {})
        all_topics_catalog.append({
            "topic": t,
            "title": syl.get("title", t),
            "description": syl.get("description", f"{t} curriculum"),
            "progress": t_prog,
            "is_current": (current_topic == t),
            "navigate_url": f"/learning/{t}?module={t_prog['active_module']}",
            "modules_count": len(MODULE_KEYS)
        })

    return {
        "target_role": target_role,
        "continue_course": continue_course,
        "next_course": next_course,
        "learning_path": learning_path,
        "all_topics": all_topics_catalog
    }

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
        "video_progress": user_state.video_progress or {},
        "topic_ability": user_state.topic_ability or {},
        "fatigue": user_state.fatigue,
        "resume_filename": user_state.resume_filename,
        "last_video_id": user_state.last_video_id,
        "last_video_title": user_state.last_video_title,
        "last_video_position_seconds": user_state.last_video_position_seconds or 0.0,
        "last_accessed_at": user_state.last_accessed_at,
    }

class NavigatePayload(BaseModel):
    topic: str
    module: Optional[str] = "intro"

@router.post("/navigate")
async def navigate_topic(
    payload: NavigatePayload,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Direct navigation from dashboard to a specific topic and module."""
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    if not user_state:
        user_state = models.UserState(user_id=user.id)
        db.add(user_state)

    topic = payload.topic if payload.topic in TOPICS else "Machine Learning"
    user_state.current_topic = topic

    prog = dict(user_state.module_progress or {})
    if topic not in prog:
        prog[topic] = {"intro": "active", "core": "locked", "summary": "locked"}

    requested_mod = payload.module if payload.module in MODULE_KEYS else "intro"
    if prog[topic].get(requested_mod) == "locked":
        prog[topic][requested_mod] = "active"
    user_state.current_module = requested_mod
    user_state.module_progress = prog

    # Adaptive video level
    ability_map = user_state.topic_ability or {}
    topic_ability = ability_map.get(topic, {})
    if topic_ability.get("videoLevel"):
        user_state.current_difficulty = topic_ability.get("videoLevel")

    await db.commit()
    return {
        "success": True,
        "current_topic": user_state.current_topic,
        "current_module": user_state.current_module,
        "current_difficulty": user_state.current_difficulty,
        "module_progress": user_state.module_progress
    }

class VideoCompletePayload(BaseModel):
    topic: str
    module: str
    video_id: str

@router.post("/video/complete")
async def complete_video(
    payload: VideoCompletePayload,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Marks a video as completed in the database and computes quiz unlock status."""
    from datetime import datetime
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()
    if not user_state:
        raise HTTPException(status_code=404, detail="User state not found")

    video_prog = dict(user_state.video_progress or {})
    topic_prog = dict(video_prog.get(payload.topic, {}))
    mod_vids = list(topic_prog.get(payload.module, []))

    if payload.video_id not in mod_vids:
        mod_vids.append(payload.video_id)
        topic_prog[payload.module] = mod_vids
        video_prog[payload.topic] = topic_prog
        user_state.video_progress = video_prog

        act = models.LearningActivity(
            user_id=user.id,
            activity_type="completed_video",
            title=f"Watched {payload.topic} video",
            description=f"Completed video in {payload.module.capitalize()} module",
            topic=payload.topic,
            created_at=datetime.utcnow().isoformat()
        )
        db.add(act)
    user_state.last_accessed_at = datetime.utcnow().isoformat()
    if user_state.last_video_id == payload.video_id:
        user_state.last_video_position_seconds = 0.0
    await db.commit()

    required_count = 2 if payload.module in ("core", "advanced") else 1
    completed_count = len(mod_vids)
    is_quiz_unlocked = completed_count >= required_count
    prog = calculate_course_progress(payload.topic, user_state)

    return {
        "success": True,
        "completed_videos": mod_vids,
        "completed_count": completed_count,
        "required_count": required_count,
        "is_quiz_unlocked": is_quiz_unlocked,
        "course_progress": prog
    }

def _fetch_youtube_videos(topic, difficulty, mod_key):
    if not VideosSearch:
        return []

    # Check if topic has custom syllabus with specific subtopics
    syl = TOPIC_SYLLABUS.get(topic, {}).get("modules", {}).get(mod_key, {})
    focus_topic = syl.get("focus") or ""
    subtopics = syl.get("subtopics") or []
    sub_query = subtopics[0] if subtopics else ""

    if mod_key == "intro":
        query = f"{topic} {sub_query or 'introduction fundamentals'} tutorial {difficulty}".strip()
    elif mod_key == "core":
        query = f"{topic} {sub_query or 'core concepts deep dive'} course {difficulty}".strip()
    elif mod_key == "advanced":
        query = f"{topic} {sub_query or 'advanced architecture'} tutorial {difficulty}".strip()
    else:
        query = f"{topic} {sub_query or 'production deployment project'} review {difficulty}".strip()

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

def _parse_views(v_str):
    try:
        v_str_clean = str(v_str).replace(",", "").strip()
        if v_str_clean.upper().endswith("M"):
            return float(v_str_clean[:-1]) * 1_000_000
        elif v_str_clean.upper().endswith("K"):
            return float(v_str_clean[:-1]) * 1_000
        return float(v_str_clean)
    except (ValueError, TypeError):
        return 0

@router.get("/videos")
async def get_videos(
    topic: str,
    difficulty: Optional[str] = None,
    module: str = "intro",
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.UserState).filter(models.UserState.user_id == user.id))
    user_state = result.scalars().first()

    # Adaptive video level from user_state topic_ability
    effective_difficulty = difficulty
    if not effective_difficulty and user_state:
        ability_info = (user_state.topic_ability or {}).get(topic, {})
        effective_difficulty = ability_info.get("videoLevel", user_state.current_difficulty or "beginner")
    if not effective_difficulty:
        effective_difficulty = "beginner"

    all_videos = []

    # Dynamically fetch videos for all modules in MODULE_KEYS
    for mod_key in MODULE_KEYS:
        mod_vids = _fetch_youtube_videos(topic, effective_difficulty, mod_key)
        if not mod_vids:
            topic_videos = VIDEO_DB.get(topic, {})
            diff_videos = topic_videos.get(effective_difficulty, topic_videos.get("beginner", {}))
            mod_vids = diff_videos.get(mod_key, [])

        for idx, v in enumerate(mod_vids):
            video_copy = dict(v)
            video_id = video_copy.get("url") or f"{topic}_{mod_key}_{idx}"
            video_copy["id"] = video_id
            video_copy["module"] = mod_key
            video_copy["is_current_module"] = (mod_key == module)

            # Check if video was marked complete by user
            user_mod_vids = (user_state.video_progress or {}).get(topic, {}).get(mod_key, []) if user_state else []
            video_copy["is_completed"] = (video_id in user_mod_vids) or (video_copy.get("url") in user_mod_vids)
            all_videos.append(video_copy)

    # Calculate module completion and quiz lock status
    current_mod_vids = [v for v in all_videos if v.get("module") == module]
    required_count = 2 if module in ("core", "advanced") else 1
    if 0 < len(current_mod_vids) < required_count:
        required_count = len(current_mod_vids)
    completed_count = sum(1 for v in current_mod_vids if v.get("is_completed"))
    is_quiz_unlocked = (completed_count >= required_count) if required_count > 0 else False

    # Find the "best" video by highest view count
    best_idx = -1
    best_views = -1
    for i, v in enumerate(all_videos):
        if not v.get("is_current_module"):
            continue
        num = _parse_views(v.get("views", "0"))
        if num > best_views:
            best_views = num
            best_idx = i

    if best_idx == -1 and all_videos:
        best_idx = 0

    if best_idx >= 0 and best_idx < len(all_videos):
        all_videos[best_idx]["recommended"] = True

    # Retrieve syllabus breakdown for this topic
    syllabus_info = TOPIC_SYLLABUS.get(topic)

    # Course progress and continuation metadata
    course_prog = calculate_course_progress(topic, user_state)
    is_same_topic = (user_state and user_state.current_topic == topic)

    return {
        "videos": all_videos,
        "current_module": module,
        "current_difficulty": effective_difficulty,
        "completed_count": completed_count,
        "required_count": required_count,
        "is_quiz_unlocked": is_quiz_unlocked,
        "syllabus": syllabus_info,
        "course_progress": course_prog,
        "last_video_id": user_state.last_video_id if is_same_topic and user_state else None,
        "last_video_position_seconds": user_state.last_video_position_seconds if is_same_topic and user_state else 0.0,
        "last_video_title": user_state.last_video_title if is_same_topic and user_state else None,
    }
