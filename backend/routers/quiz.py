import random
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from redis_client import get_session
import models
from data import QUIZ_BANK
# from qgen.cache import load_topic_questions  # Assuming qgen is moved and works

router = APIRouter()

DIFFICULTY_MIX = {
    "beginner":     {"easy": 8, "medium": 5, "hard": 2},
    "intermediate": {"easy": 5, "medium": 6, "hard": 4},
    "advanced":     {"easy": 2, "medium": 5, "hard": 8},
}

async def get_current_user(token: str = Header(...), db: AsyncSession = Depends(get_db)):
    user_id = await get_session(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user_id

@router.get("/generate")
async def generate_quiz(topic: str, difficulty: str, user_id: int = Depends(get_current_user)):
    # In a real scenario, use load_topic_questions(topic) from qgen
    # generated = load_topic_questions(topic)
    generated = []
    
    by_level = {"easy": [], "medium": [], "hard": []}
    for q in (generated if generated else QUIZ_BANK.get(topic, [])):
        by_level.setdefault(q["level"], []).append(q)
        
    mix = DIFFICULTY_MIX.get(difficulty, DIFFICULTY_MIX["intermediate"])
    pool = []
    leftover = []
    for level, want in mix.items():
        available = list(by_level.get(level, []))
        random.shuffle(available)
        pool.extend(available[:want])
        leftover.extend(available[want:])
        
    random.shuffle(leftover)
    target_total = sum(mix.values())
    while len(pool) < target_total and leftover:
        pool.append(leftover.pop())
        
    random.shuffle(pool)
    
    # ── FIX FOR QUIZ BUG: Shuffle options dynamically ──
    processed_pool = []
    for idx, q in enumerate(pool):
        original_opts = q["opts"]
        original_ans_idx = q["ans"]
        
        # Zip options with their original index
        opts_with_idx = list(enumerate(original_opts))
        random.shuffle(opts_with_idx)
        
        shuffled_opts = [opt for _, opt in opts_with_idx]
        # Find where the original answer went
        new_ans_idx = next(i for i, (orig_i, _) in enumerate(opts_with_idx) if orig_i == original_ans_idx)
        
        processed_pool.append({
            "id": idx,
            "q": q["q"],
            "opts": shuffled_opts,
            "ans": new_ans_idx,
            "level": q["level"],
            "explanation": q.get("explanation", "")
        })
        
    return {"questions": processed_pool}
