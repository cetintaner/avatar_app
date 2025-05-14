import os
import subprocess
import uuid
import shutil
from tortoise.api import TextToSpeech
import streamlit as st

# Dizinleri oluştur
UPLOAD_DIR = "inputs"
OUTPUT_DIR = "outputs"
SADTALKER_DIR = "SadTalker"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Başlık
st.title("🎭 Realistic Talking Avatar App")

# Fotoğraf yükleme alanı
uploaded_image = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

# Metin girme alanı
text = st.text_area("Enter your script (Türkçe/English supported)")

# Buton tıklaması ile işlem başlatma
if st.button("Generate Talking Video") and uploaded_image and text:
    unique_id = str(uuid.uuid4())
    image_path = f"{UPLOAD_DIR}/{unique_id}.jpg"
    audio_path = f"{UPLOAD_DIR}/{unique_id}.wav"
    video_dir = f"{OUTPUT_DIR}/{unique_id}"

    # Fotoğrafı kaydet
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    st.info("⏳ Generating speech...")

    # TextToSpeech nesnesi oluştur
    tts = TextToSpeech()

    try:
        # Ses dosyasını oluştur
        audio_data = tts.synthesize(text=text, voice='tom')

        # Ses dosyasını kaydet
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_data)

        st.info("⏳ Creating talking video...")
        os.makedirs(video_dir, exist_ok=True)

        # Video oluşturma
        subprocess.run([
            "python", f"{SADTALKER_DIR}/inference.py",
            "--driven_audio", audio_path,
            "--source_image", image_path,
            "--result_dir", video_dir,
            "--enhancer", "gfpgan"
        ])

        # Video dosyasını kontrol et ve göster
        final_video = f"{video_dir}/result.mp4"
        if os.path.exists(final_video):
            st.video(final_video)
            st.success("✅ Done!")
        else:
            st.error("❌ Video generation failed.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
