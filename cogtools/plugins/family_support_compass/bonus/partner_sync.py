from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PySide6.QtCore import Qt

class PartnerSyncWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Daily Partner Sync (2-min check-in):"))
        self.worry = QLineEdit()
        self.worry.setPlaceholderText("Today's worry")
        layout.addWidget(self.worry)
        self.need = QLineEdit()
        self.need.setPlaceholderText("What I need from you")
        layout.addWidget(self.need)
        self.forget = QTextEdit()
        self.forget.setPlaceholderText("Things I'll forget unless prompted")
        layout.addWidget(self.forget)
        self.setLayout(layout)