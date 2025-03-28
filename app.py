import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompt for summarization
prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        raise e

# Function to generate summary using Gemini AI
def generate_gemini_content(transcript_text, prompt, model_name):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to list available models
def list_available_models():
    models = genai.list_models()
    return [model.name for model in models if "generateContent" in model.supported_generation_methods]

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

# Display available models in a dropdown
available_models = list_available_models()
selected_model = st.selectbox("Choose a Gemini Model", available_models, index=0)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt, selected_model)
        st.markdown("## Detailed Notes:")
        st.write(summary)
