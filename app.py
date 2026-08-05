import streamlit as st
import time
from google import genai

# --- Page Configuration ---
st.set_page_config(
    page_title="AI YouTube Script Generator",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI-Powered YouTube Content Script Generator")
st.caption("Generate structured, high-retention YouTube scripts complete with audio, visual cues, and CTAs.")

# --- Sidebar: Configuration & API Key ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Input
    api_key = st.text_input("Enter Gemini API Key:", type="password", help="Get your free key from Google AI Studio")
    
    st.markdown("---")
    st.subheader("🎯 Video Parameters")
    
    target_audience = st.selectbox(
        "Target Audience:",
        ["Beginners", "Tech Enthusiasts", "Students", "Entrepreneurs", "General Public"]
    )
    
    video_duration = st.select_slider(
        "Estimated Video Length:",
        options=["60s (Shorts)", "3-5 Mins", "8-10 Mins", "15+ Mins"]
    )
    
    tone = st.selectbox(
        "Script Tone:",
        ["Engaging & Energetic", "Educational & Professional", "Casual & Conversational", "Dramatic & Storytelling"]
    )

# --- Main Interface ---
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input("Video Topic / Main Keyword:", placeholder="e.g., How to Learn Python in 2026")
    key_points = st.text_area("Key Points or Main Takeaways (Optional):", placeholder="e.g., Cover basics, free resources, projects to build...")

with col2:
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    - Be specific with your topic.
    - Select a tone that matches your brand.
    - Provide custom key points if you want specific sections included.
    """)

# --- Robust Model Generation Function with Retry Logic ---
def generate_script_with_retry(client, prompt, max_retries=3):
    """Attempts to call the API and retries if 503 UNAVAILABLE occurs."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            # If server is overloaded (503), wait and retry
            if "503" in error_str or "UNAVAILABLE" in error_str or "high demand" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3  # Waits 3s, then 6s, etc.
                    st.warning(f"Server is busy. Retrying in {wait_time} seconds (Attempt {attempt + 2}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    raise Exception("The AI service is currently experiencing extremely high traffic. Please wait 1-2 minutes and click Generate again.")
            else:
                # Re-raise non-503 errors (e.g., invalid API key)
                raise e

# --- Generation Logic ---
if st.button("🚀 Generate YouTube Script", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a Video Topic.")
    else:
        with st.spinner("Brainstorming retention hook, visual cues, and dialogue..."):
            try:
                # Initialize Google GenAI Client
                client = genai.Client(api_key=api_key)
                
                # Construct Prompt
                prompt = f"""
                You are an expert YouTube content creator and scriptwriter known for high-retention video scripts.
                
                Generate a comprehensive YouTube Video Script based on the following details:
                - **Topic:** {topic}
                - **Target Audience:** {target_audience}
                - **Video Length:** {video_duration}
                - **Tone:** {tone}
                - **Key Points to Include:** {key_points if key_points else "Infer logical key points based on the topic."}
                
                **Structure the Output as follows:**
                1. **Video Title Ideas:** (Provide 3 catchy, high-CTR titles)
                2. **Pattern Interrupt / Hook (0-15s):** (Grabs attention immediately)
                3. **Intro & Channel Branding:** (Brief introduction and video premise)
                4. **Main Body Segments:** Break this down into structured chapters. For each chapter, include:
                   - **[Visual Cue]:** B-roll, text overlays, screen recordings, or camera cuts.
                   - **[Audio/Spoken Script]:** Word-for-word spoken dialogue.
                5. **Outro & Call-to-Action (CTA):** Encouraging likes, comments, and channel subscriptions.
                """
                
                # Call model using retry function
                script_output = generate_script_with_retry(client, prompt)
                
                # Render Generated Output
                st.success("Script Generated Successfully!")
                st.markdown("---")
                st.markdown(script_output)
                
                # Download Button
                st.download_button(
                    label="📄 Download Script (.txt)",
                    data=script_output,
                    file_name=f"{topic.lower().replace(' ', '_')}_script.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
