import os
import math
from PySide6.QtCore import QThread, Signal
import os
from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips

class Worker(QThread):
    progress = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, input_dir, output_dir, overlays):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.overlays = overlays  # list of overlay dicts

    def run(self):
        try:
            files = [f for f in os.listdir(self.input_dir) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            total = len(files)
            self.progress.emit(f"Found {total} video files to process")
            for i, file in enumerate(files):
                video_path = os.path.join(self.input_dir, file)
                self.progress.emit(f"Processing video {i+1}/{total}: {file}")
                self.process_video(video_path)
                self.progress.emit(f"Completed video {i+1}/{total}: {file}")
            self.progress.emit("All videos processed successfully")
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def process_video(self, video_path):
        try:
            clip = VideoFileClip(video_path)
            for overlay in self.overlays:
                if overlay['type'] == 'image':
                    if not os.path.exists(overlay['file']):
                        raise FileNotFoundError(f"Image file not found: {overlay['file']}")
                    try:
                        wm = ImageClip(overlay['file'])
                        wm = wm.resized(width=int(clip.w * overlay['scale']))
                    except Exception as e:
                        raise Exception(f"Failed to load image {overlay['file']}: {str(e)}")
                    wm = wm.with_duration(clip.duration).with_position(overlay['position']).with_opacity(overlay['opacity'])
                    if 'rotation' in overlay:
                        wm = wm.rotated(overlay['rotation'])
                    clip = CompositeVideoClip([clip, wm])
                elif overlay['type'] == 'video':
                    if not os.path.exists(overlay['file']):
                        raise FileNotFoundError(f"Video file not found: {overlay['file']}")
                    try:
                        wm = VideoFileClip(overlay['file'])
                        wm = wm.resized(width=int(clip.w * overlay['scale']))
                    except Exception as e:
                        raise Exception(f"Failed to load video {overlay['file']}: {str(e)}")
                    if overlay.get('loop', False):
                        loops = math.ceil(clip.duration / wm.duration)
                        wm = concatenate_videoclips([wm] * loops)
                        wm = wm.subclipped(0, clip.duration)
                    else:
                        wm = wm.with_duration(clip.duration)
                    wm = wm.with_position(overlay['position']).with_opacity(overlay['opacity'])
                    clip = CompositeVideoClip([clip, wm])
                elif overlay['type'] == 'text':
                    try:
                        txt_clip = TextClip(overlay['text'], fontsize=overlay['size'], color=overlay['color'], font=overlay['font'])
                    except Exception as e:
                        raise Exception(f"Failed to create text clip: {str(e)}")
                    txt_clip = txt_clip.with_position(overlay['position']).with_duration(clip.duration).with_opacity(overlay['opacity'])
                    clip = CompositeVideoClip([clip, txt_clip])
            out_path = os.path.join(self.output_dir, os.path.basename(video_path))
            clip.write_videofile(out_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            raise Exception(f"Error processing {video_path}: {str(e)}")