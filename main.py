import os
from moviepy.editor import VideoFileClip, ImageClip

INPUT_DIR = "input_videos"
OUTPUT_DIR = "output_videos"
WATERMARK_PATH = "watermark.png"

POSITION = ("right","bottom")
OPACITY = 0.6
SCALE = 0.15

os.makedirs(OUTPUT_DIR, exist_ok=True)

def watermark_video(video_path):
    clip = VideoFileClip(video_path)

    if WATERMARK_PATH.endswith(".mp4"):
        wm = VideoFileClip(WATERMARK_PATH).resize(width=clip.w * SCALE)
        wm = wm.set_duration(clip.duration)
    else:
        wm = ImageClip(WATERMARK_PATH).resize(width=clip.w * SCALE)
        wm = wm.set_duration(clip.duration)

    wm = wm.set_position(POSITION).set_opacity(OPACITY)

    final = clip.overlay(wm)
    out_path = os.path.join(OUTPUT_DIR, os.path.basename(video_path))
    final.write_videofile(out_path, codec="libx264", audio_codec="aac")

for file in os.listdir(INPUT_DIR):
    if file.lower().endswith((".mp4", ".mov", ".avi")):
        watermark_video(os.path.join(INPUT_DIR, file))
