from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class ExecFunctionCoachWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Executive Function Coach (planner coming soon)"))
        self.setLayout(layout)