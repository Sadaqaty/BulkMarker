import os
from PySide6.QtCore import QThread, Signal
from moviepy.editor import VideoFileClip, ImageClip, TextClip

class Worker(QThread):
    progress = Signal(int)
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
            for i, file in enumerate(files):
                video_path = os.path.join(self.input_dir, file)
                self.process_video(video_path)
                self.progress.emit(int((i+1)/total * 100))
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def process_video(self, video_path):
        clip = VideoFileClip(video_path)
        for overlay in self.overlays:
            if overlay['type'] == 'image':
                wm = ImageClip(overlay['file']).resize(width=clip.w * overlay['scale'])
                wm = wm.set_duration(clip.duration).set_position(overlay['position']).set_opacity(overlay['opacity'])
                if 'rotation' in overlay:
                    wm = wm.rotate(overlay['rotation'])
                clip = clip.overlay(wm)
            elif overlay['type'] == 'video':
                wm = VideoFileClip(overlay['file']).resize(width=clip.w * overlay['scale'])
                wm = wm.set_duration(clip.duration).set_position(overlay['position']).set_opacity(overlay['opacity'])
                if overlay.get('loop', False):
                    wm = wm.loop(duration=clip.duration)
                clip = clip.overlay(wm)
            elif overlay['type'] == 'text':
                txt_clip = TextClip(overlay['text'], fontsize=overlay['size'], color=overlay['color'], font=overlay['font'])
                txt_clip = txt_clip.set_position(overlay['position']).set_duration(clip.duration).set_opacity(overlay['opacity'])
                clip = clip.overlay(txt_clip)
        out_path = os.path.join(self.output_dir, os.path.basename(video_path))
        clip.write_videofile(out_path, codec="libx264", audio_codec="aac")