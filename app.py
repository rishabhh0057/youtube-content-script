import streamlit as st
import html
import urllib.parse

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="YouTube Script Generator Studio Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. SIDEBAR CONFIGURATION & ADJUSTABLE COLUMN SLIDERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## ⚙️ Studio Layout Controls")

theme_choice = st.sidebar.selectbox(
    "🎨 UI Theme Engine",
    ["Midnight Cyberpunk", "Dark Glassmorphism", "Clean Studio Light"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Grid Workspace Resizer")
left_col_ratio = st.sidebar.slider(
    "Inputs vs Output Split Ratio",
    min_value=25,
    max_value=75,
    value=40,
    step=5,
    help="Drag to adjust the width balance between the parameter panel and the script studio preview."
)

right_col_ratio = 100 - left_col_ratio
st.sidebar.caption(f"Layout Ratio: **{left_col_ratio}% Inputs | {right_col_ratio}% Preview**")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")
st.sidebar.info(
    "• **Teleprompter Mode** gives you a full-width presentation view.\n"
    "• Use **Custom Rules** to enforce specific B-roll or sponsorship placements."
)

# -----------------------------------------------------------------------------
# 3. ADVANCED CUSTOM CSS FOR MAXIMUM VISUAL APPEAL
# -----------------------------------------------------------------------------
def inject_custom_css(theme):
    if theme == "Midnight Cyberpunk":
        bg_color = "#070913"
        card_bg = "rgba(18, 24, 43, 0.75)"
        text_color = "#F3F4F6"
        accent_gradient = "linear-gradient(135deg, #FF007F 0%, #7928CA 100%)"
        accent_border = "rgba(255, 0, 127, 0.3)"
        subtle_text = "#9CA3AF"
    elif theme == "Dark Glassmorphism":
        bg_color = "#0F172A"
        card_bg = "rgba(30, 41, 59, 0.7)"
        text_color = "#F8FAFC"
        accent_gradient = "linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)"
        accent_border = "rgba(59, 130, 246, 0.3)"
        subtle_text = "#94A3B8"
    else:  # Clean Studio Light
        bg_color = "#F8FAFC"
        card_bg = "#FFFFFF"
        text_color = "#0F172A"
        accent_gradient = "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"
        accent_border = "#E2E8F0"
        subtle_text = "#64748B"

    css = f"""
    <style>
    /* Global App Container */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Premium Glassmorphic Card Blocks */
    .styled-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid {accent_border};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    /* Hero Gradient Title */
    .hero-title {{
        font-size: 2.5rem;
        font-weight: 900;
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }}
    
    .hero-subtitle {{
        color: {subtle_text};
        font-size: 1.05rem;
        margin-bottom: 24px;
    }}
    
    /* Script Section Cards */
    .script-section {{
        border-left: 4px solid #3B82F6;
        background: rgba(255, 255, 255, 0.03);
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 18px;
    }}
    
    .visual-cue {{
        background: rgba(245, 158, 11, 0.15);
        border: 1px dashed #F59E0B;
        color: #FBBF24;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin-bottom: 8px;
        display: inline-block;
    }}

    /* Stat Pill Badge */
    .metric-pill {{
        background: {accent_gradient};
        color: white;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-right: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}

    /* Teleprompter Box */
    .teleprompter-box {{
        background: #000000;
        color: #00FF66;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.35rem;
        line-height: 1.8;
        padding: 28px;
        border-radius: 16px;
        border: 2px solid #00FF66;
        height: 400px;
        overflow-y: scroll;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.2);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css(theme_choice)

# -----------------------------------------------------------------------------
# 4. APP HEADER & LAYOUT INITIALIZATION
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">🎬 YouTube Script Studio Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Craft viral, high-retention video scripts tailored precisely to your target audience.</div>', unsafe_allow_html=True)

# Interactive columns dynamic sizing
col_inputs, col_preview = st.columns([left_col_ratio, right_col_ratio], gap="large")

# Session state handling
if "script_plain" not in st.session_state:
    st.session_state.script_plain = ""
if "word_count" not in st.session_state:
    st.session_state.word_count = 0
if "hook_text" not in st.session_state:
    st.session_state.hook_text = ""
if "intro_text" not in st.session_state:
    st.session_state.intro_text = ""
if "body_text" not in st.session_state:
    st.session_state.body_text = ""
if "outro_text" not in st.session_state:
    st.session_state.outro_text = ""

# -----------------------------------------------------------------------------
# 5. INPUT FORM COLUMN
# -----------------------------------------------------------------------------
with col_inputs:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.markdown("### 📌 Script Builder Parameters")
    
    topic = st.text_input("🎥 Video Topic / Title", placeholder="e.g. 10 AI Productivity Tools to Automate Your Life")
    
    c1, c2 = st.columns(2)
    with c1:
        target_age = st.selectbox(
            "👥 Target Age Group",
            ["Teens (13-17)", "Young Adults (18-24)", "Adults (25-34)", "Middle-Aged (35-50)", "Seniors (50+)"],
            index=1
        )
    with c2:
        target_gender = st.selectbox(
            "🎯 Audience Gender Focus",
            ["All Audiences", "Male", "Female", "Inclusive / Non-Binary"]
        )
        
    pacing_tone = st.selectbox(
        "⚡ Video Pacing & Style",
        ["Fast & Dynamic (Tech/MrBeast style)", "Educational & In-depth (Documentary style)", "Storytelling & Conversational (Vlog style)", "Professional & Executive"]
    )
    
    custom_features = st.text_area(
        "📝 Custom Script Directives",
        placeholder="e.g., Mention a sponsor at 2:00, include sound effect cues, use humor...",
        height=130
    )
    
    generate_btn = st.button("🚀 Generate High-Retention Script", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. GENERATION LOGIC
# -----------------------------------------------------------------------------
if generate_btn:
    topic_val = topic if topic else "Untitled YouTube Video"
    custom_val = custom_features if custom_features else "Standard high-retention video style."
    
    st.session_state.hook_text = f"If you're still doing {topic_val} the old way, you are wasting hours every week! In this video, I'm revealing the step-by-step secret strategy."
    st.session_state.intro_text = f"Welcome back to the channel! Tailored specifically for our {target_age} viewers, today we are breaking down everything you need to know about {topic_val}."
    st.session_state.body_text = f"Rule #1: Focus on core fundamentals.\nRule #2: Avoid the critical mistakes that most {target_gender} creators make.\nRule #3: Apply this actionable pro-tip immediately."
    st.session_state.outro_text = f"If this helped you out, drop a like and hit subscribe for more content on {topic_val}. See you in the next one!"
    
    st.session_state.script_plain = f"""TITLE: {topic_val}
AUDIENCE: {target_age} | {target_gender}
PACING: {pacing_tone}
DIRECTIVES: {custom_val}

--- 1. THE HOOK (0:00 - 0:15) ---
Visual: Fast push-in zoom on creator, high energy sound effect.
Dialogue: "{st.session_state.hook_text}"

--- 2. INTRO & VALUE PROPOSITION (0:15 - 0:45) ---
Visual: Kinetic typography title card on screen.
Dialogue: "{st.session_state.intro_text}"

--- 3. CORE CONTENT (0:45 - 4:00) ---
Visual: Screen recording or B-roll overlays matching points.
Directive Note: {custom_val}
Dialogue / Points:
{st.session_state.body_text}

--- 4. CALL TO ACTION & OUTRO (4:00 - End) ---
Visual: Animated subscribe button overlay & End-screen video cards.
Dialogue: "{st.session_state.outro_text}"
""".strip()

    st.session_state.word_count = len(st.session_state.script_plain.split())

# -----------------------------------------------------------------------------
# 7. OUTPUT PREVIEW & SCRIPT DASHBOARD
# -----------------------------------------------------------------------------
with col_preview:
    if st.session_state.script_plain:
        st.markdown('<div class="styled-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Script Analytics Dashboard")
        
        est_minutes = round(st.session_state.word_count / 130, 1)
        
        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <span class="metric-pill">⏱️ Est. Duration: ~{est_minutes} min</span>
            <span class="metric-pill">📝 Word Count: {st.session_state.word_count}</span>
            <span class="metric-pill">⚡ Target Pacing: 130 WPM</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabs for Studio Script View vs Teleprompter
        tab_formatted, tab_teleprompter, tab_export = st.tabs(["🎬 Studio View", "📺 Teleprompter Mode", "📥 Export & Share"])
        
        with tab_formatted:
            st.markdown('<div class="styled-card">', unsafe_allow_html=True)
            st.markdown(f"<h2>📹 {html.escape(topic if topic else 'Untitled Video')}</h2>")
            st.caption(f"Target: **{target_age}** | **{target_gender}** | Style: **{pacing_tone}**")
            st.divider()
            
            # Hook Card
            st.markdown("""
            <div class="script-section">
                <h4>🔥 1. The Hook (0:00 - 0:15)</h4>
                <div class="visual-cue">🎥 VISUAL: Fast push-in camera zoom, sound effect burst</div>
                <p><strong>Dialogue:</strong> "{hook}"</p>
            </div>
            """.format(hook=html.escape(st.session_state.hook_text)), unsafe_allow_html=True)
            
            # Intro Card
            st.markdown("""
            <div class="script-section">
                <h4>📍 2. Intro & Value Proposition (0:15 - 0:45)</h4>
                <div class="visual-cue">🎥 VISUAL: Kinetic text overlay on screen</div>
                <p><strong>Dialogue:</strong> "{intro}"</p>
            </div>
            """.format(intro=html.escape(st.session_state.intro_text)), unsafe_allow_html=True)
            
            # Body Card
            st.markdown("""
            <div class="script-section">
                <h4>💡 3. Core Content (0:45 - 4:00)</h4>
                <div class="visual-cue">🎥 VISUAL: Relevant B-roll footage / Product demonstrations</div>
                <p><strong>Content Outline:</strong></p>
                <p style="white-space: pre-line;">{body}</p>
            </div>
            """.format(body=html.escape(st.session_state.body_text)), unsafe_allow_html=True)
            
            # Outro Card
            st.markdown("""
            <div class="script-section">
                <h4>📢 4. Call to Action & Outro</h4>
                <div class="visual-cue">🎥 VISUAL: End screen video recommendations card</div>
                <p><strong>Dialogue:</strong> "{outro}"</p>
            </div>
            """.format(outro=html.escape(st.session_state.outro_text)), unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_teleprompter:
            st.markdown('<div class="styled-card">', unsafe_allow_html=True)
            st.markdown("### 📺 High-Contrast Teleprompter Mode")
            st.caption("Scroll down as you present directly to your camera lens.")
            
            teleprompter_content = f"""
{st.session_state.hook_text.upper()}

[ PAUSE - INTRO TITLE CARD ]

{st.session_state.intro_text}

[ CORE POINTS ]

{st.session_state.body_text}

[ OUTRO & CTA ]

{st.session_state.outro_text}
            """
            st.markdown(f'<div class="teleprompter-box">{html.escape(teleprompter_content).replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_export:
            st.markdown('<div class="styled-card">', unsafe_allow_html=True)
            st.markdown("### 📥 Download Script Formats")
            d1, d2, d3 = st.columns(3)
            
            # 1. Markdown
            d1.download_button("📄 Download .MD", data=st.session_state.script_plain.encode("utf-8"), file_name="script.md", mime="text/markdown", use_container_width=True)
            
            # 2. Text File
            d2.download_button("📝 Download .TXT", data=st.session_state.script_plain.encode("utf-8"), file_name="script.txt", mime="text/plain", use_container_width=True)
            
            # 3. Teleprompter Text
            d3.download_button("📺 Teleprompter Script", data=teleprompter_content.encode("utf-8"), file_name="teleprompter.txt", mime="text/plain", use_container_width=True)

            st.divider()
            st.markdown("### ✉️ Quick Share Links")
            s1, s2 = st.columns(2)
            
            wa_text = urllib.parse.quote(f"Check out my new YouTube Script:\n\n{st.session_state.script_plain[:250]}...")
            wa_url = f"https://api.whatsapp.com/send?text={wa_text}"
            s1.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 Share via WhatsApp</button></a>', unsafe_allow_html=True)
            
            mail_sub = urllib.parse.quote(f"YouTube Script: {topic if topic else 'New Video'}")
            mail_body = urllib.parse.quote(st.session_state.script_plain)
            mail_url = f"mailto:?subject={mail_sub}&body={mail_body}"
            s2.markdown(f'<a href="{mail_url}"><button style="width:100%; background:#2563EB; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; cursor:pointer;">✉️ Send via Email</button></a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="styled-card">', unsafe_allow_html=True)
        st.info("👈 Enter your video details on the left and click **Generate High-Retention Script** to open your script dashboard.")
        st.markdown('</div>', unsafe_allow_html=True)
