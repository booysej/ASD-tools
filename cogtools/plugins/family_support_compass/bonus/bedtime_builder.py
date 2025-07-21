from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PySide6.QtCore import Qt

class BedtimeBuilderWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bedtime Routine Builder (demo):"))
        self.timer_bar = QProgressBar()
        self.timer_bar.setMaximum(100)
        self.timer_bar.setValue(60)  # Placeholder
        self.timer_bar.setStyleSheet("QProgressBar::chunk { background: #2196f3; } QProgressBar { background: #333; color: #fff; }")
        layout.addWidget(self.timer_bar)
        layout.addWidget(QLabel("Story Prompt: 'Once upon a time...' (custom stories soon)"))
        self.setLayout(layout)