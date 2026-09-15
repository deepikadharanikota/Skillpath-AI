import os
import time
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
PUBLIC_BACKEND_URL = os.getenv("PUBLIC_BACKEND_URL", "http://localhost:8000")

STAGE_LOGIN = "login"
STAGE_UPLOAD = "upload"
STAGE_DASHBOARD = "dashboard"
STAGE_LEARNING = "learning"
STAGE_QUIZ = "quiz"
STAGE_RESULTS = "results"

st.set_page_config(page_title="SkillPath AI", page_icon="🎓", layout="centered")

def init_state():
    defaults = {
        "token": None,
        "stage": STAGE_LOGIN,
        "user_state": None,
        "quiz_questions": [],
        "quiz_idx": 0,
        "quiz_score": 0,
        "quiz_done": False,
        "quiz_answers": {},
        "quiz_question_start_time": 0.0,
        "code_text": "",
        "code_eval": None,
        "last_reward": 0.0,
        "next_rec": None
    }
    
    query_params = st.query_params
    if "token" in query_params and "token" not in st.session_state:
        st.session_state["token"] = query_params["token"]
        st.session_state["stage"] = STAGE_UPLOAD
        
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    /* Glassmorphism containers (metrics, expanders) */
    div[data-testid="stExpander"], div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    /* Style headings */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    if st.session_state.stage != STAGE_LOGIN and st.session_state.token:
        with st.sidebar:
            st.markdown("### ⚙️ Account")
            if st.button("Logout 🚪", key="sidebar_logout"):
                st.session_state.clear()
                st.query_params.clear()
                st.rerun()

def fetch_state():
    headers = {"token": st.session_state.token}
    resp = requests.get(f"{BACKEND_URL}/learning/state", headers=headers)
    if resp.status_code == 200:
        st.session_state.user_state = resp.json()
        
def render_login():
    inject_custom_css()
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>SkillPath AI 🎓</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #888;'>Your intelligent, adaptive learning journey starts here.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if "error" in st.query_params:
            st.error(f"⚠️ Authentication Error: {st.query_params['error']}")

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f'<a href="{PUBLIC_BACKEND_URL}/auth/login" target="_self" style="text-decoration: none;"><button style="width: 100%; padding: 15px; font-size: 18px; font-weight: bold; background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); color: white; border: none; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;">Login with GitHub 🚀</button></a>', unsafe_allow_html=True)

def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF file."""
    import PyPDF2
    import io
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_text_from_docx(file_bytes):
    """Extract text from a DOCX file."""
    import docx
    import io
    doc = docx.Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def render_upload():
    inject_custom_css()
    render_sidebar()
    st.markdown("## 🚀 Kickstart Your Journey")
    st.markdown("Upload your resume to let our AI build a personalized curriculum tailored to your exact skill gaps.")
    st.markdown("---")
    
    col_input, col_role = st.columns(2)
    
    resume_text = ""
    with col_input:
        st.markdown("#### 1. Provide Resume")
        upload_method = st.radio("Choose input method:", ["Upload File (PDF/DOCX)", "Paste Text"], horizontal=True, label_visibility="collapsed")
        
        if upload_method == "Upload File (PDF/DOCX)":
            uploaded_file = st.file_uploader("Drop file here", type=["pdf", "docx"], label_visibility="collapsed")
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                with st.spinner("Extracting text..."):
                    if uploaded_file.name.lower().endswith(".pdf"):
                        resume_text = extract_text_from_pdf(file_bytes)
                    elif uploaded_file.name.lower().endswith(".docx"):
                        resume_text = extract_text_from_docx(file_bytes)
                
                if resume_text:
                    st.success(f"✅ Extracted {len(resume_text.split())} words.")
                    with st.expander("Preview text"):
                        st.text(resume_text[:1000] + "...")
                else:
                    st.warning("Could not extract text.")
        else:
            resume_text = st.text_area("Paste text", height=150, label_visibility="collapsed")
            
    with col_role:
        st.markdown("#### 2. Select Target Role")
        @st.cache_data(ttl=3600)
        def fetch_roles():
            try:
                resp = requests.get(f"{BACKEND_URL}/roles", timeout=5)
                if resp.status_code == 200:
                    return resp.json().get("roles", ["ML Engineer"])
            except Exception as e:
                pass
            return ["ML Engineer"]
            
        available_roles = fetch_roles()
        target_role = st.selectbox("Role", available_roles, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Learning Journey ➔"):
            if not resume_text.strip():
                st.error("Please provide your resume text or upload a file first.")
                return
            with st.spinner("Analyzing skill gaps..."):
                headers = {"token": st.session_state.token}
                payload = {"resume_text": resume_text, "target_role": target_role}
                resp = requests.post(f"{BACKEND_URL}/learning/start", json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.user_state = data["state"]
                    st.session_state.stage = STAGE_LEARNING
                    st.rerun()

def render_learning():
    inject_custom_css()
    render_sidebar()
    state = st.session_state.user_state
    if not state:
        fetch_state()
        state = st.session_state.user_state
        
    topic = state.get('current_topic', 'N/A')
    difficulty = state.get('current_difficulty', 'N/A')
    module = state.get('current_module', 'N/A')
    
    col_header, col_action = st.columns([2, 1])
    with col_header:
        st.markdown(f"## 📚 {topic} Journey")
        st.markdown(f"**Difficulty:** `{difficulty.upper()}` &nbsp;|&nbsp; **Module:** `{module.upper()}`")
    with col_action:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Take Quiz"):
            headers = {"token": st.session_state.token}
            resp = requests.get(f"{BACKEND_URL}/quiz/generate", params={"topic": topic, "difficulty": difficulty}, headers=headers)
            if resp.status_code == 200:
                st.session_state.quiz_questions = resp.json()["questions"]
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_done = False
                st.session_state.stage = STAGE_QUIZ
                st.session_state.quiz_question_start_time = time.time()
                st.rerun()
                
    st.markdown("---")
    st.markdown("### 🎬 Suggested Videos")
    
    headers = {"token": st.session_state.token}
    resp = requests.get(
        f"{BACKEND_URL}/learning/videos",
        params={"topic": topic, "difficulty": difficulty, "module": module},
        headers=headers
    )
    
    if resp.status_code == 200:
        videos = resp.json().get("videos", [])
        if videos:
            recommended_vids = [v for v in videos if v.get("recommended")]
            other_vids = [v for v in videos if not v.get("recommended")]
            
            def render_video(video, is_recommended=False):
                vid_url = video.get("url", "")
                vid_id = ""
                if "v=" in vid_url:
                    vid_id = vid_url.split("v=")[-1].split("&")[0]
                elif "youtu.be/" in vid_url:
                    vid_id = vid_url.split("youtu.be/")[-1].split("?")[0]
                
                if is_recommended:
                    st.markdown("#### 🌟 Recommended Best Video")
                else:
                    st.markdown(f"**{video.get('module', '').capitalize()} Module Video**")
                    
                vcol1, vcol2 = st.columns([1, 2])
                with vcol1:
                    if video.get("thumb"):
                        st.image(video["thumb"], use_container_width=True)
                with vcol2:
                    st.markdown(f"**{video.get('title', 'Video')}**")
                    st.caption(f"📺 {video.get('channel', '')} &nbsp;|&nbsp; ⏱ {video.get('duration', '')} &nbsp;|&nbsp; 👁 {video.get('views', '')} views")
                    st.markdown(f"[▶ Watch on YouTube]({vid_url})")
                
                if vid_id and is_recommended:
                    st.video(f"https://www.youtube.com/watch?v={vid_id}")
            
            if recommended_vids:
                render_video(recommended_vids[0], is_recommended=True)
                st.markdown("---")
                
            if other_vids:
                with st.expander("Show alternative videos"):
                    for i, video in enumerate(other_vids):
                        render_video(video)
                        if i < len(other_vids) - 1:
                            st.markdown("---")
        else:
            st.info("No videos available yet.")
    else:
        st.warning("Could not load videos.")

def render_quiz():
    inject_custom_css()
    render_sidebar()
    questions = st.session_state.quiz_questions
    idx = st.session_state.quiz_idx
    
    if st.session_state.quiz_done:
        st.markdown(f"## 🏆 Quiz Complete!")
        st.metric("Score", f"{st.session_state.quiz_score}%")
        st.markdown("---")
        st.markdown("### 💻 Code Challenge")
        code = st.text_area("Write your code here (optional)", value=st.session_state.code_text, height=150)
        st.session_state.code_text = code
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Check My Code"):
                headers = {"token": st.session_state.token}
                resp = requests.post(f"{BACKEND_URL}/learning/evaluate_code", json={"code": code}, headers=headers)
                if resp.status_code == 200:
                    st.session_state.code_eval = resp.json()
        with c2:
            if st.button("Submit Module ➔"):
                headers = {"token": st.session_state.token}
                code_score = st.session_state.code_eval["score"] if st.session_state.code_eval else 0
                payload = {"quiz_score": st.session_state.quiz_score, "code_score": code_score}
                resp = requests.post(f"{BACKEND_URL}/learning/submit_module", json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.last_reward = data["reward"]
                    st.session_state.next_rec = data["next_recommendation"]
                    st.session_state.stage = STAGE_RESULTS
                    st.rerun()
                
        if st.session_state.code_eval:
            st.success(f"Code Score: {st.session_state.code_eval['score']}%")
            
        return

    q = questions[idx]
    st.markdown(f"### Question {idx+1} of {len(questions)}")
    st.progress((idx) / len(questions))
    
    st.markdown(f"**{q['q']}**")
    selected = st.radio("Select your answer:", q['opts'], index=None, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    elapsed = time.time() - st.session_state.quiz_question_start_time
    remaining = max(0, 40 - elapsed)
    
    col_submit, col_time = st.columns([1, 1])
    with col_time:
        st.caption(f"⏱ {int(remaining)}s remaining")
        st.progress(remaining / 40)
    with col_submit:
        if remaining <= 0 or st.button("Submit Answer"):
            ans_idx = q['opts'].index(selected) if selected else -1
            st.session_state.quiz_answers[idx] = ans_idx
            
            if idx + 1 >= len(questions):
                correct = sum(1 for i, qq in enumerate(questions) if st.session_state.quiz_answers.get(i) == qq['ans'])
                st.session_state.quiz_score = int((correct / len(questions)) * 100)
                st.session_state.quiz_done = True
            else:
                st.session_state.quiz_idx += 1
                st.session_state.quiz_question_start_time = time.time()
            st.rerun()
            
    st_autorefresh(interval=1000, key=f"timer_{idx}")

def render_results():
    inject_custom_css()
    render_sidebar()
    st.markdown("## 🎉 Module Complete!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("AI Reward Signal", f"{st.session_state.last_reward:+.2f}")
    with col2:
        st.metric("Next Topic", st.session_state.next_rec['topic'])
        st.metric("Recommended Difficulty", st.session_state.next_rec['difficulty'].upper())
    
    st.markdown("---")
    
    if st.button("Continue to Next Module ➔"):
        st.session_state.stage = STAGE_LEARNING
        st.rerun()

if st.session_state.stage == STAGE_LOGIN:
    render_login()
elif st.session_state.stage == STAGE_UPLOAD:
    render_upload()
elif st.session_state.stage == STAGE_LEARNING:
    render_learning()
elif st.session_state.stage == STAGE_QUIZ:
    render_quiz()
elif st.session_state.stage == STAGE_RESULTS:
    render_results()
