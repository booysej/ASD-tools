from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class FocusTaskManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Focus Task Manager (Kanban coming soon)"))
        self.setLayout(layout)