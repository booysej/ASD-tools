from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class CalmModeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Calm Mode Launcher (demo):"))
        self.breath_btn = QPushButton("Start Breathing Exercise")
        self.breath_btn.setStyleSheet("background: #4caf50; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(self.breath_btn)
        self.ambient_btn = QPushButton("Start Ambient Lighting/Audio")
        self.ambient_btn.setStyleSheet("background: #2196f3; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(self.ambient_btn)
        self.setLayout(layout)