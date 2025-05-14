import os
import subprocess
import uuid
import shutil
from tortoise.api import TextToSpeech
import streamlit as st

UPLOAD_DIR = "inputs"
OUTPUT_DIR = "outputs"
SADTALKER_DIR = "SadTalker"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.title("🎭 Realistic Talking Avatar App")
uploaded_image = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
text = st.text_area("Enter your script (Türkçe/English supported)")

if st.button("Generate Talking Video") and uploaded_image and text:
    unique_id = str(uuid.uuid4())
    image_path = f"{UPLOAD_DIR}/{unique_id}.jpg"
    audio_path = f"{UPLOAD_DIR}/{unique_id}.wav"
    video_dir = f"{OUTPUT_DIR}/{unique_id}"

    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    st.info("⏳ Generating speech...")
    tts = TextToSpeech()
    tts.tts_to_file(text=text, voice='tom', file_path=audio_path)

    st.info("⏳ Creating talking video...")
    os.makedirs(video_dir, exist_ok=True)

    subprocess.run([
        "python", f"{SADTALKER_DIR}/inference.py",
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--result_dir", video_dir,
        "--enhancer", "gfpgan"
    ])

    final_video = f"{video_dir}/result.mp4"
    if os.path.exists(final_video):
        st.video(final_video)
        st.success("✅ Done!")
    else:
        st.error("❌ Video generation failed.")
