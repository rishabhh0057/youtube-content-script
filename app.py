import streamlit as st
import html
import urllib.parse
import os
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import moviepy as mp

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="YouTube Script & Asset Generator Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. SIDEBAR CONFIGURATION & ADJUSTABLE COLUMN SLIDERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## ⚙️ Layout & Theme Controls")

# Custom Theme Selector
theme_choice = st.sidebar.selectbox("🎨 App Theme", ["Dark Glass", "Cyberpunk Neon", "Light Clean"])

# Dynamic Column Width Slider
st.sidebar.markdown("### 📐 Adjustable Layout Grid")
left_col_ratio = st.sidebar.slider(
    "Input Panel Width vs Preview Panel Width",
    min_value=20,
    max_value=80,
    value=45,
    step=5,
    help="Adjust the slider ratio to widen or narrow the input form and preview columns dynamically!"
)

right_col_ratio = 100 - left_col_ratio
st.sidebar.caption(f"Current Layout Ratio: **{left_col_ratio}% : {right_col_ratio}%**")

# -----------------------------------------------------------------------------
# 3. ADVANCED CUSTOM CSS FOR PREMIUM BEAUTIFICATION
# -----------------------------------------------------------------------------
def inject_custom_css(theme):
    if theme == "Dark Glass":
        bg_color = "#0B0F19"
        card_bg = "rgba(22, 31, 48, 0.75)"
        text_color = "#F3F4F6"
        accent_color = "#3B82F6"
        border_color = "rgba(255, 255, 255, 0.1)"
    elif theme == "Cyberpunk Neon":
        bg_color = "#090014"
        card_bg = "rgba(24, 0, 46, 0.85)"
        text_color = "#00F0FF"
        accent_color = "#FF007F"
        border_color = "#FF007F"
    else:  # Light Clean
        bg_color = "#F8FAFC"
        card_bg = "#FFFFFF"
        text_color = "#0F172A"
        accent_color = "#2563EB"
        border_color = "#E2E8F0"

    css = f"""
    <style>
    /* Global App Background */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Beautiful Glassmorphic Cards */
    .styled-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }}
    
    /* Styled Headers */
    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }}
    
    /* Speech Duration Badge */
    .metric-badge {{
        display: inline-block;
        background: {accent_color};
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css(theme_choice)

# -----------------------------------------------------------------------------
# 4. HELPER FUNCTIONS FOR ASSET GENERATION (IMAGE & VIDEO)
# -----------------------------------------------------------------------------
def generate_topic_image(topic_text):
    """Generates a styled 1920x1080 banner image for the topic."""
    img = Image.new('RGB', (1920, 1080), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Simple aesthetic layout
    draw.rectangle([60, 60, 1860, 1020], outline=(59, 130, 246), width=8)
    draw.text((120, 450), "YOUTUBE CONTENT ASSET", fill=(255, 75, 75))
    draw.text((120, 520), f"TOPIC: {topic_text[:50]}", fill=(255, 255, 255))
    
    output_img_path = "topic_image.png"
    img.save(output_img_path)
    return output_img_path

def generate_topic_video(topic_text, script_narration):
    """Generates an MP4 video combining gTTS voiceover + image slide using MoviePy 2.0+."""
    # Step A: Synthesize voiceover audio
    tts = gTTS(text=script_narration[:300], lang='en', slow=False)
    audio_path = "voiceover_temp.mp3"
    tts.save(audio_path)
    
    audio_clip = mp.AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Step B: Render visual slide image
    img_path = generate_topic_image(topic_text)

    # Step C: Build video clip (MoviePy v2.0+ compatible API)
    image_clip = mp.ImageClip(img_path).with_duration(duration)
    video_clip = image_clip.with_audio(audio_clip)

    output_video_path = "generated_topic_video.mp4"
    video_clip.write_videofile(output_video_path, fps=24, codec="libx264")

    # Clean up audio resource
    audio_clip.close()
    video_clip.close()
    if os.path.exists(audio_path):
        os.remove(audio_path)
        
    return output_video_path

# -----------------------------------------------------------------------------
# 5. APP HEADER & LAYOUT INITIALIZATION
# -----------------------------------------------------------------------------
st.markdown('<h1 class="main-title">🎬 YouTube Script Generator Pro</h1>', unsafe_allow_html=True)
st.write("Generate high-retention video scripts customized by audience demographics, custom parameters, and AI visual assets.")

# Apply user's custom slider widths to st.columns
col_inputs, col_preview = st.columns([left_col_ratio, right_col_ratio], gap="medium")

# Session state initialization
if "script_html" not in st.session_state:
    st.session_state.script_html = ""
if "script_plain" not in st.session_state:
    st.session_state.script_plain = ""
if "word_count" not in st.session_state:
    st.session_state.word_count = 0
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "generated_video" not in st.session_state:
    st.session_state.generated_video = None

# -----------------------------------------------------------------------------
# 6. INPUT FORM COLUMN
# -----------------------------------------------------------------------------
with col_inputs:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.subheader("📌 Script Parameters")
    
    topic = st.text_input("Video Topic / Title", placeholder="e.g. 10 AI Productivity Tools for 2026")
    
    c1, c2 = st.columns(2)
    with c1:
        target_age = st.selectbox(
            "Target Age",
            ["Teens (13-17)", "Young Adults (18-24)", "Adults (25-34)", "Middle-Aged (35-50)", "Seniors (50+)"],
            index=1
        )
    with c2:
        target_gender = st.selectbox(
            "Target Gender",
            ["All Audiences", "Male-leaning", "Female-leaning", "Inclusive / Non-Binary"]
        )
    
    custom_features = st.text_area(
        "Custom Script Features & Instructions",
        placeholder="e.g., Include comedic B-roll cues, add mid-video CTA at 2 mins, fast pacing...",
        height=120
    )
    
    generate_btn = st.button("🚀 Generate Script", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. GENERATION LOGIC
# -----------------------------------------------------------------------------
if generate_btn:
    topic_val = topic if topic else "Untitled YouTube Video"
    custom_val = custom_features if custom_features else "Standard high-retention video style."
    
    st.session_state.script_html = f"""
    <h2>📹 Title: {html.escape(topic_val)}</h2>
    <p><strong>🎯 Audience:</strong> {target_age} | {target_gender}</p>
    <p><strong>⚡ Custom Rules:</strong> {html.escape(custom_val)}</p>
    <hr>
    
    <h3>🔥 1. The Hook (0:00 - 0:15)</h3>
    <p><strong>Visual Cue:</strong> Dynamic jump cuts, fast push-in camera zoom.</p>
    <p><strong>Dialogue:</strong> "If you think {html.escape(topic_val)} is hard, you are doing it wrong. In this video, I'm revealing the exact step-by-step strategy!"</p>
    
    <h3>📍 2. Intro & Value Proposition (0:15 - 0:45)</h3>
    <p><strong>Visual Cue:</strong> Title card overlay with key take-aways on screen.</p>
    <p><strong>Dialogue:</strong> "Welcome back! Tailored specifically for our {target_age} audience, today we're uncovering secrets most creators skip."</p>
    
    <h3>💡 3. Core Content & Main Body (0:45 - 4:00)</h3>
    <p><strong>Custom Applied Rule:</strong> <em>{html.escape(custom_val)}</em></p>
    <ul>
        <li><strong>Point 1:</strong> Foundational breakdown of {html.escape(topic_val)}.</li>
        <li><strong>Point 2:</strong> Major mistakes to avoid for {target_gender} creators.</li>
        <li><strong>Point 3:</strong> Actionable pro-tip you can implement today.</li>
    </ul>
    
    <h3>📢 4. Call To Action & Outro (4:00 - End)</h3>
    <p><strong>Visual Cue:</strong> End-screen cards pointing to recommended videos.</p>
    <p><strong>Dialogue:</strong> "If you found this helpful, hit the Like button and subscribe for more content customized for you!"</p>
    """.strip()

    st.session_state.script_plain = f"""
Title: {topic_val}
Audience: {target_age} | {target_gender}
Custom Instructions: {custom_val}

--- 1. THE HOOK (0:00 - 0:15) ---
Visual: Dynamic jump cuts, camera zoom.
Dialogue: "If you think {topic_val} is hard, you are doing it wrong. In this video, I'm revealing the exact step-by-step strategy!"

--- 2. INTRO & VALUE PROPOSITION (0:15 - 0:45) ---
Visual: Title card overlay.
Dialogue: "Welcome back! Tailored specifically for our {target_age} audience, today we're uncovering secrets most creators skip."

--- 3. CORE CONTENT (0:45 - 4:00) ---
Custom Feature: {custom_val}
- Point 1: Foundational breakdown of {topic_val}.
- Point 2: Major mistakes to avoid for {target_gender} creators.
- Point 3: Actionable pro-tip.

--- 4. OUTRO & CTA ---
Dialogue: "If you found this helpful, hit the Like button and subscribe for more!"
    """.strip()

    st.session_state.word_count = len(st.session_state.script_plain.split())
    # Reset asset previews on new script generation
    st.session_state.generated_image = None
    st.session_state.generated_video = None

# -----------------------------------------------------------------------------
# 8. OUTPUT PREVIEW, ASSETS & EXPORT COLUMN
# -----------------------------------------------------------------------------
with col_preview:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.subheader("📑 Script Preview & Report")
    
    if st.session_state.script_html:
        # Estimated reading time
        est_minutes = round(st.session_state.word_count / 130, 1)
        st.markdown(
            f'<span class="metric-badge">⏱️ Est. Speech Time: ~{est_minutes} mins ({st.session_state.word_count} words)</span>', 
            unsafe_allow_html=True
        )
        
        # HTML Script Display
        st.markdown(st.session_state.script_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- NEW FEATURE: TOPIC VISUAL ASSET GENERATOR ---
        st.markdown('<div class="styled-card">', unsafe_allow_html=True)
        st.subheader("🎨 Generate Visual Media Asset")
        st.write("Create a custom cover image or animated audio-video preview for your video topic.")
        
        asset_col1, asset_col2 = st.columns(2)
        
        with asset_col1:
            if st.button("🖼️ Generate Topic Image", use_container_width=True):
                topic_str = topic if topic else "YouTube Topic"
                st.session_state.generated_image = generate_topic_image(topic_str)
                st.success("Topic Image Created!")
                
        with asset_col2:
            if st.button("🎥 Render Topic MP4 Video", use_container_width=True):
                with st.spinner("Synthesizing voiceover & rendering MP4..."):
                    topic_str = topic if topic else "YouTube Topic"
                    st.session_state.generated_video = generate_topic_video(topic_str, st.session_state.script_plain)
                    st.success("MP4 Video Rendered!")
        
        # Display Generated Media Assets
        if st.session_state.generated_image and os.path.exists(st.session_state.generated_image):
            st.markdown("#### Generated Image Asset")
            st.image(st.session_state.generated_image, use_container_width=True)
            with open(st.session_state.generated_image, "rb") as file:
                st.download_button("📥 Download Image (.png)", data=file, file_name="topic_thumbnail.png", mime="image/png")

        if st.session_state.generated_video and os.path.exists(st.session_state.generated_video):
            st.markdown("#### Generated Video Asset")
            st.video(st.session_state.generated_video)
            with open(st.session_state.generated_video, "rb") as file:
                st.download_button("📥 Download Video (.mp4)", data=file, file_name="topic_preview.mp4", mime="video/mp4")
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Section
        st.markdown('<div class="styled-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Multi-Format Downloads")
        d1, d2, d3, d4 = st.columns(4)
        
        # 1. Markdown
        d1.download_button("📄 Markdown", data=st.session_state.script_plain.encode("utf-8"), file_name="script.md", mime="text/markdown", use_container_width=True)
        
        # 2. DOCX Word
        doc_html = f"<html><body>{st.session_state.script_html}</body></html>".encode("utf-8")
        d2.download_button("📝 DOCX", data=doc_html, file_name="script.doc", mime="application/msword", use_container_width=True)
        
        # 3. PPT Outline
        ppt_txt = f"SLIDE 1: Title\n{topic}\n\nSLIDE 2: Hook\nAudience: {target_age}\n\nSLIDE 3: Key Points\n{custom_features}".encode("utf-8")
        d3.download_button("📊 PPT", data=ppt_txt, file_name="ppt_outline.txt", mime="text/plain", use_container_width=True)
        
        # 4. HTML File
        d4.download_button("🌐 HTML", data=st.session_state.script_html.encode("utf-8"), file_name="script.html", mime="text/html", use_container_width=True)

        # Direct Sharing Links
        st.markdown("### ✉️ Direct Share Options")
        s1, s2 = st.columns(2)
        
        wa_text = urllib.parse.quote(f"Check out my YouTube Script:\n\n{st.session_state.script_plain[:250]}...")
        wa_url = f"https://api.whatsapp.com/send?text={wa_text}"
        s1.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">💬 Share via WhatsApp</button></a>', unsafe_allow_html=True)
        
        mail_sub = urllib.parse.quote(f"YouTube Script: {topic if topic else 'New Video'}")
        mail_body = urllib.parse.quote(st.session_state.script_plain)
        mail_url = f"mailto:?subject={mail_sub}&body={mail_body}"
        s2.markdown(f'<a href="{mail_url}"><button style="width:100%; background:#2563EB; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">✉️ Send via Email</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Adjust the parameters on the left and click **Generate Script** to create your script preview and enable asset generation.")
        st.markdown('</div>', unsafe_allow_html=True)
