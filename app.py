import streamlit as st
from google import genai
from google.genai import types

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

# --- Main Interface: Topic & Key Details ---
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
                
                # Construct Engineering Prompt
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
                
                # Call Gemini Model (using gemini-2.5-flash)
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                
                # Render Generated Output
                st.success("Script Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Download Button
                st.download_button(
                    label="📄 Download Script (.txt)",
                    data=response.text,
                    file_name=f"{topic.lower().replace(' ', '_')}_script.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
