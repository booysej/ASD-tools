from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class NoiseVisualizerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ambient Noise Level (demo):"))
        self.noise_bar = QProgressBar()
        self.noise_bar.setMaximum(100)
        self.noise_bar.setValue(30)  # Placeholder
        self.noise_bar.setStyleSheet("QProgressBar::chunk { background: #ff9800; } QProgressBar { background: #333; color: #fff; }")
        layout.addWidget(self.noise_bar)
        self.setLayout(layout)