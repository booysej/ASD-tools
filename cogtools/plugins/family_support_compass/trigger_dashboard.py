from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtCore import Qt

class TriggerDashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Family Trigger Map (customizable soon):"))
        trigger_map = QListWidget()
        for trigger in ["Noise", "Tone", "Mess", "Transitions"]:
            item = QListWidgetItem(trigger)
            item.setForeground(Qt.white)
            trigger_map.addItem(item)
        trigger_map.setStyleSheet("background: #333; color: #fff;")
        layout.addWidget(trigger_map)
        layout.addWidget(QLabel("Incident Log (tag, context, people):"))
        incident_log = QListWidget()
        for entry in ["2024-06-01: Noise - meltdown (living room)", "2024-06-02: Mess - stress (kitchen)"]:
            item = QListWidgetItem(entry)
            item.setForeground(Qt.white)
            incident_log.addItem(item)
        incident_log.setStyleSheet("background: #333; color: #fff;")
        layout.addWidget(incident_log)
        layout.addWidget(QLabel("Coping Suggestions (coming soon): quiet time, visual schedules, etc."))
        cooldown_btn = QPushButton("Start Cooldown Timer")
        cooldown_btn.setStyleSheet("background: #ff9800; color: #fff; font-weight: bold; padding: 8px; border-radius: 6px;")
        layout.addWidget(cooldown_btn)
        self.setLayout(layout)