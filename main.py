"""
main.py
-------
SkillPath AI — a fully Python application.

This is the single entry point for the whole project. It replaces the
old React/JavaScript frontend (`my-app/`) with a Streamlit UI that talks
directly, in-process, to the same real RL core (`dqn_agent.py` +
`environment.py`) that used to be served over HTTP for the React app to
consume. There is no JavaScript, no Node, and no browser-side code
anywhere in this project anymore — every screen, every piece of state,
and every decision is plain Python.

Run:
    pip install -r requirements.txt
    streamlit run main.py
"""

import os
import random
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from data import (
    ROLES, ROLE_SKILLS, TOPICS, DIFFICULTIES,
    MODULE_STRUCTURE, MODULE_KEYS, VIDEO_DB, QUIZ_BANK, CODE_PROMPTS,
)
from agent_utils import (
    extract_skills_from_text, compute_reward, adapt_difficulty,
    get_module_status, compute_topic_knowledge,
)
from recommender import get_initial_recommendation, get_next_recommendation, evaluate_code
from dqn_agent import DQNAgent
from environment import STATE_DIM, ACTION_DIM, build_state
from qgen.cache import load_topic_questions

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "dqn_weights.pkl")

QUIZ_SECONDS_PER_QUESTION = 40  # each question auto-advances to the next one after this many seconds

STAGE_UPLOAD = "upload"
STAGE_DASHBOARD = "dashboard"
STAGE_LEARNING = "learning"
STAGE_QUIZ = "quiz"
STAGE_RESULTS = "results"


# ─────────────────────────────────────────────────────────────────────────
# Page setup & theme (mirrors the old UIComponents.jsx color palette)
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="SkillPath AI", page_icon="🎓", layout="centered")

COLORS = {
    "bg": "#080d18", "surf": "#0f1623", "card": "#151e2e", "border": "#1e2d45",
    "accent": "#6366f1", "cyan": "#06b6d4", "green": "#10b981",
    "amber": "#f59e0b", "red": "#ef4444", "purple": "#8b5cf6",
    "text": "#e2e8f0", "muted": "#64748b", "dim": "#2d3748",
}

st.markdown(f"""
<style>
.stApp {{ background-color: {COLORS['bg']}; color: {COLORS['text']}; }}
[data-testid="stSidebar"] {{ background-color: {COLORS['surf']}; }}
.sp-card {{
    background: {COLORS['card']}; border: 1px solid {COLORS['border']};
    border-radius: 16px; padding: 20px 24px; margin-bottom: 16px;
}}
.sp-card-highlight {{ border-color: {COLORS['accent']}66; }}
.sp-badge {{
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600; margin-right: 6px; margin-bottom: 6px;
}}
.sp-section-label {{
    font-size: 11px; font-weight: 700; color: {COLORS['muted']};
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;
}}
</style>
""", unsafe_allow_html=True)


def badge(label, color=COLORS["accent"]):
    return (
        f'<span class="sp-badge" style="background:{color}18;color:{color};'
        f'border:1px solid {color}33;">{label}</span>'
    )


def diff_color(d):
    return {"beginner": COLORS["green"], "intermediate": COLORS["amber"], "advanced": COLORS["red"]}[d]


def diff_label(d):
    return {"beginner": "🌱 Beginner", "intermediate": "🔥 Intermediate", "advanced": "⚡ Advanced"}[d]


def card_open(highlight=False):
    cls = "sp-card sp-card-highlight" if highlight else "sp-card"
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def section_label(text):
    st.markdown(f'<div class="sp-section-label">{text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────
# Session state initialization
# ─────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": STAGE_UPLOAD,
        "target_role": "ML Engineer",
        "extracted_skills": [],
        "current_topic": "Machine Learning",
        "current_difficulty": "beginner",
        "current_module": "intro",
        "module_progress": {},
        "quiz_history": [],
        "session_count": 0,
        "fatigue": 0.0,
        "agent_explanation": None,
        "next_rec": None,
        "difficulty_changed": False,
        "pending_state": None,
        "pending_action": None,
        "video_progress": {},        # {video_key: count of videos completed so far in that module}
        "quiz_questions": [],        # the 15 shuffled leveled questions for the current attempt
        "quiz_idx": 0,                # index of the question currently being shown (one-by-one, no skipping)
        "quiz_question_start_time": 0.0,  # wall-clock time the current question was first shown
        "quiz_answers": {},
        "quiz_done": False,
        "quiz_score": 0,
        "code_text": "",
        "code_eval": None,
        "last_quiz_score": 0,
        "last_code_score": 0,
        "last_reward": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if "agent" not in st.session_state:
        agent = DQNAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM, seed=42)
        if os.path.exists(WEIGHTS_PATH):
            try:
                agent.load(WEIGHTS_PATH)
            except Exception:
                pass
        st.session_state["agent"] = agent


init_state()


# ─────────────────────────────────────────────────────────────────────────
# Helpers shared across stages
# ─────────────────────────────────────────────────────────────────────────
def current_topic_mastery():
    """Topic mastery dict derived from quiz history, same shape the old
    App.js built before every recommendation call."""
    mastery = {}
    for t in TOPICS:
        t_hist = [h for h in st.session_state.quiz_history if h["topic"] == t]
        mastery[t] = (
            sum(h["quizScore"] for h in t_hist) / len(t_hist) / 100
            if t_hist else 0.0
        )
    return mastery


def start_learning_journey(resume_text, role):
    skills = extract_skills_from_text(resume_text or "")
    role_skills = ROLE_SKILLS.get(role, [])
    st.session_state.extracted_skills = skills
    st.session_state.target_role = role

    rec = get_initial_recommendation(st.session_state.agent, role, skills, role_skills)
    topic = rec["topic"] if rec["topic"] in TOPICS else "Machine Learning"
    st.session_state.current_topic = topic
    st.session_state.current_difficulty = rec.get("difficulty", "beginner")
    st.session_state.current_module = "intro"
    st.session_state.agent_explanation = rec
    st.session_state.pending_state = rec["state"]
    st.session_state.pending_action = rec["encoded_action"]

    st.session_state.module_progress = {
        topic: {"intro": "active", "core": "locked", "summary": "locked"}
    }
    st.session_state.stage = STAGE_LEARNING


def video_key(topic, difficulty, module):
    return f"{topic}::{difficulty}::{module}"


# How many questions to draw from each difficulty level, based on the
# learner's current adaptive difficulty (set by adapt_difficulty()/the DQN
# from past quiz scores — see submit_module_results() below). This is what
# makes question *composition within a quiz* adapt to performance, on top
# of the existing topic/difficulty recommendation that already adapts
# between quizzes.
DIFFICULTY_MIX = {
    "beginner":     {"easy": 8, "medium": 5, "hard": 2},
    "intermediate": {"easy": 5, "medium": 6, "hard": 4},
    "advanced":     {"easy": 2, "medium": 5, "hard": 8},
}


def build_quiz_pool(topic: str, difficulty: str) -> list:
    """Prefers AI-generated questions (from qgen/, built offline from the
    course videos' transcripts via generate_quiz_bank.py). Falls back to
    the static QUIZ_BANK in data.py for any topic that hasn't been
    generated yet, so the app always has a working quiz."""
    generated = load_topic_questions(topic)
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

    # If a level came up short (e.g. a freshly-generated topic doesn't yet
    # have 8 easy questions), backfill from whatever's left so the quiz
    # still has a full question count instead of coming up short.
    random.shuffle(leftover)
    target_total = sum(mix.values())
    while len(pool) < target_total and leftover:
        pool.append(leftover.pop())

    return pool


def go_to_quiz():
    topic = st.session_state.current_topic
    difficulty = st.session_state.current_difficulty
    pool = build_quiz_pool(topic, difficulty)
    random.shuffle(pool)

    st.session_state.quiz_questions = pool
    st.session_state.quiz_idx = 0
    st.session_state.quiz_question_start_time = time.time()
    st.session_state.quiz_answers = {}
    st.session_state.quiz_done = False
    st.session_state.quiz_score = 0
    st.session_state.code_text = ""
    st.session_state.code_eval = None
    st.session_state.stage = STAGE_QUIZ


def submit_module_results(quiz_score, code_score):
    role_skills = ROLE_SKILLS.get(st.session_state.target_role, [])
    topic = st.session_state.current_topic
    module = st.session_state.current_module

    topic_alignment = 1.0 if topic in role_skills else 0.3
    mastery_gain = ((quiz_score + code_score) / 200) * 0.3
    new_fatigue = min(1.0, st.session_state.fatigue + 0.1)

    reward = compute_reward(quiz_score, code_score, mastery_gain, new_fatigue, topic_alignment)
    st.session_state.last_quiz_score = quiz_score
    st.session_state.last_code_score = code_score
    st.session_state.last_reward = reward
    st.session_state.fatigue = new_fatigue

    history_entry = {
        "topic": topic,
        "module": MODULE_STRUCTURE[module]["label"],
        "moduleKey": module,
        "difficulty": st.session_state.current_difficulty,
        "quizScore": quiz_score,
        "codeScore": code_score,
        "reward": round(reward, 3),
    }
    st.session_state.quiz_history = st.session_state.quiz_history + [history_entry]
    st.session_state.session_count += 1

    # Mark module completed / unlock next module in this topic
    progress = dict(st.session_state.module_progress)
    if topic not in progress:
        progress[topic] = {"intro": "locked", "core": "locked", "summary": "locked"}
    else:
        progress[topic] = dict(progress[topic])
    progress[topic][module] = "completed"

    idx = MODULE_KEYS.index(module)
    next_mod = MODULE_KEYS[idx + 1] if idx + 1 < len(MODULE_KEYS) else None
    if next_mod:
        progress[topic][next_mod] = "active"
    st.session_state.module_progress = progress

    # ── Real DQN training step: this is the actual gradient update ──
    topic_mastery = current_topic_mastery()
    next_state = build_state(topic_mastery, [h["quizScore"] for h in st.session_state.quiz_history], new_fatigue)
    if st.session_state.pending_state is not None and st.session_state.pending_action is not None:
        st.session_state.agent.remember(
            st.session_state.pending_state,
            st.session_state.pending_action,
            reward,
            next_state,
            False,
        )
        st.session_state.agent.replay()

    adapted = adapt_difficulty(topic, st.session_state.quiz_history, st.session_state.current_difficulty)
    st.session_state.difficulty_changed = adapted != st.session_state.current_difficulty

    rec = get_next_recommendation(
        st.session_state.agent,
        target_role=st.session_state.target_role,
        completed_topic=topic,
        completed_module=module,
        quiz_score=quiz_score,
        code_score=code_score,
        difficulty=adapted,
        topic_mastery=topic_mastery,
        recent_history=st.session_state.quiz_history[-3:],
        fatigue=new_fatigue,
    )
    st.session_state.next_rec = rec
    st.session_state.pending_state = rec["state"]
    st.session_state.pending_action = rec["encoded_action"]

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
        st.session_state.module_progress = dict(progress)

    st.session_state.current_topic = next_topic
    st.session_state.current_difficulty = rec.get("difficulty", adapted)
    st.session_state.current_module = target_module
    st.session_state.stage = STAGE_RESULTS


# ─────────────────────────────────────────────────────────────────────────
# Top navigation
# ─────────────────────────────────────────────────────────────────────────
def render_nav():
    if st.session_state.stage in (STAGE_UPLOAD, STAGE_QUIZ):
        return
    cols = st.columns([3, 1, 1])
    with cols[0]:
        st.markdown("### 🎓 SkillPath AI")
    with cols[1]:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.stage = STAGE_DASHBOARD
            st.rerun()
    with cols[2]:
        if st.button("📚 Study", use_container_width=True):
            st.session_state.stage = STAGE_LEARNING
            st.rerun()
    st.divider()


# ─────────────────────────────────────────────────────────────────────────
# Stage: Resume upload
# ─────────────────────────────────────────────────────────────────────────
def render_upload():
    st.markdown(
        "<div style='text-align:center;'><div style='font-size:48px;'>🎓</div>"
        "<h1 style='margin-bottom:4px;'>Your Personal Learning Coach</h1>"
        f"<p style='color:{COLORS['muted']};'>Upload your resume and we'll figure out exactly "
        "what to teach you — step by step, at your own pace.</p></div>",
        unsafe_allow_html=True,
    )

    card_open()
    section_label("Step 1 — Paste or upload your resume")
    uploaded = st.file_uploader("Drop a .txt resume file here", type=["txt"])
    resume_text = st.session_state.get("resume_text", "")
    if uploaded is not None:
        resume_text = uploaded.read().decode("utf-8", errors="ignore")

    resume_text = st.text_area(
        "Or paste it below",
        value=resume_text,
        height=160,
        placeholder=(
            "Paste your resume text here...\n\nExample:\nPython developer with 3 years "
            "experience in Machine Learning and Deep Learning.\nWorked with TensorFlow, "
            "PyTorch, NumPy, Pandas...\nBuilt ML models for classification and regression tasks."
        ),
    )
    st.session_state.resume_text = resume_text

    if resume_text.strip():
        preview_skills = extract_skills_from_text(resume_text)
        st.markdown(
            f"✅ **We found {len(preview_skills)} skill(s) in your resume:**  \n"
            + " ".join(badge(s, COLORS["green"]) for s in preview_skills),
            unsafe_allow_html=True,
        )
    card_close()

    card_open()
    section_label("Step 2 — What job are you aiming for?")
    target_role = st.radio("Target role", ROLES, index=ROLES.index(st.session_state.target_role),
                            horizontal=False, label_visibility="collapsed")
    st.session_state.target_role = target_role
    st.markdown(
        f"Skills needed for **{target_role}**:  \n"
        + " ".join(badge(s, COLORS["cyan"]) for s in ROLE_SKILLS.get(target_role, [])),
        unsafe_allow_html=True,
    )
    card_close()

    if st.button("🚀 Start My Learning Journey", type="primary", use_container_width=True):
        with st.spinner("Reading your resume and figuring out what to teach you first..."):
            start_learning_journey(resume_text, target_role)
        st.rerun()
    st.caption("No resume? That's fine — just click the button and we'll use sensible defaults to get you started.")


# ─────────────────────────────────────────────────────────────────────────
# Stage: Learning module (videos)
# ─────────────────────────────────────────────────────────────────────────
def render_learning():
    exp = st.session_state.agent_explanation
    if exp:
        card_open()
        st.markdown(f"**🤖 Your Learning Coach says:**  \n"
                     f"<span style='color:{COLORS['muted']};font-size:13px;'>{exp.get('explanation', '')}</span>",
                     unsafe_allow_html=True)
        card_close()

    topic = st.session_state.current_topic
    difficulty = st.session_state.current_difficulty
    module_key = st.session_state.current_module
    mod_info = MODULE_STRUCTURE[module_key]

    module_context = {
        "intro": {"focus": "big picture concepts and why this subject matters",
                  "tip": "Don't worry about memorizing everything — just get comfortable with the ideas."},
        "core": {"focus": "the most important tools and techniques",
                 "tip": "Try to follow along with the videos and take notes as you go."},
        "summary": {"focus": "connecting all the concepts together",
                    "tip": "Think about how everything links up — this prepares you for the quiz."},
    }
    ctx = module_context[module_key]

    card_open(highlight=True)
    st.markdown(
        f"<div style='font-size:36px;'>{mod_info['icon']}</div>"
        + badge(topic, COLORS["accent"]) + badge(diff_label(difficulty), diff_color(difficulty))
        + badge(mod_info["label"], COLORS["cyan"]),
        unsafe_allow_html=True,
    )
    st.markdown(f"## {topic} — {mod_info['label']}")
    st.markdown(f"In this module, you'll focus on **{ctx['focus']}**.")
    st.info(f"💡 Tip: {ctx['tip']}")
    card_close()

    card_open()
    section_label("📺 Watch these videos — in order")
    st.caption("Videos unlock one at a time. Finish the current video and mark it watched to "
               "unlock the next one — you can't skip ahead.")

    videos = (
        VIDEO_DB.get(topic, {}).get(difficulty, {}).get(module_key)
        or VIDEO_DB.get(topic, {}).get("beginner", {}).get(module_key, [])
    )
    vkey = video_key(topic, difficulty, module_key)
    completed_count = st.session_state.video_progress.get(vkey, 0)

    for i, v in enumerate(videos):
        if i < completed_count:
            # Already watched — shown compact, with a checkmark
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;padding:8px 0;'>"
                f"<span style='font-size:18px;'>✅</span>"
                f"<span style='color:{COLORS['muted']};text-decoration:line-through;'>{v['title']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        elif i == completed_count:
            # The current, unlocked video
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(v["thumb"], use_container_width=True)
            with cols[1]:
                st.markdown(f"**▶ Now playing — {v['title']}**")
                st.caption(f"{v['channel']} · {v['views']} views · {v['duration']}")
                st.markdown(f"[▶ Watch on YouTube]({v['url']})")
                if st.button(f"✅ I've watched this — Unlock Next", key=f"watch_{vkey}_{i}"):
                    progress = dict(st.session_state.video_progress)
                    progress[vkey] = i + 1
                    st.session_state.video_progress = progress
                    st.rerun()
        else:
            # Locked — not reachable until earlier videos are marked watched
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;padding:8px 0;opacity:0.45;'>"
                f"<span style='font-size:18px;'>🔒</span>"
                f"<span>{v['title']}</span>"
                f"<span style='font-size:11px;color:{COLORS['muted']};'>(watch the video above first)</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown("---")
    card_close()

    all_watched = completed_count >= len(videos)

    card_open()
    if all_watched:
        st.markdown("### ✋ Done watching? Let's test your knowledge!")
        st.caption("You've finished every video in this module. When you're ready, take the quiz.")
    else:
        st.markdown("### 🔒 Quiz locked")
        st.caption(f"Watch all {len(videos)} videos in this module ({completed_count}/{len(videos)} done) "
                   "to unlock the quiz.")
    if st.button("📝 I'm Ready — Take the Quiz", type="primary", use_container_width=True, disabled=not all_watched):
        with st.spinner("Preparing your quiz..."):
            go_to_quiz()
        st.rerun()
    card_close()


# ─────────────────────────────────────────────────────────────────────────
# Stage: Quiz
# ─────────────────────────────────────────────────────────────────────────
LEVEL_COLOR = {"easy": "green", "medium": "amber", "hard": "red"}
LEVEL_LABEL = {"easy": "🟢 Easy", "medium": "🟠 Medium", "hard": "🔴 Hard"}


def render_quiz_timer(seconds_left):
    """Purely visual live countdown (independent JS ticking clock — no
    extra packages, built on Streamlit's own components.html). The real
    enforcement of the 40s-per-question auto-advance happens server-side
    in Python below (via st_autorefresh); this is just so the countdown
    doesn't feel like a frozen screen between server ticks."""
    import streamlit.components.v1 as components
    start = max(0, int(round(seconds_left)))
    color = "#10b981" if start > 20 else "#f59e0b" if start > 10 else "#ef4444"
    components.html(
        f"""
        <div style="font-family:inherit;">
          <div id="sp-timer" style="font-size:26px;font-weight:800;color:{color};">
            {start}s
          </div>
          <div style="font-size:11px;color:#64748b;">time left to answer this question</div>
        </div>
        <script>
          let remaining = {start};
          const el = document.getElementById('sp-timer');
          const timer = setInterval(() => {{
            remaining -= 1;
            if (remaining <= 10) {{ el.style.color = '#ef4444'; }}
            else if (remaining <= 20) {{ el.style.color = '#f59e0b'; }}
            if (remaining <= 0) {{
              el.innerText = "0s";
              clearInterval(timer);
            }} else {{
              el.innerText = remaining + 's';
            }}
          }}, 1000);
        </script>
        """,
        height=55,
    )


def render_quiz():
    topic = st.session_state.current_topic
    difficulty = st.session_state.current_difficulty
    module_key = st.session_state.current_module
    module_label = MODULE_STRUCTURE[module_key]["label"]

    questions = st.session_state.quiz_questions
    total = len(questions)
    code_prompt = CODE_PROMPTS.get(topic, {}).get(
        module_key, f"Write a {topic} code snippet demonstrating what you learned in the {module_label} module."
    )

    st.markdown(
        "<div style='text-align:center;'>"
        + badge(topic, COLORS["accent"]) + badge(diff_label(difficulty), diff_color(difficulty))
        + badge(f"📝 {module_label} Quiz", COLORS["cyan"])
        + "<h2>Test Your Knowledge</h2>"
        + f"<p>{total} questions — 5 easy, 5 medium, 5 hard. Answer them one at a time; "
          "no skipping, no going back.</p></div>",
        unsafe_allow_html=True,
    )

    # ── One-by-one, timed, no-skip question flow ──
    if not st.session_state.quiz_done:
        idx = st.session_state.quiz_idx
        q = questions[idx]

        def advance(chosen_option_index):
            """Record the answer (None if unanswered) for the current
            question and move on to the next one, or finish the quiz if
            this was the last question. Shared by both the Submit button
            and the 40s auto-advance timeout below."""
            answers = dict(st.session_state.quiz_answers)
            answers[idx] = chosen_option_index
            st.session_state.quiz_answers = answers

            if idx + 1 >= total:
                correct = sum(
                    1 for i, qq in enumerate(questions)
                    if st.session_state.quiz_answers.get(i) == qq["ans"]
                )
                st.session_state.quiz_score = round((correct / total) * 100) if total else 0
                st.session_state.quiz_done = True
            else:
                st.session_state.quiz_idx = idx + 1
                st.session_state.quiz_question_start_time = time.time()
            st.rerun()

        card_open(highlight=True)
        st.progress((idx) / total, text=f"Question {idx + 1} of {total}")
        st.markdown(badge(LEVEL_LABEL[q["level"]], COLORS[LEVEL_COLOR[q["level"]]]), unsafe_allow_html=True)
        st.markdown(f"### {q['q']}")

        selected_key = f"quiz_option_{idx}"
        selected = st.radio(
            "answer", q["opts"], index=None, key=selected_key, label_visibility="collapsed",
        )

        elapsed = time.time() - st.session_state.quiz_question_start_time
        remaining = max(0.0, QUIZ_SECONDS_PER_QUESTION - elapsed)

        render_quiz_timer(remaining)

        # Tick the server every second while this question is on screen, so
        # the 40s cutoff is enforced even if the candidate never clicks
        # anything. Keyed per-question so the refresh counter resets cleanly
        # when we move to the next question.
        st_autorefresh(interval=1000, key=f"quiz_autorefresh_{idx}")

        if remaining <= 0:
            # Time's up — auto-advance with whatever (if anything) was selected.
            chosen = q["opts"].index(selected) if selected is not None else None
            advance(chosen)

        if st.button("Submit", type="primary", disabled=selected is None, use_container_width=True):
            advance(q["opts"].index(selected))

        if selected is None:
            st.caption("Select an answer, then click Submit. If time runs out, we'll move on automatically.")
        card_close()
        return  # nothing else renders until the quiz is fully done

    # ── Quiz finished: score + full review ──
    score = st.session_state.quiz_score
    color = COLORS["green"] if score >= 80 else COLORS["amber"] if score >= 50 else COLORS["red"]
    msg = ("🎉 Excellent! You've got this!" if score >= 80 else
           "👍 Good effort! Keep going!" if score >= 50 else "💪 Keep practicing — you'll get there!")

    card_open()
    st.markdown(f"<div style='text-align:center;'><span style='font-size:32px;font-weight:900;color:{color};'>"
                 f"{score}%</span><br>{msg}</div>", unsafe_allow_html=True)
    card_close()

    card_open()
    section_label(f"Review — all {total} questions")
    for qi, q in enumerate(questions):
        chosen = st.session_state.quiz_answers.get(qi)
        st.markdown(badge(LEVEL_LABEL[q["level"]], COLORS[LEVEL_COLOR[q["level"]]]), unsafe_allow_html=True)
        st.markdown(f"**{qi + 1}. {q['q']}**")
        if chosen == q["ans"]:
            st.success(f"✅ Correct: {q['opts'][q['ans']]}")
        else:
            st.error(f"❌ You chose: {q['opts'][chosen] if chosen is not None else '—'} · "
                     f"Correct: {q['opts'][q['ans']]}")
        if q.get("explanation"):
            st.caption(f"💡 {q['explanation']}")
        st.markdown("")
    card_close()

    card_open()
    section_label("💻 Coding Challenge")
    st.markdown(f"**Your task:** {code_prompt}")
    code = st.text_area(
        "code", value=st.session_state.code_text, height=180,
        placeholder=f"# Write your {topic} code here\n# Don't worry about it being perfect — just give it a try!",
        label_visibility="collapsed",
    )
    st.session_state.code_text = code

    cols = st.columns([1, 2])
    with cols[0]:
        if st.button("Check My Code", disabled=not code.strip()):
            st.session_state.code_eval = evaluate_code(code, topic, difficulty, module_key)
            st.rerun()
    with cols[1]:
        ev = st.session_state.code_eval
        if ev:
            st.markdown(f"**{ev['score']}% Code Score**  \n{ev['feedback']}")
            if ev.get("strengths"):
                st.caption(f"✅ {ev['strengths']}")
            if ev.get("improvements"):
                st.caption(f"💡 {ev['improvements']}")
    if not code.strip():
        st.caption("The coding challenge is optional, but it really helps! Give it a try. 😊")
    card_close()

    if st.button("✅ Complete This Module", type="primary", use_container_width=True):
        with st.spinner("Saving your results and preparing what's next..."):
            code_score = st.session_state.code_eval["score"] if st.session_state.code_eval else 0
            submit_module_results(st.session_state.quiz_score, code_score)
        st.rerun()
    st.caption(
        "Your results will be saved and we'll prepare your next lesson."
        if st.session_state.code_eval else
        "You can skip the code challenge and just submit your quiz."
    )


# ─────────────────────────────────────────────────────────────────────────
# Stage: Results
# ─────────────────────────────────────────────────────────────────────────
def render_results():
    quiz_score = st.session_state.last_quiz_score
    code_score = st.session_state.last_code_score
    reward = st.session_state.last_reward
    completed_topic = None  # topic already advanced; look at quiz_history
    last_entry = st.session_state.quiz_history[-1]
    completed_topic = last_entry["topic"]
    completed_module_key = last_entry["moduleKey"]
    mod_info = MODULE_STRUCTURE[completed_module_key]

    idx = MODULE_KEYS.index(completed_module_key)
    next_mod = MODULE_KEYS[idx + 1] if idx + 1 < len(MODULE_KEYS) else None
    next_mod_info = MODULE_STRUCTURE[next_mod] if next_mod else None
    topic_complete = next_mod is None

    performance_msg = (
        "🎉 Outstanding! You really nailed it!" if quiz_score >= 80 else
        "👍 Good job! You're making solid progress." if quiz_score >= 60 else
        "💪 Keep at it — every session makes you stronger."
    )
    emoji = "🏆" if quiz_score >= 80 else "⭐" if quiz_score >= 60 else "💪"

    st.markdown(
        f"<div style='text-align:center;'><div style='font-size:48px;'>{emoji}</div>"
        + badge(f"{completed_topic} — {mod_info['label']}", COLORS["accent"])
        + badge("Module Complete!", COLORS["green"])
        + f"<h2>{performance_msg}</h2><p>Here's how you did this session</p></div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    cols[0].metric("📝 Quiz Score", f"{quiz_score}%")
    cols[1].metric("💻 Code Score", f"{code_score}%" if code_score > 0 else "Skipped")
    cols[2].metric("📈 Progress Boost", f"{'+' if reward > 0 else ''}{reward * 100:.0f}")

    card_open()
    section_label(f"Your progress through {completed_topic}")
    cols = st.columns(len(MODULE_KEYS))
    for i, mk in enumerate(MODULE_KEYS):
        is_completed = MODULE_KEYS.index(completed_module_key) >= i
        info = MODULE_STRUCTURE[mk]
        with cols[i]:
            st.markdown(
                f"<div style='text-align:center;padding:10px;border-radius:10px;"
                f"background:{COLORS['green'] + '15' if is_completed else COLORS['dim'] + '22'};'>"
                f"<div style='font-size:20px;'>{'✅' if is_completed else info['icon']}</div>"
                f"<div style='font-size:11px;font-weight:700;color:{COLORS['green'] if is_completed else COLORS['muted']};'>"
                f"{info['label']}</div></div>",
                unsafe_allow_html=True,
            )
    if topic_complete:
        st.success(f"🎓 You've completed all of {completed_topic}! All 3 modules done. Great work!")
    card_close()

    if st.session_state.difficulty_changed:
        card_open()
        icon = "📈" if quiz_score >= 80 else "📉"
        title = "Leveling up your difficulty!" if quiz_score >= 80 else "Adjusting to make things easier"
        detail = (
            "You've been doing really well consistently, so we're increasing the challenge. You're ready for it!"
            if quiz_score >= 80 else
            "We noticed this has been tough, so we're making the next session a bit easier. "
            "There's no shame in that — learning takes time."
        )
        st.markdown(f"### {icon} {title}")
        st.caption(detail)
        card_close()

    rec = st.session_state.next_rec
    if rec:
        card_open(highlight=True)
        section_label("🤖 What your learning coach recommends next")
        st.markdown(f"### {rec['topic']}")
        st.markdown(badge(diff_label(rec["difficulty"]), diff_color(rec["difficulty"]))
                     + (badge(f"Next: {next_mod_info['label']}", COLORS["cyan"])
                        if next_mod_info and not topic_complete
                        else badge(rec.get("strategy", "progression"), COLORS["accent"])),
                     unsafe_allow_html=True)
        st.write(rec.get("explanation", ""))
        if rec.get("encouragement"):
            st.markdown(f"*\"{rec['encouragement']}\"*")
        card_close()

    cols = st.columns(2)
    with cols[0]:
        label = f"Continue to {next_mod_info['label']} →" if (next_mod_info and not topic_complete) else "Start Next Lesson →"
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.stage = STAGE_LEARNING
            st.rerun()
    with cols[1]:
        if st.button("📊 View My Dashboard", use_container_width=True):
            st.session_state.stage = STAGE_DASHBOARD
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────
# Stage: Dashboard
# ─────────────────────────────────────────────────────────────────────────
def render_dashboard():
    extracted_skills = st.session_state.extracted_skills
    target_role = st.session_state.target_role
    module_progress = st.session_state.module_progress
    quiz_history = st.session_state.quiz_history

    role_skills = ROLE_SKILLS.get(target_role, [])
    covered_skills = [s for s in extracted_skills if s in role_skills]
    role_readiness = round((len(covered_skills) / len(role_skills)) * 100) if role_skills else 0

    topic_knowledge = {t: compute_topic_knowledge(t, extracted_skills, module_progress, quiz_history) for t in TOPICS}
    avg_score = round(sum(h["quizScore"] for h in quiz_history) / len(quiz_history)) if quiz_history else 0
    completed_topics = sum(
        1 for t in TOPICS
        if all(get_module_status(module_progress, t)[m] == "completed" for m in MODULE_KEYS)
    )

    st.markdown("## 📊 My Learning Dashboard")
    cols = st.columns(4)
    cols[0].metric("🎯 Career Readiness", f"{role_readiness}%")
    cols[1].metric("✅ Lessons Done", st.session_state.session_count)
    cols[2].metric("🏆 Avg Quiz Score", f"{avg_score}%" if avg_score > 0 else "—")
    cols[3].metric("📚 Topics Finished", f"{completed_topics}/{len(TOPICS)}")

    tab_overview, tab_subjects, tab_role, tab_history = st.tabs(
        ["📊 Overview", "📚 My Progress", "🎯 Career Fit", "📈 History"]
    )

    with tab_overview:
        card_open()
        section_label("How much you know about each subject")
        for t in TOPICS:
            val = topic_knowledge[t]
            color = COLORS["green"] if val > 0.7 else COLORS["cyan"] if val > 0.35 else COLORS["accent"]
            st.markdown(f"<div style='display:flex;justify-content:space-between;'><span style='font-size:12px;color:{COLORS['muted']};'>{t}</span>"
                         f"<span style='font-size:12px;color:{color};font-weight:700;'>{round(val*100)}%</span></div>",
                         unsafe_allow_html=True)
            st.progress(val)
        st.caption("💡 These percentages are estimated based on what you listed on your resume and your quiz "
                   "performance — not a fixed default. Keep completing lessons to improve your scores!")
        card_close()

    with tab_subjects:
        card_open()
        section_label("Your learning journey — level by level")
        for t in TOPICS:
            knowledge = topic_knowledge[t]
            status = get_module_status(module_progress, t)
            topic_quizzes = [h for h in quiz_history if h["topic"] == t]
            is_current = t == st.session_state.current_topic
            k_color = COLORS["green"] if knowledge > 0.7 else COLORS["amber"] if knowledge > 0.35 else COLORS["red"]

            st.markdown(f"**{t}** {'· *Currently Studying*' if is_current else ''} "
                         f"— <span style='color:{k_color};font-weight:900;'>{round(knowledge*100)}%</span>",
                         unsafe_allow_html=True)
            st.progress(knowledge)
            mcols = st.columns(3)
            for i, mk in enumerate(MODULE_KEYS):
                ms = status[mk]
                info = MODULE_STRUCTURE[mk]
                icon = "✅" if ms == "completed" else info["icon"] if ms == "active" else "🔒"
                state_label = "Done!" if ms == "completed" else "In Progress" if ms == "active" else "Locked"
                mcols[i].markdown(f"<div style='text-align:center;'>{icon}<br>"
                                    f"<span style='font-size:11px;'>{info['label']}</span><br>"
                                    f"<span style='font-size:9px;color:{COLORS['muted']};'>{state_label}</span></div>",
                                    unsafe_allow_html=True)
            if topic_quizzes:
                best = max(h["quizScore"] for h in topic_quizzes)
                st.caption(f"Best Score: **{best}%** · Sessions: **{len(topic_quizzes)}**")
            st.markdown("---")
        card_close()

    with tab_role:
        card_open()
        section_label(f"How ready are you to become a {target_role}?")
        st.markdown(f"Overall Readiness — **{role_readiness}%**")
        st.progress(role_readiness / 100)
        st.caption(f"Based on skills found in your resume vs. what a {target_role} typically needs")

        cols = st.columns(2)
        for i, skill in enumerate(role_skills):
            has = skill in extracted_skills
            with cols[i % 2]:
                st.markdown(f"{'✅' if has else '❌'} {skill}")

        gaps = [s for s in role_skills if s not in extracted_skills]
        if gaps:
            st.warning("🎯 Focus on these to close the gap: " + ", ".join(gaps[:5]))
        card_close()

    with tab_history:
        card_open()
        section_label("Your recent sessions")
        if not quiz_history:
            st.caption("No sessions yet. Complete your first quiz to see your history here!")
        else:
            for h in reversed(quiz_history):
                cols = st.columns([2, 1, 1])
                cols[0].markdown(f"**{h['topic']}**  \n{h['module']} · {h['difficulty']}")
                cols[1].markdown(f"Quiz: **{h['quizScore']}%**")
                cols[2].markdown(f"Code: **{h['codeScore']}%**")
        card_close()

    if st.button("Continue Studying →", type="primary"):
        st.session_state.stage = STAGE_LEARNING
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────────────────
render_nav()

if st.session_state.stage == STAGE_UPLOAD:
    render_upload()
elif st.session_state.stage == STAGE_DASHBOARD:
    render_dashboard()
elif st.session_state.stage == STAGE_LEARNING:
    render_learning()
elif st.session_state.stage == STAGE_QUIZ:
    render_quiz()
elif st.session_state.stage == STAGE_RESULTS:
    render_results()
