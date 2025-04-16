import streamlit as st
import os
import requests

# Set Streamlit page config
st.set_page_config(page_title="Smart Email Rewriter", page_icon="📧", layout="centered")

# Title
st.title("📧 Smart Email Rewriter")
st.write("Rewrite your emails in different tones or styles using AI.")

# Input fields
email_input = st.text_area("✍️ Enter your draft email here:", height=200)

tone_options = ["Formal", "Friendly", "Persuasive", "Apologetic", "Professional", "Assertive", "Encouraging"]
tone = st.selectbox("🎨 Choose a tone/style for rewriting:", tone_options)

# Rewrite button
if st.button("🔁 Rewrite"):
    if not email_input.strip():
        st.warning("Please enter your draft email.")
    else:
        with st.spinner("Rewriting your email..."):
            # API Call to Groq
            groq_api_key = st.secrets["GROQ_API_KEY"]
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a helpful email assistant. Rewrite emails in the '{tone}' tone. Keep the content meaningful and grammatically correct."
                    },
                    {
                        "role": "user",
                        "content": email_input
                    }
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                rewritten = response.json()["choices"][0]["message"]["content"]
                st.subheader("✅ Rewritten Email:")
                st.success(rewritten)
            else:
                st.error("Failed to rewrite email. Please check your API key or try again later.")
