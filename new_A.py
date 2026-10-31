import html
import inspect
import os
import tempfile

import streamlit as st

from main import run_pipeline
from core.rag_engine import ask_question

st.set_page_config(
    page_title="VideoMind AI",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====================================================================== STYLE
FONTS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=DM+Sans:wght@400;500;600&display=swap');
</style>"""

CSS = """
<style>
:root{
  --ink:#07061a; --panel:#100e2b; --panel2:#0b0a22; --line:#2a2650;
  --text:#ece9ff; --muted:#9a95c7;
  --violet:#7c5cff; --cyan:#22d3ee; --amber:#ffb454; --rose:#ff5fa2;
  --display:'Bricolage Grotesque','Segoe UI',sans-serif; --body:'DM Sans','Segoe UI',sans-serif;
}
@property --a{syntax:'<angle>'; initial-value:0deg; inherits:false}

html, body, .stApp, .stMarkdown, input, textarea, button, label{font-family:var(--body)}
.stApp{background:var(--ink); color:var(--text)}
[data-testid="stHeader"]{background:transparent}
#MainMenu, footer{visibility:hidden}
.block-container{position:relative; z-index:2; max-width:1400px; padding:1.2rem 2rem 4rem}

/* ---------- ambient background: drifting aurora + fine grid ---------- */
.stApp::before{content:""; position:fixed; inset:-20%; z-index:0; pointer-events:none;
  background:
    radial-gradient(38% 34% at 18% 22%, rgba(124,92,255,.38), transparent 70%),
    radial-gradient(34% 30% at 82% 18%, rgba(34,211,238,.22), transparent 70%),
    radial-gradient(40% 36% at 70% 88%, rgba(255,95,162,.18), transparent 70%),
    radial-gradient(30% 28% at 8% 90%, rgba(255,180,84,.12), transparent 70%);
  filter:blur(30px); animation:drift 26s ease-in-out infinite alternate}
.stApp::after{content:""; position:fixed; inset:0; z-index:1; pointer-events:none; opacity:.5;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
  background-size:56px 56px; mask-image:radial-gradient(70% 60% at 50% 30%, #000 30%, transparent 100%)}
@keyframes drift{0%{transform:translate3d(-2%,-1%,0) scale(1)}100%{transform:translate3d(3%,2%,0) scale(1.08)}}

/* ---------- top bar ---------- */
.brand{display:flex; align-items:center; gap:.7rem; font-family:var(--display); font-weight:800; font-size:1.45rem; letter-spacing:-.3px}
.mark{display:flex; align-items:flex-end; gap:3px; height:26px}
.mark i{width:5px; border-radius:3px; background:linear-gradient(180deg,var(--cyan),var(--violet)); animation:wave 1.2s ease-in-out infinite}
.mark i:nth-child(1){height:40%}.mark i:nth-child(2){height:100%; animation-delay:.15s}
.mark i:nth-child(3){height:65%; animation-delay:.3s}.mark i:nth-child(4){height:85%; animation-delay:.45s}
@keyframes wave{0%,100%{transform:scaleY(.18)}50%{transform:scaleY(1)}}

/* ---------- hero: centered, one orchestrated entrance ---------- */
.hero{text-align:center; max-width:50rem; margin:2.2rem auto 0}
.hero-h{font-family:var(--display); font-weight:800; font-size:clamp(2.6rem,5.6vw,4.8rem); line-height:1.02; letter-spacing:-1.5px;
  margin:0 0 1rem; background:linear-gradient(100deg,#fff 10%,#cfc6ff 45%,#8fe9f7 80%); background-size:200% 100%;
  -webkit-background-clip:text; background-clip:text; color:transparent; animation:rise .9s cubic-bezier(.2,.8,.2,1) both, sheen 9s ease-in-out 1s infinite}
.hero-p{color:var(--muted); font-size:1.15rem; line-height:1.6; max-width:38rem; margin:0 auto; animation:rise .9s .12s cubic-bezier(.2,.8,.2,1) both}
.tags{display:flex; flex-wrap:wrap; justify-content:center; gap:.55rem; margin-top:1.4rem; animation:rise .9s .24s cubic-bezier(.2,.8,.2,1) both}
.tag{padding:.38rem .85rem; border-radius:999px; border:1px solid var(--line); background:rgba(255,255,255,.04); color:#cfcaf5; font-size:.9rem}
@keyframes rise{from{opacity:0; transform:translateY(22px)}to{opacity:1; transform:none}}
@keyframes sheen{0%,100%{background-position:0% 0}50%{background-position:100% 0}}

/* ---------- signature element: spinning gradient border on the input panel ---------- */
.st-key-analyze{max-width:780px; margin:2.2rem auto 0; border:1.5px solid transparent; border-radius:24px; padding:1.4rem 1.6rem 1.2rem;
  background:linear-gradient(var(--panel),var(--panel2)) padding-box,
             conic-gradient(from var(--a), var(--violet), var(--cyan), var(--amber), var(--rose), var(--violet)) border-box;
  animation:spin 7s linear infinite, rise .9s .35s cubic-bezier(.2,.8,.2,1) both; box-shadow:0 20px 70px rgba(124,92,255,.18)}
@keyframes spin{to{--a:360deg}}
.panel-h{font-family:var(--display); font-size:1.5rem; font-weight:800; margin:0 0 .2rem}
.panel-s{color:var(--muted); margin-bottom:.6rem}

/* ---------- feature tiles ---------- */
.tiles{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; margin-top:2.6rem}
.tile{padding:1.3rem 1.4rem; border-radius:20px; border:1px solid var(--line); background:rgba(16,14,43,.7);
  transition:transform .25s, border-color .25s, box-shadow .25s}
.tile:hover{transform:translateY(-5px); border-color:var(--violet); box-shadow:0 18px 50px rgba(124,92,255,.25)}
.tile .ic{font-size:1.5rem; width:46px; height:46px; display:grid; place-items:center; border-radius:14px; margin-bottom:.8rem;
  background:linear-gradient(135deg,rgba(124,92,255,.35),rgba(34,211,238,.25))}
.tile h4{margin:0 0 .3rem; font-family:var(--display); font-size:1.15rem}
.tile p{margin:0; color:var(--muted); line-height:1.5}

/* ---------- live progress (shown while a video is being analyzed) ---------- */
.load{display:grid; place-items:center; min-height:80vh}
.runbox{width:min(580px,100%); padding:1.8rem 1.9rem 1.5rem; border-radius:24px; border:1px solid var(--line);
  background:rgba(16,14,43,.85); backdrop-filter:blur(14px); box-shadow:0 30px 80px rgba(7,6,26,.6)}
.run-h{font-family:var(--display); font-weight:800; font-size:1.6rem; margin:0}
.run-s{color:var(--muted); margin:.25rem 0 1.1rem}
.bar{height:5px; border-radius:5px; background:var(--line); overflow:hidden; margin-bottom:1.1rem}
.bar i{display:block; height:100%; border-radius:5px; background:linear-gradient(90deg,var(--violet),var(--cyan)); transition:width .6s ease}
.bar.indet i{width:35%; animation:slide 1.4s ease-in-out infinite alternate}
@keyframes slide{from{margin-left:0}to{margin-left:65%}}
.step{display:flex; gap:.95rem; align-items:flex-start; padding:.75rem 0; opacity:.42; transition:opacity .3s}
.step.done{opacity:.85}
.step.active{opacity:1}
.step + .step{border-top:1px solid rgba(42,38,80,.7)}
.dot{flex:0 0 30px; height:30px; border-radius:50%; display:grid; place-items:center; font-size:.85rem; font-weight:600;
  border:1.5px solid var(--line); color:var(--muted)}
.step.done .dot{background:linear-gradient(135deg,var(--violet),var(--cyan)); border-color:transparent; color:#07061a; font-weight:800}
.step.active .dot{border-color:rgba(34,211,238,.25); border-top-color:var(--cyan); animation:rot 1s linear infinite}
.step b{display:block; font-weight:600; font-size:1.05rem}
.step small{display:block; color:var(--muted); margin-top:.1rem; font-size:.9rem}
.step.active small{color:#9ff0fb}
.note{color:var(--muted); font-size:.88rem; margin:.9rem 0 0}
@keyframes rot{to{transform:rotate(360deg)}}

/* ---------- workspace ---------- */
.vtitle{font-family:var(--display); font-weight:800; font-size:clamp(1.6rem,3vw,2.3rem); letter-spacing:-.6px; line-height:1.1; margin:.4rem 0 .9rem}
.chips{display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1rem}
.chip{padding:.35rem .8rem; border-radius:999px; background:rgba(34,211,238,.1); border:1px solid rgba(34,211,238,.3); color:#9ff0fb; font-size:.88rem}
.chip.v{background:rgba(124,92,255,.14); border-color:rgba(124,92,255,.4); color:#cfc6ff}
[data-testid="stVideo"]{border-radius:20px; overflow:hidden; border:1px solid var(--line); box-shadow:0 24px 60px rgba(0,0,0,.55)}
.st-key-results, .st-key-chat{border:1px solid var(--line); border-radius:22px; padding:1.1rem 1.3rem; background:rgba(16,14,43,.78); backdrop-filter:blur(12px)}
.st-key-results{margin-top:1.1rem}
.transcript{max-height:340px; overflow-y:auto; line-height:1.75; color:#cfcaf5; white-space:pre-wrap; padding-right:.6rem}
.transcript::-webkit-scrollbar{width:6px}.transcript::-webkit-scrollbar-thumb{background:var(--line); border-radius:6px}
.live{display:inline-flex; align-items:center; gap:.45rem; color:#7ff0d6; font-size:.88rem}
.live i{width:8px; height:8px; border-radius:50%; background:#7ff0d6; animation:ping 1.7s ease-in-out infinite}
@keyframes ping{0%,100%{box-shadow:0 0 0 0 rgba(127,240,214,.6)}50%{box-shadow:0 0 0 8px rgba(127,240,214,0)}}
.chat-h{font-family:var(--display); font-weight:800; font-size:1.3rem; margin-bottom:.2rem}
.row{display:flex; gap:.7rem; margin:.8rem 0; align-items:flex-start}
.row.user{flex-direction:row-reverse}
.av{flex:0 0 34px; height:34px; border-radius:50%; display:grid; place-items:center; font-size:.95rem}
.av.user{background:linear-gradient(135deg,var(--amber),var(--rose))}
.av.bot{background:linear-gradient(135deg,var(--cyan),var(--violet))}
.bub{max-width:84%; padding:.7rem 1rem; border-radius:16px; line-height:1.6; animation:pop .3s ease-out}
.bub.user{background:#1d1a45; border:1px solid var(--line); border-top-right-radius:4px}
.bub.bot{background:rgba(124,92,255,.14); border:1px solid rgba(124,92,255,.5); border-top-left-radius:4px}
@keyframes pop{from{opacity:0; transform:translateY(10px) scale(.97)}to{opacity:1; transform:none}}
.dots span{display:inline-block; width:8px; height:8px; margin:0 3px; border-radius:50%; background:var(--cyan); animation:bounce 1.1s infinite}
.dots span:nth-child(2){animation-delay:.15s}.dots span:nth-child(3){animation-delay:.3s}
@keyframes bounce{0%,80%,100%{transform:translateY(0); opacity:.4}40%{transform:translateY(-7px); opacity:1}}
.empty-chat{color:var(--muted); text-align:center; padding:2.2rem .5rem}

/* ---------- widgets ---------- */
.stTextInput input{background:#0a0922; border:1px solid var(--line); border-radius:14px; color:var(--text); padding:.75rem 1rem}
.stTextInput input:focus{border-color:var(--cyan); box-shadow:0 0 0 3px rgba(34,211,238,.18)}
.main .stButton>button, [data-testid="stFormSubmitButton"]>button, .stDownloadButton>button{
  background:linear-gradient(95deg,var(--violet),var(--cyan)); color:#07061a; font-weight:700; border:none; border-radius:14px;
  padding:.6rem 1.3rem; transition:transform .18s, box-shadow .18s, filter .18s}
.main .stButton>button:hover, [data-testid="stFormSubmitButton"]>button:hover, .stDownloadButton>button:hover{
  transform:translateY(-2px); box-shadow:0 12px 30px rgba(124,92,255,.45); filter:brightness(1.08)}
.main .stButton>button:active{transform:translateY(0) scale(.98)}
.stTabs [data-baseweb="tab"]{color:var(--muted); font-weight:500}
.stTabs [aria-selected="true"]{color:#fff}
.stTabs [data-baseweb="tab-highlight"]{background:linear-gradient(90deg,var(--violet),var(--cyan)); height:3px}
[data-testid="stFileUploaderDropzone"]{background:rgba(124,92,255,.07); border:1.5px dashed rgba(124,92,255,.6); border-radius:16px}
.st-key-sug button{background:rgba(255,255,255,.05) !important; color:#d8d4ff !important; border:1px solid var(--line) !important; font-weight:500 !important}
[data-testid="stSidebar"]{background:var(--panel2); border-right:1px solid var(--line)}
[data-testid="stSidebar"] .stButton>button{width:100%; justify-content:flex-start; text-align:left; background:transparent; color:#cfcaf5; border:1px solid var(--line); border-radius:12px}

@media (prefers-reduced-motion: reduce){ *, *::before, *::after{animation:none !important; transition:none !important} }
</style>
"""

st.markdown(FONTS, unsafe_allow_html=True)
st.markdown(CSS, unsafe_allow_html=True)

# ====================================================================== STATE
st.session_state.setdefault("history", [])  # newest first
st.session_state.setdefault("current", None)
st.session_state.setdefault("language", "english")


def open_entry(i):
    st.session_state.current = i


def new_video():
    st.session_state.current = None


def ask_suggestion(text):
    st.session_state.pending_q = text


def bubble(role, text):
    safe = html.escape(str(text)).replace("\n", "<br>")
    icon = "🧑" if role == "user" else "✦"
    return f'<div class="row {role}"><div class="av {role}">{icon}</div><div class="bub {role}">{safe}</div></div>'


TYPING = '<div class="row"><div class="av bot">✦</div><div class="bub bot"><div class="dots"><span></span><span></span><span></span></div></div></div>'

# ====================================================================== PROGRESS
# The keys below are what run_pipeline() reports through on_progress(step, detail).
STEPS = [
    ("audio", "Preparing the audio", "Downloading or converting, then splitting into parts"),
    ("transcribe", "Writing the transcript", "Turning speech into text"),
    ("summary", "Finding the key points", "Summary, action items and decisions"),
    ("index", "Building the search index", "So you can chat with the video"),
]
STEP_KEYS = [key for key, _, _ in STEPS]


def loader_html(active=None, detail=""):
    """HTML for the progress card. active = index of the running step.
    active=None means the pipeline cannot report steps, so show a plain busy bar."""
    # NOTE: built on a single line on purpose; indented lines would be rendered as a code block by markdown.
    if active is None:
        return (
            '<div class="load"><div class="runbox">'
            '<div class="run-h">Analyzing your video</div>'
            '<div class="run-s">This can take a few minutes for long videos. Keep this tab open.</div>'
            '<div class="bar indet"><i></i></div></div></div>'
        )

    rows = ""
    for i, (_, label, desc) in enumerate(STEPS):
        if i < active:
            state, mark, text = "done", "✓", "Done"
        elif i == active:
            state, mark, text = "active", "", html.escape(detail) if detail else desc
        else:
            state, mark, text = "todo", str(i + 1), desc
        rows += (
            f'<div class="step {state}"><div class="dot">{mark}</div>'
            f"<div><b>{label}</b><small>{text}</small></div></div>"
        )
    pct = int((active + 0.5) / len(STEPS) * 100)
    return (
        '<div class="load"><div class="runbox">'
        '<div class="run-h">Analyzing your video</div>'
        f'<div class="run-s">Step {active + 1} of {len(STEPS)}: {STEPS[active][1].lower()}</div>'
        f'<div class="bar"><i style="width:{pct}%"></i></div>'
        f"{rows}"
        '<div class="note">Long videos can take a few minutes. Keep this tab open.</div>'
        "</div></div>"
    )


# ====================================================================== JOB
job = st.session_state.get("job")
if job:
    slot = st.empty()  # this one element is redrawn every time the pipeline moves to a new step

    # works with the old run_pipeline too: live steps only appear once it accepts on_progress
    reports_progress = "on_progress" in inspect.signature(run_pipeline).parameters

    def report(step, detail=""):
        if step in STEP_KEYS:
            slot.markdown(loader_html(STEP_KEYS.index(step), detail), unsafe_allow_html=True)

    slot.markdown(loader_html(0 if reports_progress else None), unsafe_allow_html=True)
    try:
        extra = {"on_progress": report} if reports_progress else {}
        result = run_pipeline(job["source"], job["language"], **extra)
        st.session_state.history.insert(
            0,
            {"label": result.get("title") or job["label"], "result": result, "video": job["video"], "messages": []},
        )
        st.session_state.current = 0
    except Exception as exc:
        st.session_state.error = f"Could not analyze this video: {exc}"
    st.session_state.pop("job", None)
    st.rerun()

# ====================================================================== SIDEBAR
with st.sidebar:
    st.markdown("### Your library")
    if not st.session_state.history:
        st.caption("Analyzed videos will appear here.")
    for i, e in enumerate(st.session_state.history):
        st.button(f"▶  {str(e['label'])[:30]}", key=f"hist_{i}", on_click=open_entry, args=(i,))

# ====================================================================== TOP BAR
bar_l, bar_r = st.columns([4, 1])
bar_l.markdown(
    '<div class="brand"><div class="mark"><i></i><i></i><i></i><i></i></div>VideoMind AI</div>',
    unsafe_allow_html=True,
)
if st.session_state.current is not None:
    bar_r.button("＋ New video", on_click=new_video, use_container_width=True)


# ====================================================================== LANDING
def start_job(source, label, video):
    st.session_state.job = {"source": source, "label": label, "video": video, "language": st.session_state.language}
    st.rerun()


def page_landing():
    if "error" in st.session_state:
        st.error(st.session_state.pop("error"))

    st.markdown(
        '<div class="hero"><div class="hero-h">Ask any video anything.</div>'
        '<div class="hero-p">Paste a YouTube link or drop in a file. VideoMind transcribes it, writes the summary and '
        "action items, then answers your questions using what was actually said.</div>"
        '<div class="tags"><span class="tag">YouTube links</span><span class="tag">Local video files</span>'
        '<span class="tag">English and Hinglish</span></div></div>',
        unsafe_allow_html=True,
    )

    with st.container(key="analyze"):
        st.markdown(
            '<div class="panel-h">Start with a video</div>'
            '<div class="panel-s">Pick a source, choose the spoken language, and press Analyze.</div>',
            unsafe_allow_html=True,
        )
        st.session_state.language = st.radio(
            "Spoken language",
            ["english", "hinglish"],
            index=["english", "hinglish"].index(st.session_state.language),
            horizontal=True,
        )
        t_url, t_file = st.tabs(["YouTube link", "Upload a video"])
        with t_url:
            c1, c2 = st.columns([4, 1])
            url = c1.text_input("link", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
            if c2.button("Analyze", key="go_url", use_container_width=True):
                if url.strip():
                    start_job(url.strip(), "YouTube video", url.strip())
                else:
                    st.warning("Paste a YouTube link first.")
        with t_file:
            up = st.file_uploader(
                "video",
                type=["mp4", "mov", "mkv", "avi", "webm", "mp3", "wav", "m4a"],
                label_visibility="collapsed",
            )
            if st.button("Analyze file", key="go_file"):
                if up is None:
                    st.warning("Choose a video file first.")
                else:
                    suffix = os.path.splitext(up.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(up.getbuffer())
                    start_job(tmp.name, up.name, tmp.name)

    st.markdown(
        '<div class="tiles">'
        '<div class="tile"><div class="ic">📝</div><h4>A title and summary</h4><p>Skip the full watch. Get the main points in a minute of reading.</p></div>'
        '<div class="tile"><div class="ic">✅</div><h4>Actions and decisions</h4><p>See who needs to do what, what was decided and what is still open.</p></div>'
        '<div class="tile"><div class="ic">💬</div><h4>Answers from the video</h4><p>Ask follow-up questions in plain language and get replies grounded in the transcript.</p></div>'
        "</div>",
        unsafe_allow_html=True,
    )


# ====================================================================== WORKSPACE
def page_workspace(entry):
    res = entry["result"]
    words = len(res["transcript"].split())
    minutes = max(1, round(words / 150))

    left, right = st.columns([1.35, 1], gap="large")

    with left:
        st.markdown(f'<div class="vtitle">{html.escape(str(res["title"]))}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="chips"><span class="chip">{words:,} words</span>'
            f'<span class="chip">about {minutes} min of speech</span>'
            f'<span class="chip v">{st.session_state.language.title()}</span></div>',
            unsafe_allow_html=True,
        )
        if entry["video"]:
            st.video(entry["video"])

        with st.container(key="results"):
            t1, t2, t3, t4, t5 = st.tabs(["Summary", "Action items", "Decisions", "Open questions", "Transcript"])
            with t1:
                st.markdown(res["summary"])
            with t2:
                st.markdown(res["action_items"])
            with t3:
                st.markdown(res["key_decisions"])
            with t4:
                st.markdown(res["open_questions"])
            with t5:
                st.markdown(
                    '<span class="live"><i></i>Search index ready</span>'
                    f'<div class="transcript" style="margin-top:.7rem">{html.escape(res["transcript"])}</div>',
                    unsafe_allow_html=True,
                )
        notes = (
            f"# {res['title']}\n\n## Summary\n{res['summary']}\n\n## Action items\n{res['action_items']}\n\n"
            f"## Key decisions\n{res['key_decisions']}\n\n## Open questions\n{res['open_questions']}\n"
        )
        st.download_button("Download notes", notes, file_name="video-notes.md", mime="text/markdown")

    with right:
        with st.container(key="chat"):
            st.markdown('<div class="chat-h">Chat with this video</div>', unsafe_allow_html=True)
            box = st.container(height=430, border=False)
            with box:
                if not entry["messages"]:
                    st.markdown(
                        '<div class="empty-chat">Ask a question and the answer comes from this video.<br>Try one of the ideas below.</div>',
                        unsafe_allow_html=True,
                    )
                for role, text in entry["messages"]:
                    st.markdown(bubble(role, text), unsafe_allow_html=True)

            if not entry["messages"]:
                with st.container(key="sug"):
                    for s in ["Summarize this in 3 points", "What are the key takeaways?", "What should I do next?"]:
                        st.button(s, key=f"s_{s}", on_click=ask_suggestion, args=(s,), use_container_width=True)

            with st.form("chat_form", clear_on_submit=True, border=False):
                c1, c2 = st.columns([5, 1])
                q = c1.text_input("q", placeholder="Ask anything about this video", label_visibility="collapsed")
                sent = c2.form_submit_button("Send")

        question = st.session_state.pop("pending_q", None) or (q.strip() if sent and q.strip() else None)
        if question:
            with box:
                st.markdown(bubble("user", question), unsafe_allow_html=True)
                wait = st.empty()
                wait.markdown(TYPING, unsafe_allow_html=True)
                try:
                    answer = ask_question(res["rag_chain"], question)
                except Exception as exc:
                    answer = f"Something went wrong while answering: {exc}"
                wait.empty()
            entry["messages"] += [("user", question), ("bot", answer)]
            st.rerun()


# ====================================================================== ROUTER
cur = st.session_state.current
if cur is None:
    page_landing()
else:
    page_workspace(st.session_state.history[cur])