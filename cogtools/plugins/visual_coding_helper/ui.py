from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class VisualCodingHelperWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Visual Coding Helper (flowcharts coming soon)"))
        self.setLayout(layout)