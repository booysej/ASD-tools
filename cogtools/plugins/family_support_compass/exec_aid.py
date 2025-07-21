from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

class ExecAidWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        anchor_card = QLabel("Today's Anchor: \n1. School dropoff\n2. Therapy\n3. Dinner prep")
        anchor_card.setStyleSheet("background: #444; color: #fff; font-size: 18px; border-radius: 8px; padding: 12px;")
        layout.addWidget(anchor_card)
        nudge_btn = QPushButton("Send gentle nudge to partner")
        nudge_btn.setStyleSheet("background: #2196f3; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(nudge_btn)
        layout.addWidget(QLabel("Visual Rewards & Streaks (coming soon)"))
        self.setLayout(layout)