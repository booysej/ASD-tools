from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QPushButton
from PySide6.QtCore import Qt

class ChildJournalWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Child Mood & Trigger Tracker:"))
        mood_row = QHBoxLayout()
        mood_row.addWidget(QLabel("Mood:"))
        self.mood_combo = QComboBox()
        self.mood_combo.addItems(["😊 Happy", "😐 Neutral", "😟 Upset", "😡 Meltdown"])
        mood_row.addWidget(self.mood_combo)
        layout.addLayout(mood_row)
        layout.addWidget(QLabel("Triggers/Notes:"))
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Describe triggers, routines, successes...")
        layout.addWidget(self.notes)
        layout.addWidget(QLabel("ASD-style Observational Checklist (coming soon)"))
        layout.addWidget(QLabel("Family Coping Suggestions (coming soon)"))
        self.suggest_btn = QPushButton("How to Respond (AI suggestions soon)")
        self.suggest_btn.setStyleSheet("background: #2196f3; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(self.suggest_btn)
        self.setLayout(layout)