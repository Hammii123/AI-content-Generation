import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Content Assistant", page_icon="✍️")

st.title("✍️ AI Content Assistant")
st.write("Create social media content using Groq AI.")

# Load API key from Streamlit secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = None

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
    placeholder="Example: Benefits of learning Python for beginners"
)

target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: Students and beginner developers"
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Casual", "Funny", "Inspirational", "Educational"]
)

if st.button("Generate Content", type="primary"):
    if not GROQ_API_KEY:
        st.error("Groq API key not found. Add GROQ_API_KEY to Streamlit secrets.")
    elif not topic.strip() or not target_audience.strip():
        st.warning("Please enter both the topic and target audience.")
    else:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are an expert social media content writer.

Create content using these details:

Content Type: {content_type}
Platform: {platform}
Topic: {topic}
Target Audience: {target_audience}
Tone: {tone}

Return the response in exactly this format:

POST:
Write a complete, engaging post suitable for the selected platform.

CAPTION:
Write a short, attractive caption.

HASHTAGS:
Provide 8 to 12 relevant hashtags.

Keep the content practical, natural, engaging, and appropriate for the target audience.
"""

        try:
            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI content creation assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

            generated_content = response.choices[0].message.content

            st.success("Content generated successfully!")
            st.subheader("Generated Content")
            st.markdown(generated_content)

            st.download_button(
                label="Download Content",
                data=generated_content,
                file_name="ai_generated_content.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error(f"Something went wrong: {error}")

st.divider()
st.caption("Built with Streamlit and Groq AI")
