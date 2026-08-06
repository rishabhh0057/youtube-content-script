import streamlit as st
import html
import os
import urllib.parse
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
# ✅ NEW (Compatible with MoviePy 2.0+)
import moviepy as mp

# Google API Imports for YouTube Upload
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME SWITCHING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Auto YouTube Creator Studio",
    page_icon="🎬",
    layout="wide"
)

st.sidebar.title("⚙️ Layout & Theme")
theme_choice = st.sidebar.selectbox("🎨 App Theme", ["Dark Glass", "Cyberpunk", "Light"])

left_col_ratio = st.sidebar.slider("Panel Split Ratio (%)", 20, 80, 45, 5)
right_col_ratio = 100 - left_col_ratio

# Apply Dynamic CSS Styling
def apply_css(theme):
    bg_color = "#0B0F19" if theme == "Dark Glass" else ("#090014" if theme == "Cyberpunk" else "#F8FAFC")
    card_bg = "rgba(22, 31, 48, 0.8)" if theme == "Dark Glass" else ("rgba(24, 0, 46, 0.9)" if theme == "Cyberpunk" else "#FFFFFF")
    text_color = "#F3F4F6" if theme != "Light" else "#0F172A"
    
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .styled-card {{
            background: {card_bg};
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)

apply_css(theme_choice)

st.title("🎬 AI Video Creator & YouTube Auto-Publisher")

col_inputs, col_preview = st.columns([left_col_ratio, right_col_ratio], gap="medium")

# Initialize Session States
for key in ["script_text", "script_html", "generated_video_path"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# -----------------------------------------------------------------------------
# 2. SCRIPT GENERATION INPUT FORM
# -----------------------------------------------------------------------------
with col_inputs:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.subheader("📌 Step 1: Script Parameters")
    
    topic = st.text_input("Video Topic", "10 Productivity Hacks for 2026")
    target_age = st.selectbox("Target Age", ["13-17", "18-24", "25-34", "35-50", "50+"], index=1)
    target_gender = st.selectbox("Target Gender", ["All Audiences", "Male-leaning", "Female-leaning"])
    custom_features = st.text_area("Custom Features", "Include energetic voiceover and mid-video CTA.")
    
    if st.button("🚀 Generate Script", type="primary", use_container_width=True):
        st.session_state.script_text = f"Welcome! Today we are discussing {topic}. Tailored specifically for our {target_age} audience. Click subscribe for more updates!"
        
        st.session_state.script_html = f"""
        <h3>📹 Video Title: {html.escape(topic)}</h3>
        <p><strong>Target Audience:</strong> {target_age} | {target_gender}</p>
        <hr>
        <p><strong>Script Narrative:</strong></p>
        <p>{st.session_state.script_text}</p>
        """
        st.success("Script generated successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AUTOMATED VIDEO CREATION ENGINE (TTS + MoviePy)
# -----------------------------------------------------------------------------
def create_video_from_script(text, output_filename="generated_video.mp4"):
    # Step A: Convert Script Text to Audio using gTTS
    tts = gTTS(text=text, lang='en', slow=False)
    audio_path = "voiceover.mp3"
    tts.save(audio_path)
    audio_clip = mp.AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Step B: Create Slide Visual Image using Pillow
    img = Image.new('RGB', (1920, 1080), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    
    # Simple text wrapped layout
    text_content = f"TOPIC: {topic}\n\n{text[:150]}..."
    d.text((100, 400), text_content, fill=(255, 255, 255))
    
    image_path = "slide_frame.png"
    img.save(image_path)

    # Step C: Combine Audio + Slide into MP4 Video using MoviePy
    image_clip = mp.ImageClip(image_path).set_duration(duration)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_filename, fps=24, codec="libx264")

    # Clean up temp files
    if os.path.exists(audio_path): os.remove(audio_path)
    if os.path.exists(image_path): os.remove(image_path)
    
    return output_filename

# -----------------------------------------------------------------------------
# 4. YOUTUBE UPLOAD ENGINE
# -----------------------------------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_to_youtube(video_path, title, description, privacy_status="private"):
    if not os.path.exists("client_secret.json"):
        st.error("Missing 'client_secret.json'. Please add Google OAuth credentials file.")
        return None

    # Authenticate OAuth Flow
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    # Prepare Video Payload
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'Productivity', 'YouTube Short'],
            'categoryId': '22'  # Category 22 = People & Blogs
        },
        'status': {
            'privacyStatus': privacy_status  # Options: 'private', 'public', 'unlisted'
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if response is not None:
            if 'id' in response:
                return response['id']
    return None

# -----------------------------------------------------------------------------
# 5. PREVIEW, VIDEO RENDERING, AND YOUTUBE PUBLISHING
# -----------------------------------------------------------------------------
with col_preview:
    st.markdown('<div class="styled-card">', unsafe_allow_html=True)
    st.subheader("🎬 Step 2: Render & Publish Video")
    
    if st.session_state.script_html:
        st.markdown(st.session_state.script_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🎥 Generate Video (MP4)")
        
        if st.button("🔨 Render MP4 Video", use_container_width=True):
            with st.spinner("Generating Voiceover & Rendering Video..."):
                video_file = create_video_from_script(st.session_state.script_text)
                st.session_state.generated_video_path = video_file
                st.success("Video Rendered Successfully!")
        
        # Play local video preview if generated
        if st.session_state.generated_video_path and os.path.exists(st.session_state.generated_video_path):
            st.video(st.session_state.generated_video_path)
            
            st.markdown("---")
            st.subheader("☁️ Step 3: Auto-Upload to YouTube")
            
            privacy = st.selectbox("Privacy Level", ["private", "unlisted", "public"])
            
            if st.button("🔴 Upload to YouTube Channel", type="primary", use_container_width=True):
                with st.spinner("Authenticating and Uploading to YouTube..."):
                    video_id = upload_to_youtube(
                        video_path=st.session_state.generated_video_path,
                        title=topic,
                        description=f"{st.session_state.script_text}\n\nGenerated with AI Studio.",
                        privacy_status=privacy
                    )
                    if video_id:
                        st.balloons()
                        st.success(f"Uploaded Successfully! Video ID: {video_id}")
                        st.markdown(f"[🔗 View Video on YouTube](https://youtu.be/{video_id})")

    else:
        st.info("Generate a script first in Step 1 to unlock Video Generation & YouTube Uploading.")
    st.markdown('</div>', unsafe_allow_html=True)

AttributeError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/youtube-content-script/app.py", line 172, in <module>
    video_file = create_video_from_script(st.session_state.script_text)
File "/mount/src/youtube-content-script/app.py", line 108, in create_video_from_script
    image_clip = mp.ImageClip(image_path).set_duration(duration)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
