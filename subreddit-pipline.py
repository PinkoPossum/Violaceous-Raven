import os
import re
import random
import pandas as pd
from datetime import datetime, timezone
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment
from gtts import gTTS
import praw

# === CONFIGURATION ===
REDDIT_CLIENT_ID = "place-holder"
REDDIT_CLIENT_SECRET = "place-holder"
REDDIT_USER_AGENT = "place-holder"

SUBREDDIT_NAME = "Desired Subreddit Goes Here"
POST_LIMIT = 5
EXCEL_FILE = "top_posts.xlsx" # Name of output file for post info.
RAW_VIDEO_DIR = "raw_video" # Name of video with your stock footage.
AUDIO_OUTPUT_DIR = "narrations" # Name of folder with your narrations.
VIDEO_OUTPUT_DIR = "videos" # Name of output folder.

# === INITIALIZATION ===
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# === UTILITIES ===
def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", str(text).strip())

def generate_ns_id(existing_ids, count):
    if existing_ids.empty:
        start = 1
    else:
        last_id = existing_ids.str.extract(r'NS(\d+)', expand=False).dropna().astype(int).max()
        start = last_id + 1
    return [f"NS{str(i).zfill(4)}" for i in range(start, start + count)]

# === MAIN TASKS ===
def fetch_top_posts():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = []

    for submission in subreddit.top(time_filter='day', limit=POST_LIMIT):
        posts.append({
            "ID": "",  # placeholder
            "Title": submission.title,
            "Author": submission.author.name if submission.author else "[deleted]",
            "Date": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "Content": submission.selftext,
            "URL": f"https://reddit.com{submission.permalink}"
        })
    return posts

def update_excel(posts):
    new_df = pd.DataFrame(posts)

    if os.path.exists(EXCEL_FILE):
        existing_df = pd.read_excel(EXCEL_FILE)
        new_ids = generate_ns_id(existing_df["ID"], len(new_df))
        new_df["ID"] = new_ids
        combined = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        new_ids = generate_ns_id(pd.Series(dtype=str), len(new_df))
        new_df["ID"] = new_ids
        combined = new_df

    combined.to_excel(EXCEL_FILE, index=False)
    print(f"Updated spreadsheet with {len(new_df)} posts.")
    return new_df

def split_text_into_chunks(text, max_chars=4500):
    parts = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for part in parts:
        if len(current_chunk) + len(part) <= max_chars:
            current_chunk += part + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = part + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_audio(id_tag, content):
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(AUDIO_OUTPUT_DIR, f"{id_tag}.mp3")
    print(f"🔊 Generating audio with Google TTS: {filepath}")

    chunks = split_text_into_chunks(content)
    temp_files = []

    for i, chunk in enumerate(chunks):
        print(f"🧩 Synthesizing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
        tts = gTTS(text=chunk, lang='en', slow=False)
        temp_path = os.path.join(AUDIO_OUTPUT_DIR, f"{id_tag}_part{i}.mp3")
        tts.save(temp_path)
        temp_files.append(temp_path)

    # Concatenate all audio parts
    combined = AudioSegment.empty()
    for temp in temp_files:
        combined += AudioSegment.from_file(temp)

    combined.export(filepath, format="mp3")

    # Clean up temporary chunks
    for temp in temp_files:
        os.remove(temp)

    print(f"✅ Combined audio saved: {filepath}")
    return filepath

def generate_video(id_tag, audio_path):
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
    video_files = [f for f in os.listdir(RAW_VIDEO_DIR) if f.lower().endswith(('.mp4', '.mov'))]
    if not video_files:
        print("❌ No raw video files found.")
        return

    chosen_video = os.path.join(RAW_VIDEO_DIR, random.choice(video_files))
    output_path = os.path.join(VIDEO_OUTPUT_DIR, f"{id_tag}.mp4")

    video = VideoFileClip(chosen_video)
    audio = AudioFileClip(audio_path)
    final = video.set_audio(audio).subclip(0, min(video.duration, audio.duration))
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')

    print(f"✅ Video saved: {output_path}")

def main():
    print("📥 Fetching top posts...")
    raw_posts = fetch_top_posts()
    processed_df = update_excel(raw_posts)

    print("🎤 Generating audio and 🎬 creating video:")
    for _, row in processed_df.tail(POST_LIMIT).iterrows():
        id_tag = row["ID"]
        content = row["Content"]

        if pd.isna(content) or not content.strip():
            continue

        audio_path = generate_audio(id_tag, content)
        generate_video(id_tag, audio_path)

    print("🎉 All tasks completed!")

if __name__ == "__main__":
    main()
