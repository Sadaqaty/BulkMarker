from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QFormLayout, QComboBox, QDoubleSpinBox, QSpinBox,
    QTextEdit, QCheckBox, QScrollArea, QListWidget, QProgressBar,
    QStackedWidget, QRadioButton, QButtonGroup
)

def create_dashboard_page():
    page = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("Dashboard - Overview and Quick Actions"))
    # Add widgets for dashboard
    page.setLayout(layout)
    return page

def create_bulk_processing_page(main_window):
    page = QWidget()
    layout = QVBoxLayout()

    # Input folder
    input_group = QGroupBox("Input Folder")
    input_layout = QFormLayout()
    main_window.input_edit = QLineEdit()
    main_window.input_edit.setPlaceholderText("Select input folder...")
    input_button = QPushButton("Browse")
    input_button.clicked.connect(main_window.select_input_dir)
    input_layout.addRow(main_window.input_edit, input_button)
    input_group.setLayout(input_layout)

    # Output folder
    output_group = QGroupBox("Output Folder")
    output_layout = QFormLayout()
    main_window.output_edit = QLineEdit()
    main_window.output_edit.setPlaceholderText("Select output folder...")
    output_button = QPushButton("Browse")
    output_button.clicked.connect(main_window.select_output_dir)
    output_layout.addRow(main_window.output_edit, output_button)
    output_group.setLayout(output_layout)

    # Overlay type
    overlay_type_group = QGroupBox("Overlay Type")
    overlay_type_layout = QVBoxLayout()
    main_window.overlay_type_group = QButtonGroup()
    image_radio = QRadioButton("Image")
    video_radio = QRadioButton("Video")
    text_radio = QRadioButton("Text")
    main_window.overlay_type_group.addButton(image_radio, 0)
    main_window.overlay_type_group.addButton(video_radio, 1)
    main_window.overlay_type_group.addButton(text_radio, 2)
    image_radio.setChecked(True)
    overlay_type_layout.addWidget(image_radio)
    overlay_type_layout.addWidget(video_radio)
    overlay_type_layout.addWidget(text_radio)
    overlay_type_group.setLayout(overlay_type_layout)

    # Overlay config stack
    main_window.overlay_stack = QStackedWidget()

    # Image config
    image_widget = QWidget()
    image_layout = QFormLayout()
    main_window.image_file_edit = QLineEdit()
    main_window.image_file_edit.setPlaceholderText("Select image file...")
    image_browse = QPushButton("Browse")
    image_browse.clicked.connect(lambda: main_window.select_file(main_window.image_file_edit, "Images (*.png *.jpg *.svg)"))
    main_window.image_scale = QDoubleSpinBox()
    main_window.image_scale.setRange(0.01, 1.0)
    main_window.image_scale.setValue(0.15)
    main_window.image_scale.setSingleStep(0.01)
    main_window.image_position = QComboBox()
    main_window.image_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
    main_window.image_opacity = QDoubleSpinBox()
    main_window.image_opacity.setRange(0.0, 1.0)
    main_window.image_opacity.setValue(0.6)
    main_window.image_opacity.setSingleStep(0.1)
    main_window.image_rotation = QSpinBox()
    main_window.image_rotation.setRange(0, 360)
    image_layout.addRow("File:", main_window.image_file_edit)
    image_layout.addRow("", image_browse)
    image_layout.addRow("Scale:", main_window.image_scale)
    image_layout.addRow("Position:", main_window.image_position)
    image_layout.addRow("Opacity:", main_window.image_opacity)
    image_layout.addRow("Rotation (°):", main_window.image_rotation)
    image_widget.setLayout(image_layout)
    main_window.overlay_stack.addWidget(image_widget)

    # Video config
    video_widget = QWidget()
    video_layout = QFormLayout()
    main_window.video_file_edit = QLineEdit()
    main_window.video_file_edit.setPlaceholderText("Select video file...")
    video_browse = QPushButton("Browse")
    video_browse.clicked.connect(lambda: main_window.select_file(main_window.video_file_edit, "Videos (*.mp4 *.mov *.avi)"))
    main_window.video_scale = QDoubleSpinBox()
    main_window.video_scale.setRange(0.01, 1.0)
    main_window.video_scale.setValue(0.15)
    main_window.video_scale.setSingleStep(0.01)
    main_window.video_position = QComboBox()
    main_window.video_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
    main_window.video_opacity = QDoubleSpinBox()
    main_window.video_opacity.setRange(0.0, 1.0)
    main_window.video_opacity.setValue(0.6)
    main_window.video_opacity.setSingleStep(0.1)
    main_window.video_loop = QCheckBox("Loop video")
    video_layout.addRow("File:", main_window.video_file_edit)
    video_layout.addRow("", video_browse)
    video_layout.addRow("Scale:", main_window.video_scale)
    video_layout.addRow("Position:", main_window.video_position)
    video_layout.addRow("Opacity:", main_window.video_opacity)
    video_layout.addRow("", main_window.video_loop)
    video_widget.setLayout(video_layout)
    main_window.overlay_stack.addWidget(video_widget)

    # Text config
    text_widget = QWidget()
    text_layout = QFormLayout()
    main_window.text_edit = QTextEdit()
    main_window.text_edit.setPlaceholderText("Enter text to overlay...")
    main_window.text_edit.setMaximumHeight(60)
    main_window.text_font = QLineEdit("Arial")
    main_window.text_size = QSpinBox()
    main_window.text_size.setRange(10, 100)
    main_window.text_size.setValue(24)
    main_window.text_color = QLineEdit("#FFFFFF")
    main_window.text_position = QComboBox()
    main_window.text_position.addItems(["left-top", "center-top", "right-top", "left-center", "center", "right-center", "left-bottom", "center-bottom", "right-bottom"])
    main_window.text_opacity = QDoubleSpinBox()
    main_window.text_opacity.setRange(0.0, 1.0)
    main_window.text_opacity.setValue(1.0)
    main_window.text_opacity.setSingleStep(0.1)
    text_layout.addRow("Text:", main_window.text_edit)
    text_layout.addRow("Font:", main_window.text_font)
    text_layout.addRow("Size:", main_window.text_size)
    text_layout.addRow("Color (hex):", main_window.text_color)
    text_layout.addRow("Position:", main_window.text_position)
    text_layout.addRow("Opacity:", main_window.text_opacity)
    text_widget.setLayout(text_layout)
    main_window.overlay_stack.addWidget(text_widget)

    main_window.overlay_type_group.buttonClicked.connect(lambda: main_window.overlay_stack.setCurrentIndex(main_window.overlay_type_group.checkedId()))

    # Process button
    main_window.process_button = QPushButton("Start Processing")
    main_window.process_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
    main_window.process_button.clicked.connect(main_window.start_processing)

    # Progress
    main_window.progress_bar = QProgressBar()
    main_window.progress_label = QLabel("Ready")

    layout.addWidget(input_group)
    layout.addWidget(output_group)
    layout.addWidget(overlay_type_group)
    layout.addWidget(main_window.overlay_stack)
    layout.addWidget(main_window.process_button)
    layout.addWidget(main_window.progress_label)
    layout.addWidget(main_window.progress_bar)

    page.setLayout(layout)
    return page

def create_overlay_editor_page(main_window):
    page = QWidget()
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    layout = QVBoxLayout(scroll_widget)

    # Similar to bulk, but for editing presets or something
    layout.addWidget(QLabel("Overlay Editor - Configure overlays"))

    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)
    page_layout = QVBoxLayout(page)
    page_layout.addWidget(scroll_area)
    return page

def create_presets_page(main_window):
    page = QWidget()
    layout = QVBoxLayout()

    main_window.presets_list = QListWidget()
    main_window.load_presets()

    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save Preset")
    save_button.clicked.connect(main_window.save_preset)
    load_button = QPushButton("Load Preset")
    load_button.clicked.connect(main_window.load_preset)
    delete_button = QPushButton("Delete Preset")
    delete_button.clicked.connect(main_window.delete_preset)

    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(load_button)
    buttons_layout.addWidget(delete_button)

    layout.addWidget(QLabel("Manage Presets:"))
    layout.addWidget(main_window.presets_list)
    layout.addLayout(buttons_layout)

    page.setLayout(layout)
    return page

def create_export_queue_page():
    page = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("Export & Queue - Manage export settings and processing queue"))
    page.setLayout(layout)
    return page

def create_settings_page():
    page = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("Settings - Application settings"))
    page.setLayout(layout)
    return page