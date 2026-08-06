import streamlit as st
import html
import urllib.parse
from io import BytesIO

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STATE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="YouTube Content Script Generator",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Dynamic Theme Switcher
def apply_custom_theme(theme_choice):
    if theme_choice == "Dark Mode":
        st.markdown("""
            <style>
            .stApp { background-color: #0f172a; color: #f8fafc; }
            .script-card { background-color: #1e293b; color: #f8fafc; border: 1px solid #334155; padding: 20px; border-radius: 10px; }
            </style>
        """, unsafe_allow_html=True)
    elif theme_choice == "Cyberpunk":
        st.markdown("""
            <style>
            .stApp { background-color: #090014; color: #00f0ff; }
            .script-card { background-color: #18002e; color: #00f0ff; border: 1px solid #ff007f; padding: 20px; border-radius: 10px; }
            h1, h2, h3, label { color: #ffe600 !important; }
            </style>
        """, unsafe_allow_html=True)
    else:  # Light Mode (Default Streamlit palette touch-up)
        st.markdown("""
            <style>
            .stApp { background-color: #f8fafc; color: #0f172a; }
            .script-card { background-color: #ffffff; color: #0f172a; border: 1px solid #e2e8f0; padding: 20px; border-radius: 10px; }
            </style>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
st.sidebar.title("⚙️ App Settings")
theme_choice = st.sidebar.selectbox("🎨 Select Theme", ["Light Mode", "Dark Mode", "Cyberpunk"])
apply_custom_theme(theme_choice)

st.title("🎬 YouTube Content Script Generator")
st.write("Generate, customize, format, export, and share targeted video scripts.")

# -----------------------------------------------------------------------------
# 3. INPUT FORM SECTION
# -----------------------------------------------------------------------------
col_inputs, col_preview = st.columns([1, 1], gap="medium")

with col_inputs:
    st.subheader("📌 Script Parameters")
    
    topic = st.text_input("Video Topic / Title", placeholder="e.g. 10 AI Productivity Tools for 2026")
    
    target_age = st.selectbox(
        "Target Age Group",
        ["Teens (13-17)", "Young Adults (18-24)", "Adults (25-34)", "Middle-Aged (35-50)", "Seniors (50+)"],
        index=1
    )
    
    target_gender = st.selectbox(
        "Target Gender",
        ["All Audiences", "Male-leaning", "Female-leaning", "Inclusive / Non-Binary"]
    )
    
    custom_features = st.text_area(
        "Custom Script Features & Instructions",
        placeholder="e.g., Include comedic B-roll cues, add mid-video CTA at 2 mins, use fast-paced storytelling..."
    )
    
    generate_btn = st.button("🚀 Generate YouTube Script", type="primary", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. SCRIPT GENERATION LOGIC
# -----------------------------------------------------------------------------
if "script_html" not in st.session_state:
    st.session_state.script_html = ""
if "script_plain" not in st.session_state:
    st.session_state.script_plain = ""

if generate_btn:
    topic_val = topic if topic else "Untitled YouTube Video"
    custom_val = custom_features if custom_features else "Standard high-retention video style."
    
    # Clean HTML Output Structure
    st.session_state.script_html = f"""
    <h2>📹 Title: {html.escape(topic_val)}</h2>
    <p><strong>🎯 Audience Demographic:</strong> {target_age} | {target_gender}</p>
    <p><strong>⚡ Custom Instructions:</strong> {html.escape(custom_val)}</p>
    <hr>
    
    <h3>🔥 1. The Hook (0:00 - 0:15)</h3>
    <p><strong>Visual Cue:</strong> Dynamic jump cuts, fast push-in camera zoom.</p>
    <p><strong>Dialogue / Audio:</strong> "If you think {html.escape(topic_val)} is hard, you're doing it wrong. In this video, I'm showing you the exact shortcut!"</p>
    
    <h3>📍 2. Intro & Value Proposition (0:15 - 0:45)</h3>
    <p><strong>Visual Cue:</strong> Title card overlay with key take-away bullet points.</p>
    <p><strong>Dialogue / Audio:</strong> "Welcome back! Tailored specifically for our {target_age} viewers, today we are uncovering secrets most creators skip."</p>
    
    <h3>💡 3. Core Content & Main Body (0:45 - 4:00)</h3>
    <p><strong>Custom Applied Rule:</strong> <em>{html.escape(custom_val)}</em></p>
    <ul>
        <li><strong>Point 1:</strong> Foundational breakdown of {html.escape(topic_val)}.</li>
        <li><strong>Point 2:</strong> Top mistakes to avoid for {target_gender} audiences.</li>
        <li><strong>Point 3:</strong> Actionable pro-tip you can implement right now.</li>
    </ul>
    
    <h3>📢 4. Call To Action & Outro (4:00 - End)</h3>
    <p><strong>Visual Cue:</strong> End-screen animation pointing to recommended videos.</p>
    <p><strong>Dialogue / Audio:</strong> "If you found this helpful, hit the Like button and subscribe for more content tailored to you!"</p>
    """.strip()

    # Plaintext conversion for exports and text-only previews
    st.session_state.script_plain = f"""
Title: {topic_val}
Audience: {target_age} | {target_gender}
Custom Instructions: {custom_val}

--- 1. THE HOOK (0:00 - 0:15) ---
Visual: Dynamic jump cuts, camera zoom.
Dialogue: "If you think {topic_val} is hard, you're doing it wrong. In this video, I'm showing you the exact shortcut!"

--- 2. INTRO & VALUE PROPOSITION (0:15 - 0:45) ---
Visual: Title card overlay.
Dialogue: "Welcome back! Tailored specifically for our {target_age} viewers, today we are uncovering secrets most creators skip."

--- 3. CORE CONTENT (0:45 - 4:00) ---
Custom Feature: {custom_val}
- Point 1: Foundational breakdown of {topic_val}.
- Point 2: Top mistakes to avoid for {target_gender} audiences.
- Point 3: Actionable pro-tip.

--- 4. OUTRO & CTA ---
Dialogue: "If you found this helpful, hit the Like button and subscribe for more!"
    """.strip()

# -----------------------------------------------------------------------------
# 5. DISPLAY PREVIEW & EXPORT OPTIONS
# -----------------------------------------------------------------------------
with col_preview:
    st.subheader("📑 Script Preview & Sharing")
    
    if st.session_state.script_html:
        # Render Formatted HTML Preview inside styled div
        st.markdown(f'<div class="script-card">{st.session_state.script_html}</div>', unsafe_allow_html=True)
        st.write("")
        
        st.markdown("### 📥 Download Script Formats")
        dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
        
        # 1. Markdown Download
        md_bytes = st.session_state.script_plain.encode("utf-8")
        dl_col1.download_button("📄 Markdown", data=md_bytes, file_name="youtube_script.md", mime="text/markdown")
        
        # 2. DOCX Word Compatible File
        doc_content = f"<html><body>{st.session_state.script_html}</body></html>".encode("utf-8")
        dl_col2.download_button("📝 DOCX", data=doc_content, file_name="youtube_script.doc", mime="application/msword")
        
        # 3. PPT Outline Text Download
        ppt_outline = f"SLIDE 1: Title\n{topic}\n\nSLIDE 2: Hook & Audience\nTarget: {target_age}\n\nSLIDE 3: Content Outline\n{custom_features}".encode("utf-8")
        dl_col3.download_button("📊 PPT Outline", data=ppt_outline, file_name="ppt_script_outline.txt", mime="text/plain")
        
        # 4. HTML Download
        html_bytes = st.session_state.script_html.encode("utf-8")
        dl_col4.download_button("🌐 HTML File", data=html_bytes, file_name="youtube_script.html", mime="text/html")

        st.markdown("### 💬 Send & Share Report")
        share_col1, share_col2 = st.columns(2)
        
        # WhatsApp Share Link
        wa_text = urllib.parse.quote(f"Check out my YouTube Script:\n\n{st.session_state.script_plain[:300]}...")
        wa_url = f"https://api.whatsapp.com/send?text={wa_text}"
        share_col1.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:6px; font-weight:bold; cursor:pointer;">💬 Share on WhatsApp</button></a>', unsafe_allow_html=True)
        
        # Email Share Link
        mail_sub = urllib.parse.quote(f"YouTube Content Script: {topic if topic else 'New Video'}")
        mail_body = urllib.parse.quote(st.session_state.script_plain)
        mail_url = f"mailto:?subject={mail_sub}&body={mail_body}"
        share_col2.markdown(f'<a href="{mail_url}"><button style="width:100%; background-color:#0072C6; color:white; border:none; padding:10px; border-radius:6px; font-weight:bold; cursor:pointer;">✉️ Send via Email</button></a>', unsafe_allow_html=True)

    else:
        st.info("Fill out the parameters on the left and click **Generate YouTube Script** to view options.")
