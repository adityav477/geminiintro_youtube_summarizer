import streamlit as st
from dotenv import load_dotenv

load_dotenv()  ##to load the environemnt variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are given the transcript for a youtube video now you need to give the summary of that video in points in around 500 words : """


## tgetting youtube transcript
def extract_transcript(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


## generate summary
def generate_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Youtube sumarrizer")
youtube_link = st.text_input("Enter Youtube Video Link: ")
print(youtube_link)
if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript(youtube_link)
    if transcript_text:
        summary = generate_summary(transcript_text, prompt)
        st.markdown("## Detailed Summary")
        st.write(summary)
