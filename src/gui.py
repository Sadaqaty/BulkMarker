import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QLineEdit, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
    QComboBox, QListWidget, QTextEdit, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QIcon
from moviepy import VideoFileClip, ImageClip

class Worker(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, input_dir, output_dir, watermark_path, position, opacity, scale):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.watermark_path = watermark_path
        self.position = position
        self.opacity = opacity
        self.scale = scale

    def run(self):
        try:
            files = [f for f in os.listdir(self.input_dir) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
            total = len(files)
            for i, file in enumerate(files):
                video_path = os.path.join(self.input_dir, file)
                self.watermark_video(video_path)
                self.progress.emit(int((i+1)/total * 100))
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def watermark_video(self, video_path):
        clip = VideoFileClip(video_path)

        if self.watermark_path.endswith('.mp4'):
            wm = VideoFileClip(self.watermark_path).resize(width=clip.w * self.scale)
            wm = wm.set_duration(clip.duration)
        else:
            wm = ImageClip(self.watermark_path).resize(width=clip.w * self.scale)
            wm = wm.set_duration(clip.duration)

        wm = wm.set_position(self.position).set_opacity(self.opacity)

        final = clip.overlay(wm)
        out_path = os.path.join(self.output_dir, os.path.basename(video_path))
        final.write_videofile(out_path, codec="libx264", audio_codec="aac")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulk Video Watermarker")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_dashboard_tab()
        self.create_bulk_processing_tab()
        self.create_overlay_editor_tab()
        self.create_presets_tab()
        self.create_export_queue_tab()
        self.create_settings_tab()

    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard - Overview and Quick Actions"))
        # Add widgets for dashboard
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Dashboard")

    def create_bulk_processing_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Input folder
        input_group = QGroupBox("Input")
        input_layout = QFormLayout()
        self.input_edit = QLineEdit()
        input_button = QPushButton("Browse")
        input_button.clicked.connect(self.select_input_dir)
        input_layout.addRow(self.input_edit, input_button)
        input_group.setLayout(input_layout)

        # Output folder
        output_group = QGroupBox("Output")
        output_layout = QFormLayout()
        self.output_edit = QLineEdit()
        output_button = QPushButton("Browse")
        output_button.clicked.connect(self.select_output_dir)
        output_layout.addRow(self.output_edit, output_button)
        output_group.setLayout(output_layout)

        # Watermark
        watermark_group = QGroupBox("Watermark")
        watermark_layout = QFormLayout()
        self.watermark_edit = QLineEdit()
        watermark_button = QPushButton("Browse")
        watermark_button.clicked.connect(self.select_watermark)
        watermark_layout.addRow(self.watermark_edit, watermark_button)
        watermark_group.setLayout(watermark_layout)

        # Settings
        settings_group = QGroupBox("Settings")
        settings_layout = QFormLayout()
        self.position_combo = QComboBox()
        self.position_combo.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
        self.opacity_spin = QDoubleSpinBox()
        self.opacity_spin.setRange(0.0, 1.0)
        self.opacity_spin.setValue(0.6)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.01, 1.0)
        self.scale_spin.setValue(0.15)
        settings_layout.addRow("Position:", self.position_combo)
        settings_layout.addRow("Opacity:", self.opacity_spin)
        settings_layout.addRow("Scale:", self.scale_spin)
        settings_group.setLayout(settings_layout)

        # Process button
        self.process_button = QPushButton("Start Processing")
        self.process_button.clicked.connect(self.start_processing)

        # Progress
        self.progress_bar = QProgressBar()

        layout.addWidget(input_group)
        layout.addWidget(output_group)
        layout.addWidget(watermark_group)
        layout.addWidget(settings_group)
        layout.addWidget(self.process_button)
        layout.addWidget(self.progress_bar)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Bulk Processing")

    def create_overlay_editor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Image Overlay
        image_group = QGroupBox("Image Overlay")
        image_layout = QFormLayout()
        self.image_file_edit = QLineEdit()
        image_browse = QPushButton("Browse")
        image_browse.clicked.connect(lambda: self.select_file(self.image_file_edit, "Images (*.png *.jpg *.svg)"))
        self.image_scale = QDoubleSpinBox()
        self.image_scale.setRange(0.01, 1.0)
        self.image_scale.setValue(0.15)
        self.image_position = QComboBox()
        self.image_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
        self.image_opacity = QDoubleSpinBox()
        self.image_opacity.setRange(0.0, 1.0)
        self.image_opacity.setValue(0.6)
        self.image_rotation = QSpinBox()
        self.image_rotation.setRange(0, 360)
        image_layout.addRow("File:", self.image_file_edit)
        image_layout.addRow("", image_browse)
        image_layout.addRow("Scale:", self.image_scale)
        image_layout.addRow("Position:", self.image_position)
        image_layout.addRow("Opacity:", self.image_opacity)
        image_layout.addRow("Rotation:", self.image_rotation)
        image_group.setLayout(image_layout)

        # Video Overlay
        video_group = QGroupBox("Video Overlay")
        video_layout = QFormLayout()
        self.video_file_edit = QLineEdit()
        video_browse = QPushButton("Browse")
        video_browse.clicked.connect(lambda: self.select_file(self.video_file_edit, "Videos (*.mp4 *.mov *.avi)"))
        self.video_scale = QDoubleSpinBox()
        self.video_scale.setRange(0.01, 1.0)
        self.video_scale.setValue(0.15)
        self.video_position = QComboBox()
        self.video_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
        self.video_opacity = QDoubleSpinBox()
        self.video_opacity.setRange(0.0, 1.0)
        self.video_opacity.setValue(0.6)
        self.video_loop = QCheckBox("Loop")
        video_layout.addRow("File:", self.video_file_edit)
        video_layout.addRow("", video_browse)
        video_layout.addRow("Scale:", self.video_scale)
        video_layout.addRow("Position:", self.video_position)
        video_layout.addRow("Opacity:", self.video_opacity)
        video_layout.addRow("Loop:", self.video_loop)
        video_group.setLayout(video_layout)

        # Text Overlay
        text_group = QGroupBox("Text Overlay")
        text_layout = QFormLayout()
        self.text_edit = QTextEdit()
        self.text_font = QLineEdit("Arial")
        self.text_size = QSpinBox()
        self.text_size.setRange(10, 100)
        self.text_size.setValue(24)
        self.text_color = QLineEdit("#FFFFFF")
        self.text_position = QComboBox()
        self.text_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
        self.text_opacity = QDoubleSpinBox()
        self.text_opacity.setRange(0.0, 1.0)
        self.text_opacity.setValue(1.0)
        text_layout.addRow("Text:", self.text_edit)
        text_layout.addRow("Font:", self.text_font)
        text_layout.addRow("Size:", self.text_size)
        text_layout.addRow("Color:", self.text_color)
        text_layout.addRow("Position:", self.text_position)
        text_layout.addRow("Opacity:", self.text_opacity)
        text_group.setLayout(text_layout)

        layout.addWidget(image_group)
        layout.addWidget(video_group)
        layout.addWidget(text_group)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Overlay Editor")

    def create_presets_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.presets_list = QListWidget()
        self.load_presets()

        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Save Preset")
        save_button.clicked.connect(self.save_preset)
        load_button = QPushButton("Load Preset")
        load_button.clicked.connect(self.load_preset)
        delete_button = QPushButton("Delete Preset")
        delete_button.clicked.connect(self.delete_preset)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        buttons_layout.addWidget(delete_button)

        layout.addWidget(QLabel("Presets:"))
        layout.addWidget(self.presets_list)
        layout.addLayout(buttons_layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Presets")

    def create_export_queue_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Export & Queue - Manage queue"))
        # Add queue management
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Export & Queue")

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings - App settings"))
        # Add settings
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Settings")

    def select_input_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if dir_path:
            self.input_edit.setText(dir_path)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_edit.setText(dir_path)

    def select_watermark(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Watermark File", "", "Images (*.png *.jpg *.svg);;Videos (*.mp4 *.mov)")
        if file_path:
            self.watermark_edit.setText(file_path)

    def start_processing(self):
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()
        watermark_path = self.watermark_edit.text()
        position = self.position_combo.currentText().replace('-', ' ')
        opacity = self.opacity_spin.value()
        scale = self.scale_spin.value()

        if not all([input_dir, output_dir, watermark_path]):
            return  # Show error

        os.makedirs(output_dir, exist_ok=True)

        self.worker = Worker(input_dir, output_dir, watermark_path, position, opacity, scale)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()
        self.process_button.setEnabled(False)

    def processing_finished(self):
        self.process_button.setEnabled(True)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Success", "Processing completed!")

    def processing_error(self, error):
        self.process_button.setEnabled(True)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Error", f"Processing failed: {error}")

    def select_file(self, edit, filter_str):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", filter_str)
        if file_path:
            edit.setText(file_path)

    def load_presets(self):
        preset_dir = os.path.join(os.path.dirname(__file__), '..', 'presets')
        os.makedirs(preset_dir, exist_ok=True)
        for file in os.listdir(preset_dir):
            if file.endswith('.json'):
                self.presets_list.addItem(file[:-5])

    def save_preset(self):
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Save Preset", "Preset Name:")
        if ok and name:
            preset = {
                'watermark': self.watermark_edit.text(),
                'position': self.position_combo.currentText(),
                'opacity': self.opacity_spin.value(),
                'scale': self.scale_spin.value()
            }
            preset_dir = os.path.join(os.path.dirname(__file__), '..', 'presets')
            with open(os.path.join(preset_dir, name + '.json'), 'w') as f:
                json.dump(preset, f)
            self.presets_list.addItem(name)

    def load_preset(self):
        current = self.presets_list.currentItem()
        if current:
            name = current.text()
            preset_dir = os.path.join(os.path.dirname(__file__), '..', 'presets')
            with open(os.path.join(preset_dir, name + '.json'), 'r') as f:
                preset = json.load(f)
            self.watermark_edit.setText(preset.get('watermark', ''))
            self.position_combo.setCurrentText(preset.get('position', 'right-bottom'))
            self.opacity_spin.setValue(preset.get('opacity', 0.6))
            self.scale_spin.setValue(preset.get('scale', 0.15))

    def delete_preset(self):
        current = self.presets_list.currentItem()
        if current:
            name = current.text()
            preset_dir = os.path.join(os.path.dirname(__file__), '..', 'presets')
            os.remove(os.path.join(preset_dir, name + '.json'))
            self.presets_list.takeItem(self.presets_list.row(current))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()