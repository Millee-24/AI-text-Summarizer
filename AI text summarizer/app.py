import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(
    page_title="NLP Summarizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp { background: #0a0a0f; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.hero {
    background: #0a0a0f;
    padding: 5rem 4rem 3rem;
    border-bottom: 1px solid #1e1e2e;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    color: #f0f0f5;
    line-height: 1.1;
    margin: 0 0 1rem;
}

.hero-title span { color: #5DCAA5; }

.hero-sub {
    font-size: 1.1rem;
    color: #888;
    max-width: 560px;
    line-height: 1.7;
}

.input-zone {
    padding: 3rem 4rem;
    background: #0d0d15;
    border-bottom: 1px solid #1e1e2e;
}

.step-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5DCAA5;
    margin-bottom: 0.6rem;
}

.card {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}

.card:hover { border-color: #2e2e4e; }

.persona-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 0.5rem;
}

.persona-btn {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}

.persona-btn.active-researcher { border-color: #5DCAA5; background: #0f1e1a; }
.persona-btn.active-student    { border-color: #378ADD; background: #0f151e; }
.persona-btn.active-teacher    { border-color: #EF9F27; background: #1e160f; }
.persona-btn.active-child      { border-color: #D85A30; background: #1e130f; }

.persona-icon { font-size: 1.8rem; margin-bottom: 6px; }
.persona-name { font-size: 13px; font-weight: 500; color: #d0d0e0; }
.persona-desc { font-size: 11px; color: #666; margin-top: 2px; }

.summarize-btn {
    width: 100%;
    padding: 1rem 2rem;
    background: #5DCAA5;
    color: #0a0a0f;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    letter-spacing: 0.5px;
    margin-top: 1rem;
    transition: background 0.2s;
}

.summarize-btn:hover { background: #4db896; }

.results-zone {
    padding: 3rem 4rem;
    background: #0a0a0f;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 2.5rem;
}

.stat-card {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}

.stat-num {
    font-size: 24px;
    font-weight: 600;
    color: #f0f0f5;
    line-height: 1.2;
}

.stat-num.green  { color: #5DCAA5; }
.stat-num.blue   { color: #378ADD; }
.stat-num.amber  { color: #EF9F27; }

.stat-lbl {
    font-size: 11px;
    color: #666;
    margin-top: 4px;
    letter-spacing: 0.5px;
}

.summary-card {
    background: #12121c;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 2rem;
    line-height: 1.9;
    font-size: 15px;
    color: #c8c8d8;
    margin-bottom: 1.5rem;
}

.summary-card mark {
    background: #ffd60030;
    color: #ffd600;
    border-radius: 3px;
    padding: 0 3px;
}

.translation-card {
    background: #0f1e1a;
    border: 1px solid #1D9E7540;
    border-radius: 16px;
    padding: 2rem;
    line-height: 1.9;
    font-size: 15px;
    color: #9FE1CB;
    margin-bottom: 1.5rem;
}

.kw-chip {
    display: inline-block;
    background: #1a1a0a;
    border: 1px solid #ffd60040;
    color: #ffd600;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px 3px;
    font-weight: 500;
}

.section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5DCAA5;
    margin-bottom: 1rem;
}

.dl-btn {
    display: inline-block;
    background: #12121c;
    border: 1px solid #2e2e4e;
    color: #d0d0e0;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 13px;
    cursor: pointer;
    text-decoration: none;
    transition: border-color 0.2s;
}

.dl-btn:hover { border-color: #5DCAA5; color: #5DCAA5; }

.stTextArea textarea {
    background: #0d0d15 !important;
    color: #d0d0e0 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}

.stTextInput input {
    background: #0d0d15 !important;
    color: #d0d0e0 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div {
    background: #12121c !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
    color: #d0d0e0 !important;
}

.stRadio > div { gap: 0 !important; }
.stRadio label { color: #888 !important; }

.stButton > button {
    background: #5DCAA5 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #4db896 !important;
    transform: translateY(-1px) !important;
}

.stProgress > div > div { background: #5DCAA5 !important; }

div[data-testid="stFileUploader"] {
    background: #12121c !important;
    border: 1px dashed #2e2e4e !important;
    border-radius: 12px !important;
}

.stAlert { border-radius: 12px !important; }

h1, h2, h3 { color: #f0f0f5 !important; }

.stDownloadButton > button {
    background: #12121c !important;
    color: #d0d0e0 !important;
    border: 1px solid #2e2e4e !important;
    border-radius: 10px !important;
    font-size: 13px !important;
}

.stDownloadButton > button:hover {
    border-color: #5DCAA5 !important;
    color: #5DCAA5 !important;
}

.spinner-text { color: #5DCAA5 !important; }

.stSpinner > div { border-top-color: #5DCAA5 !important; }
</style>
""", unsafe_allow_html=True)

PERSONAS = {
    "Researcher": {"icon": "🔬", "desc": "Technical and precise",  "color": "#5DCAA5"},
    "Student":    {"icon": "📚", "desc": "Exam-ready concepts",    "color": "#378ADD"},
    "Teacher":    {"icon": "🎓", "desc": "Structured and clear",   "color": "#EF9F27"},
    "Child":      {"icon": "🌟", "desc": "Simple and friendly",    "color": "#D85A30"},
}

LANGUAGES = {
    "Hindi": "hi", "Punjabi": "pa", "French": "fr",
    "Spanish": "es", "German": "de", "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN", "Tamil": "ta",
    "Telugu": "te", "Bengali": "bn", "Japanese": "ja",
    "Korean": "ko", "Portuguese": "pt", "Russian": "ru",
    "Italian": "it", "Turkish": "tr", "Urdu": "ur",
    "Marathi": "mr", "Gujarati": "gu", "Kannada": "kn",
}

if "persona" not in st.session_state:
    st.session_state.persona = "Researcher"

st.markdown("""
<div class="hero">
    <div class="hero-title">Read less.<br><span>Know more.</span></div>
    <p class="hero-sub">
        Paste any text, drop a URL, or upload a PDF.
        Get a summary tuned to how you think — researcher, student, teacher, or child.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-zone">', unsafe_allow_html=True)

col_in, col_settings = st.columns([3, 2], gap="large")

with col_in:
    st.markdown('<div class="step-label">Step 1 — your content</div>', unsafe_allow_html=True)

    tab_text, tab_url, tab_pdf = st.tabs(["✍️  Text", "🔗  URL", "📄  PDF"])
    raw_text = None

    with tab_text:
        user_text = st.text_area(
            "text_input",
            height=180,
            placeholder="Paste any article, research paper, or passage here...",
            label_visibility="collapsed"
        )
        if user_text.strip():
            raw_text = user_text.strip()

    with tab_url:
        url_input = st.text_input(
            "url_input",
            placeholder="https://en.wikipedia.org/wiki/...",
            label_visibility="collapsed"
        )
        if url_input.strip():
            with st.spinner("Fetching content..."):
                try:
                    from scraper import get_text
                    raw_text = get_text("url", url=url_input.strip())
                    if raw_text:
                        st.success(f"Fetched {len(raw_text.split()):,} words")
                    else:
                        st.error("Could not extract text. Try a Wikipedia article.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab_pdf:
        uploaded = st.file_uploader(
            "pdf_upload",
            type=["pdf"],
            label_visibility="collapsed"
        )
        if uploaded:
            with st.spinner("Reading PDF..."):
                try:
                    import pdfplumber
                    with pdfplumber.open(uploaded) as pdf:
                        raw_text = " ".join(
                            p.extract_text() for p in pdf.pages if p.extract_text()
                        )
                    if raw_text:
                        st.success(f"Extracted {len(raw_text.split()):,} words")
                    else:
                        st.error("Could not read this PDF.")
                        raw_text = None
                except ImportError:
                    st.error("Run: pip install pdfplumber")
                except Exception as e:
                    st.error(f"Error: {e}")

with col_settings:
    st.markdown('<div class="step-label">Step 2 — who are you?</div>', unsafe_allow_html=True)

    p_cols = st.columns(2)
    persona_list = list(PERSONAS.keys())

    for i, p in enumerate(persona_list):
        with p_cols[i % 2]:
            active = "active-" + p.lower() if st.session_state.persona == p else ""
            color = PERSONAS[p]["color"]
            border = color if st.session_state.persona == p else "#1e1e2e"
            bg = color + "15" if st.session_state.persona == p else "#12121c"

            st.markdown(
                f'<div style="background:{bg}; border:1px solid {border}; '
                f'border-radius:12px; padding:1rem; text-align:center; margin-bottom:8px">'
                f'<div style="font-size:1.6rem">{PERSONAS[p]["icon"]}</div>'
                f'<div style="font-size:13px; font-weight:500; color:#d0d0e0; margin:4px 0">{p}</div>'
                f'<div style="font-size:11px; color:#666">{PERSONAS[p]["desc"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(f"Select {p}", key=f"p_{p}", use_container_width=True):
                st.session_state.persona = p
                st.rerun()

    st.markdown('<div class="step-label" style="margin-top:1.5rem">Step 3 — translate to</div>', unsafe_allow_html=True)
    language = st.selectbox(
        "Language",
        ["None — keep in English"] + list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div style="padding: 0 4rem 2rem">', unsafe_allow_html=True)
summarize_btn = st.button("✦  Summarize now", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if summarize_btn:
    if not raw_text or not raw_text.strip():
        st.markdown('<div style="padding:0 4rem">', unsafe_allow_html=True)
        st.warning("Add some content first — paste text, a URL, or a PDF.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        persona = st.session_state.persona

        st.markdown('<div class="results-zone">', unsafe_allow_html=True)

        try:
            from preprocessor import clean_text
            from summarizer import summarize_text
            from keywords import extract_keywords, highlight_keywords, generate_wordcloud
            from persona import rewrite_the_summary_for_persona, calculate_persona_stats
            from translator import summary_translation, translate_keywords

            prog = st.progress(0, text="Cleaning text...")

            cleaned = clean_text(raw_text)
            prog.progress(15, text="Summarizing with LexRank...")

            if not cleaned:
                st.error("Text is empty after cleaning.")
                st.stop()

            summary, stats = summarize_text(cleaned)
            word_limit = stats["Summary_words"]
            prog.progress(35, text="Extracting keywords with YAKE...")

            ranked_kw, ranked_scores = extract_keywords(cleaned)
            prog.progress(55, text=f"Adapting for {persona} with Gemini...")

            persona_summary = rewrite_the_summary_for_persona(
                summary=summary, persona=persona, word_limit=word_limit
            )
            persona_stats = calculate_persona_stats(summary, persona_summary)
            prog.progress(80, text="Highlighting and translating...")

            highlighted = highlight_keywords(persona_summary, ranked_kw)

            lang_key = language if language != "None — keep in English" else "None"
            translated_text = None
            display_kw = ranked_kw

            if lang_key != "None":
                translated_text = summary_translation(
                    persona_summary=persona_summary,
                    target=LANGUAGES[lang_key]
                )
                display_kw = translate_keywords(ranked_kw, target=LANGUAGES[lang_key])

            prog.progress(100, text="Done")
            prog.empty()

            total_comp = round(
                (1 - persona_stats["persona_words"] / stats["Original_words"]) * 100
            ) if stats["Original_words"] > 0 else 0

            p_color = PERSONAS[persona]["color"]

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-num">{stats["Original_words"]:,}</div>
                    <div class="stat-lbl">Original words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-num blue">{stats["Summary_words"]:,}</div>
                    <div class="stat-lbl">After LexRank</div>
                </div>
                <div class="stat-card">
                    <div class="stat-num green">{persona_stats["persona_words"]:,}</div>
                    <div class="stat-lbl">After persona</div>
                </div>
                <div class="stat-card">
                    <div class="stat-num amber">{stats["Original_words"] - persona_stats["persona_words"]:,}</div>
                    <div class="stat-lbl">Words removed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-num green">{total_comp}%</div>
                    <div class="stat-lbl">Compression</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_sum, col_side = st.columns([3, 2], gap="large")

            with col_sum:
                st.markdown(
                    f'<div class="step-label">{PERSONAS[persona]["icon"]} Summary — {persona}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="summary-card" style="border-color:{p_color}40">'
                    f'{highlighted}</div>',
                    unsafe_allow_html=True
                )

                if translated_text:
                    st.markdown(
                        f'<div class="step-label">🌐 Translation — {lang_key}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="translation-card">{translated_text}</div>',
                        unsafe_allow_html=True
                    )

                dl1, dl2 = st.columns(2)
                with dl1:
                    st.download_button(
                        "⬇ Download summary",
                        data=persona_summary,
                        file_name=f"summary_{persona.lower()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with dl2:
                    if translated_text:
                        st.download_button(
                            f"⬇ Download ({lang_key})",
                            data=translated_text,
                            file_name=f"translation_{lang_key.lower()}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

            with col_side:
                st.markdown('<div class="step-label">🔑 Keywords</div>', unsafe_allow_html=True)
                chips = "".join(
                    f'<span class="kw-chip">{kw}</span>' for kw in display_kw
                )
                st.markdown(
                    f'<div style="line-height:2.6; margin-bottom:1.5rem">{chips}</div>',
                    unsafe_allow_html=True
                )

                st.markdown('<div class="step-label">☁ Word cloud</div>', unsafe_allow_html=True)
                if display_kw:
                    wc_text = " ".join(display_kw)
                    wc = WordCloud(
                        width=700, height=360,
                        background_color="#12121c",
                        colormap="cool",
                        max_words=30,
                        prefer_horizontal=0.9
                    )
                    wc_img = wc.generate(wc_text)
                    fig, ax = plt.subplots(figsize=(7, 3.6))
                    ax.imshow(wc_img, interpolation="bilinear")
                    ax.axis("off")
                    fig.patch.set_facecolor("#12121c")
                    ax.set_facecolor("#12121c")
                    st.pyplot(fig)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Check your GEMINI_API_KEY in environment variables.")

        st.markdown("</div>", unsafe_allow_html=True)