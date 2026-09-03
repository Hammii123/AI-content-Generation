import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored social media posts, captions, and hashtags instantly.")

# Retrieve Groq API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)

# User Inputs
content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "Product Promotion", "Educational Post", "Announcement", "Blog Idea"]
)

platform = st.selectbox(
    "Platform",
    ["Instagram", "LinkedIn", "Facebook", "X (Twitter)", "TikTok"]
)

topic = st.text_area(
    "Topic",
    placeholder="e.g., Benefits of learning Python for beginners"
)

target_audience = st.text_input(
    "Target Audience",
    placeholder="e.g., Students and beginner developers"
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Casual", "Funny", "Inspirational", "Educational"]
)

# Execution
if st.button("Generate Content", type="primary"):
    if not GROQ_API_KEY:
        st.error("🔑 Groq API Key is missing. Add `GROQ_API_KEY` to your Streamlit secrets.")
    elif not topic.strip() or not target_audience.strip():
        st.warning("⚠️ Please fill in both the Topic and Target Audience fields.")
    else:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an expert social media copywriter. Generate content based on these exact specifications:

- Content Type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target Audience: {target_audience}
- Tone: {tone}

Strictly follow this structure in your response:

**POST:**
[Write a complete, engaging post tailored for {platform}]

**CAPTION:**
[Write a concise, punchy caption]

**HASHTAGS:**
[Provide 8 to 12 relevant hashtags separated by spaces]
"""

        try:
            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional AI social media content strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

            generated_content = response.choices[0].message.content

            st.success("✅ Content Generated!")
            st.markdown("---")
            st.markdown(generated_content)
            st.markdown("---")

            st.download_button(
                label="📥 Download Content (.txt)",
                data=generated_content,
                file_name=f"{platform.lower()}_content.txt",
                mime="text/plain"
            )

        except Exception as err:
            st.error(f"Error executing request: {err}")

st.divider()
st.caption("Powered by Streamlit & Groq API")
