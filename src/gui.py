import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QLineEdit, QProgressBar,
    QTabWidget, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
    QComboBox, QListWidget, QTextEdit, QCheckBox, QStackedWidget,
    QListWidgetItem, QScrollArea, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap, QIcon

from worker import Worker
from presets import PresetsManager
from pages import (
    create_dashboard_page, create_bulk_processing_page, create_overlay_editor_page,
    create_presets_page, create_export_queue_page, create_settings_page
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulk Video Watermarker")
        self.setGeometry(100, 100, 1000, 700)

        self.presets_manager = PresetsManager(os.path.join(os.path.dirname(__file__), '..', 'presets'))

        # Set modern stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #404040;
                border: 1px solid #555;
                padding: 4px;
                border-radius: 4px;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QListWidget {
                background-color: #404040;
                border: 1px solid #555;
                color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

        # Main layout
        central_widget = create_bulk_processing_page(self)
        self.setCentralWidget(central_widget)

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

        if not input_dir or not output_dir:
            QMessageBox.warning(self, "Error", "Please select input and output folders.")
            return

        if not os.path.exists(input_dir):
            QMessageBox.warning(self, "Error", "Input folder does not exist.")
            return

        videos = [f for f in os.listdir(input_dir) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        if not videos:
            QMessageBox.warning(self, "Error", "No video files found in input folder.")
            return

        os.makedirs(output_dir, exist_ok=True)

        # Collect overlay
        overlay_type = self.overlay_type_group.checkedId()
        valid_positions = ["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"]
        
        if overlay_type == 0:  # image
            if not self.image_file_edit.text():
                QMessageBox.warning(self, "Error", "Please select an image file.")
                return
            pos_str = self.image_position.currentText()
            if pos_str not in valid_positions:
                pos_str = "center"
            overlay = {
                'type': 'image',
                'file': self.image_file_edit.text(),
                'scale': self.image_scale.value(),
                'position': tuple(pos_str.split('-')),
                'opacity': self.image_opacity.value(),
                'rotation': self.image_rotation.value()
            }
        elif overlay_type == 1:  # video
            if not self.video_file_edit.text():
                QMessageBox.warning(self, "Error", "Please select a video file.")
                return
            pos_str = self.video_position.currentText()
            if pos_str not in valid_positions:
                pos_str = "center"
            overlay = {
                'type': 'video',
                'file': self.video_file_edit.text(),
                'scale': self.video_scale.value(),
                'position': tuple(pos_str.split('-')),
                'opacity': self.video_opacity.value(),
                'loop': self.video_loop.isChecked()
            }
        elif overlay_type == 2:  # text
            if not self.text_edit.toPlainText().strip():
                QMessageBox.warning(self, "Error", "Please enter text to overlay.")
                return
            pos_str = self.text_position.currentText()
            if pos_str not in valid_positions:
                pos_str = "center"
            overlay = {
                'type': 'text',
                'text': self.text_edit.toPlainText(),
                'font': self.text_font.text(),
                'size': self.text_size.value(),
                'color': self.text_color.text(),
                'position': tuple(pos_str.split('-')),
                'opacity': self.text_opacity.value()
            }

        self.worker = Worker(input_dir, output_dir, [overlay])
        self.worker.progress.connect(lambda msg: self.progress_label.setText(msg))
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()
        self.process_button.setEnabled(False)
        self.progress_label.setText("Starting processing...")

    def processing_finished(self):
        self.process_button.setEnabled(True)
        self.progress_label.setText("All processing completed")
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Success", "Processing completed!")

    def processing_error(self, error):
        self.process_button.setEnabled(True)
        self.progress_label.setText("Error occurred")
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Error", f"Processing failed: {error}")

    def select_file(self, edit, filter_str):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", filter_str)
        if file_path:
            edit.setText(file_path)

    def load_presets(self):
        self.presets_list.clear()
        self.presets_list.addItems(self.presets_manager.load_presets_list())

    def save_preset(self):
        name, ok = QInputDialog.getText(self, "Save Preset", "Preset Name:")
        if ok and name:
            # Collect current overlay data
            overlay_type = self.overlay_type_group.checkedId()
            valid_positions = ["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"]
            
            if overlay_type == 0:  # image
                pos_str = self.image_position.currentText()
                if pos_str not in valid_positions:
                    pos_str = "center"
                data = {
                    'type': 'image',
                    'file': self.image_file_edit.text(),
                    'scale': self.image_scale.value(),
                    'position': pos_str,
                    'opacity': self.image_opacity.value(),
                    'rotation': self.image_rotation.value()
                }
            elif overlay_type == 1:  # video
                pos_str = self.video_position.currentText()
                if pos_str not in valid_positions:
                    pos_str = "center"
                data = {
                    'type': 'video',
                    'file': self.video_file_edit.text(),
                    'scale': self.video_scale.value(),
                    'position': pos_str,
                    'opacity': self.video_opacity.value(),
                    'loop': self.video_loop.isChecked()
                }
            elif overlay_type == 2:  # text
                pos_str = self.text_position.currentText()
                if pos_str not in valid_positions:
                    pos_str = "center"
                data = {
                    'type': 'text',
                    'text': self.text_edit.toPlainText(),
                    'font': self.text_font.text(),
                    'size': self.text_size.value(),
                    'color': self.text_color.text(),
                    'position': pos_str,
                    'opacity': self.text_opacity.value()
                }
            self.presets_manager.save_preset(name, data)
            self.load_presets()

    def load_preset(self):
        current = self.presets_list.currentItem()
        if current:
            name = current.text()
            data = self.presets_manager.load_preset(name)
            # Switch to bulk processing
            self.sidebar.setCurrentRow(1)
            # Set the type
            if data['type'] == 'image':
                self.overlay_type_group.button(0).setChecked(True)
                self.overlay_stack.setCurrentIndex(0)
                self.image_file_edit.setText(data.get('file', ''))
                self.image_scale.setValue(data.get('scale', 0.15))
                self.image_position.setCurrentText(data.get('position', 'right-bottom').replace(' ', '-'))
                self.image_opacity.setValue(data.get('opacity', 0.6))
                self.image_rotation.setValue(data.get('rotation', 0))
            elif data['type'] == 'video':
                self.overlay_type_group.button(1).setChecked(True)
                self.overlay_stack.setCurrentIndex(1)
                self.video_file_edit.setText(data.get('file', ''))
                self.video_scale.setValue(data.get('scale', 0.15))
                self.video_position.setCurrentText(data.get('position', 'right-bottom').replace(' ', '-'))
                self.video_opacity.setValue(data.get('opacity', 0.6))
                self.video_loop.setChecked(data.get('loop', False))
            elif data['type'] == 'text':
                self.overlay_type_group.button(2).setChecked(True)
                self.overlay_stack.setCurrentIndex(2)
                self.text_edit.setPlainText(data.get('text', ''))
                self.text_font.setText(data.get('font', 'Arial'))
                self.text_size.setValue(data.get('size', 24))
                self.text_color.setText(data.get('color', '#FFFFFF'))
                self.text_position.setCurrentText(data.get('position', 'right-bottom').replace(' ', '-'))
                self.text_opacity.setValue(data.get('opacity', 1.0))

    def delete_preset(self):
        current = self.presets_list.currentItem()
        if current:
            name = current.text()
            self.presets_manager.delete_preset(name)
            self.load_presets()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()