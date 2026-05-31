import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (Tailwind-inspired, dark futuristic theme) ──────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  /* ── Base reset ── */
  html, body, [data-testid="stAppViewContainer"] {
    background: #080b14 !important;
    font-family: 'Space Grotesk', sans-serif;
  }
  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stSidebar"] { display: none; }

  /* ── Animated grid background ── */
  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(56,189,248,.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(56,189,248,.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* ── Hero header ── */
  .hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
    z-index: 1;
  }
  .hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(99,102,241,.15));
    border: 1px solid rgba(56,189,248,.3);
    color: #38bdf8;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    padding: .35rem .9rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
  }
  .hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.08;
    background: linear-gradient(135deg, #e2e8f0 30%, #38bdf8 70%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 .8rem;
  }
  .hero-sub {
    color: #64748b;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
  }

  /* ── Input card ── */
  .input-card {
    background: rgba(15,23,42,.8);
    border: 1px solid rgba(56,189,248,.18);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin: 1.5rem auto 2rem;
    max-width: 760px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 60px rgba(56,189,248,.06), 0 4px 32px rgba(0,0,0,.4);
    position: relative;
    z-index: 1;
  }
  .input-label {
    color: #94a3b8;
    font-size: .82rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .5rem;
  }

  /* ── Streamlit input override ── */
  div[data-testid="stTextInput"] input {
    background: rgba(8,11,20,.9) !important;
    border: 1px solid rgba(56,189,248,.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .95rem !important;
    padding: .75rem 1rem !important;
    transition: border-color .2s, box-shadow .2s !important;
  }
  div[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.12) !important;
  }
  div[data-testid="stTextInput"] input::placeholder { color: #334155 !important; }

  /* ── Button override ── */
  div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: .95rem !important;
    padding: .65rem 2rem !important;
    letter-spacing: .03em !important;
    transition: opacity .2s, transform .15s !important;
    width: 100%;
    box-shadow: 0 4px 20px rgba(14,165,233,.25) !important;
  }
  div[data-testid="stButton"] > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
  }

  /* ── Pipeline stepper ── */
  .pipeline-wrap {
    display: flex;
    gap: 0;
    align-items: stretch;
    margin: 2rem auto 1.5rem;
    max-width: 900px;
    position: relative;
    z-index: 1;
  }
  .step-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
  }
  .step-item:not(:last-child)::after {
    content: "";
    position: absolute;
    top: 18px;
    left: calc(50% + 18px);
    width: calc(100% - 36px);
    height: 2px;
    background: linear-gradient(90deg, rgba(56,189,248,.35), rgba(56,189,248,.08));
  }
  .step-circle {
    width: 36px; height: 36px;
    border-radius: 50%;
    border: 2px solid rgba(56,189,248,.25);
    background: rgba(15,23,42,.9);
    display: flex; align-items: center; justify-content: center;
    font-size: .8rem; font-weight: 700;
    color: #475569;
    margin-bottom: .5rem;
    transition: all .4s;
    z-index: 1;
  }
  .step-circle.active {
    border-color: #38bdf8;
    background: linear-gradient(135deg, rgba(14,165,233,.2), rgba(99,102,241,.2));
    color: #38bdf8;
    box-shadow: 0 0 18px rgba(56,189,248,.35);
    animation: pulse-step 1.4s ease-in-out infinite;
  }
  .step-circle.done {
    border-color: #34d399;
    background: linear-gradient(135deg, rgba(52,211,153,.2), rgba(16,185,129,.15));
    color: #34d399;
    box-shadow: 0 0 12px rgba(52,211,153,.25);
  }
  @keyframes pulse-step {
    0%, 100% { box-shadow: 0 0 18px rgba(56,189,248,.35); }
    50%       { box-shadow: 0 0 32px rgba(56,189,248,.6); }
  }
  .step-label {
    font-size: .72rem; font-weight: 600;
    letter-spacing: .06em; text-transform: uppercase;
    color: #334155; text-align: center;
    transition: color .4s;
  }
  .step-label.active { color: #38bdf8; }
  .step-label.done   { color: #34d399; }

  /* ── Result cards ── */
  .result-section { position: relative; z-index: 1; margin: 1.5rem 0; }
  .result-card {
    background: rgba(15,23,42,.75);
    border-radius: 14px;
    border: 1px solid rgba(56,189,248,.12);
    padding: 1.6rem 1.8rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 24px rgba(0,0,0,.35);
    animation: fadeSlideUp .5s ease both;
  }
  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .result-card-header {
    display: flex; align-items: center; gap: .7rem;
    margin-bottom: 1rem;
  }
  .result-card-icon {
    width: 34px; height: 34px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
  }
  .icon-search  { background: linear-gradient(135deg,#0ea5e9,#38bdf8); }
  .icon-reader  { background: linear-gradient(135deg,#8b5cf6,#a78bfa); }
  .icon-writer  { background: linear-gradient(135deg,#f59e0b,#fbbf24); }
  .icon-critic  { background: linear-gradient(135deg,#ef4444,#f87171); }
  .result-card-title {
    font-size: .82rem; font-weight: 700;
    letter-spacing: .09em; text-transform: uppercase;
    color: #94a3b8;
  }
  .result-card-step {
    font-size: .7rem; color: #334155; margin-top: .1rem;
  }
  .result-body {
    color: #cbd5e1;
    font-size: .92rem;
    line-height: 1.75;
    white-space: pre-wrap;
    font-family: 'Space Grotesk', sans-serif;
  }
  .result-body.report-body {
    font-size: .95rem;
    color: #e2e8f0;
    background: rgba(8,11,20,.5);
    border-radius: 8px;
    padding: 1.2rem;
    border-left: 3px solid #f59e0b;
  }
  .result-body.critic-body {
    border-left: 3px solid #ef4444;
    background: rgba(239,68,68,.04);
    border-radius: 8px;
    padding: 1.2rem;
  }

  /* ── Status bar ── */
  .status-bar {
    display: flex; align-items: center; gap: .6rem;
    background: rgba(15,23,42,.9);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 8px;
    padding: .55rem 1rem;
    margin: 1rem auto;
    max-width: 760px;
    font-size: .82rem; color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    position: relative; z-index: 1;
  }
  .status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #38bdf8;
    animation: blink 1s ease-in-out infinite;
    flex-shrink: 0;
  }
  @keyframes blink {
    0%,100% { opacity: 1; } 50% { opacity: .2; }
  }

  /* ── Divider ── */
  .fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,.2), transparent);
    margin: 2rem 0;
  }

  /* ── Streamlit expander override ── */
  details {
    background: rgba(15,23,42,.6) !important;
    border: 1px solid rgba(56,189,248,.12) !important;
    border-radius: 10px !important;
  }
  details summary {
    color: #94a3b8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .88rem !important;
    font-weight: 600 !important;
  }

  /* ── Footer ── */
  .footer {
    text-align: center;
    color: #1e293b;
    font-size: .78rem;
    padding: 3rem 0 2rem;
    position: relative; z-index: 1;
    letter-spacing: .04em;
  }

  /* hide streamlit chrome ── */
  #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⬡ Multi-Agent Research System</div>
  <h1 class="hero-title">ResearchMind AI</h1>
  <p class="hero-sub">Four specialized agents. One definitive research report.</p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline stepper (static labels, state driven) ────────────────────────────
STEPS = [
    ("🔍", "Search Agent"),
    ("📄", "Reader Agent"),
    ("✍️", "Writer Chain"),
    ("🔬", "Critic Chain"),
]

def render_pipeline(active: int, done_up_to: int):
    """Render the step indicator. active=0-3 (current), done_up_to=steps finished."""
    circles = ""
    for i, (icon, label) in enumerate(STEPS):
        if i < done_up_to:
            cls_c, cls_l = "done", "done"
            disp = "✓"
        elif i == active:
            cls_c, cls_l = "active", "active"
            disp = str(i + 1)
        else:
            cls_c, cls_l = "", ""
            disp = str(i + 1)

        circles += f"""
        <div class="step-item">
          <div class="step-circle {cls_c}">{disp}</div>
          <div class="step-label {cls_l}">{label}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-wrap">{circles}</div>', unsafe_allow_html=True)


# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Research Topic</div>', unsafe_allow_html=True)

col_inp, col_btn = st.columns([4, 1])
with col_inp:
    topic = st.text_input(
        label="topic_hidden",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_input",
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)   # align vertically
    run_btn = st.button("⚡ Run Pipeline", key="run_btn")

st.markdown('</div>', unsafe_allow_html=True)  # /input-card


# ── Session state ──────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "error" not in st.session_state:
    st.session_state.error = None


# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.results = None
    st.session_state.error = None
    st.session_state.running = True

    placeholder = st.empty()

    def show_status(msg, step_active, step_done):
        with placeholder.container():
            render_pipeline(step_active, step_done)
            st.markdown(f"""
            <div class="status-bar">
              <div class="status-dot"></div>
              <span>{msg}</span>
            </div>""", unsafe_allow_html=True)

    try:
        # Step 1
        show_status("Search agent scanning the web for sources…", 0, 0)
        # We run the real pipeline but capture intermediate via our wrapper
        # For seamless UX we run the whole pipeline and update steps via timing
        import threading, queue

        result_q: queue.Queue = queue.Queue()

        def _run():
            try:
                result_q.put(("ok", run_research_pipeline(topic.strip())))
            except Exception as exc:
                result_q.put(("err", str(exc)))

        t = threading.Thread(target=_run, daemon=True)
        t.start()

        # Animated status while waiting
        step_msgs = [
            (0, 0, "Search agent scanning the web for reliable sources…"),
            (1, 1, "Reader agent scraping top URL for deep content…"),
            (2, 2, "Writer chain drafting the full research report…"),
            (3, 3, "Critic chain reviewing and scoring the report…"),
        ]
        msg_idx = 0
        while t.is_alive():
            sa, sd, sm = step_msgs[min(msg_idx, 3)]
            show_status(sm, sa, sd)
            time.sleep(6)
            if msg_idx < 3:
                msg_idx += 1

        t.join()
        status, payload = result_q.get()

        placeholder.empty()

        if status == "ok":
            st.session_state.results = payload
        else:
            st.session_state.error = payload

    except Exception as e:
        placeholder.empty()
        st.session_state.error = str(e)

    st.session_state.running = False
    st.rerun()

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic first.")


# ── Show error ─────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
    <div class="result-card" style="border-color:rgba(239,68,68,.3);margin-top:1rem;">
      <div class="result-card-header">
        <div class="result-card-icon icon-critic">⚠️</div>
        <div>
          <div class="result-card-title">Pipeline Error</div>
          <div class="result-card-step">Something went wrong</div>
        </div>
      </div>
      <div class="result-body critic-body">{st.session_state.error}</div>
    </div>""", unsafe_allow_html=True)


# ── Show results ───────────────────────────────────────────────────────────────
if st.session_state.results:
    res = st.session_state.results
    render_pipeline(3, 4)   # all done

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ── Layout: two columns on top, full width below ──
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        # Search results
        st.markdown("""
        <div class="result-section">
          <div class="result-card">
            <div class="result-card-header">
              <div class="result-card-icon icon-search">🔍</div>
              <div>
                <div class="result-card-title">Search Results</div>
                <div class="result-card-step">Step 1 — Search Agent</div>
              </div>
            </div>""", unsafe_allow_html=True)

        search_text = res.get("search_results", "No data returned.")
        with st.expander("View raw search output", expanded=False):
            st.markdown(f'<div class="result-body">{search_text[:2000]}{"…" if len(search_text)>2000 else ""}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_r:
        # Scraped content
        st.markdown("""
        <div class="result-section">
          <div class="result-card">
            <div class="result-card-header">
              <div class="result-card-icon icon-reader">📄</div>
              <div>
                <div class="result-card-title">Scraped Content</div>
                <div class="result-card-step">Step 2 — Reader Agent</div>
              </div>
            </div>""", unsafe_allow_html=True)

        scraped_text = res.get("scraped_content", "No data returned.")
        with st.expander("View scraped page content", expanded=False):
            st.markdown(f'<div class="result-body">{scraped_text[:2000]}{"…" if len(scraped_text)>2000 else ""}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # Full-width report
    report_text = res.get("report", "No report generated.")
    st.markdown(f"""
    <div class="result-section">
      <div class="result-card">
        <div class="result-card-header">
          <div class="result-card-icon icon-writer">✍️</div>
          <div>
            <div class="result-card-title">Research Report</div>
            <div class="result-card-step">Step 3 — Writer Chain</div>
          </div>
        </div>
        <div class="result-body report-body">{report_text}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # Critic feedback
    feedback_text = res.get("feedback", "No feedback generated.")
    st.markdown(f"""
    <div class="result-section">
      <div class="result-card">
        <div class="result-card-header">
          <div class="result-card-icon icon-critic">🔬</div>
          <div>
            <div class="result-card-title">Critic Review</div>
            <div class="result-card-step">Step 4 — Critic Chain</div>
          </div>
        </div>
        <div class="result-body critic-body">{feedback_text}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Download button
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    dl_col, _, _ = st.columns([1, 2, 2])
    with dl_col:
        full_output = f"""ResearchMind AI — Report
{'='*60}
Topic: {topic}
{'='*60}

SEARCH RESULTS:
{res.get('search_results','')}

SCRAPED CONTENT:
{res.get('scraped_content','')}

RESEARCH REPORT:
{res.get('report','')}

CRITIC FEEDBACK:
{res.get('feedback','')}
"""
        st.download_button(
            label="⬇ Download Report",
            data=full_output,
            file_name=f"research_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain",
        )


# ── Idle state ─────────────────────────────────────────────────────────────────
if not st.session_state.results and not st.session_state.error:
    render_pipeline(-1, 0)
    st.markdown("""
    <div style="text-align:center;color:#1e293b;font-size:.82rem;
                letter-spacing:.06em;margin-top:1rem;position:relative;z-index:1;">
      ENTER A TOPIC ABOVE AND HIT RUN TO BEGIN
    </div>""", unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  ResearchMind AI &nbsp;·&nbsp; Search → Read → Write → Critique
</div>""", unsafe_allow_html=True)