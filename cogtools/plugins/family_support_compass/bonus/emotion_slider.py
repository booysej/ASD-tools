from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt

class EmotionSliderWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("How are you feeling? (slide to select)"))
        slider_row = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(3)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        slider_row.addWidget(QLabel("😡"))
        slider_row.addWidget(QLabel("😟"))
        slider_row.addWidget(QLabel("😐"))
        slider_row.addWidget(QLabel("😊"))
        layout.addLayout(slider_row)
        layout.addWidget(self.slider)
        self.setLayout(layout)