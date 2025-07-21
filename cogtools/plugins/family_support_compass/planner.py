from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QListWidget, QListWidgetItem, QProgressBar
from PySide6.QtCore import Qt

class PlannerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        header = QHBoxLayout()
        self.template_dropdown = QComboBox()
        self.template_dropdown.addItems([
            "Select Template", "Bedtime Routine", "Meltdown Protocol", "School Prep"
        ])
        header.addWidget(QLabel("Templates:"))
        header.addWidget(self.template_dropdown)
        header.addStretch()
        self.load_label = QLabel("Cognitive Load Score: ")
        self.load_bar = QProgressBar()
        self.load_bar.setMaximum(100)
        self.load_bar.setValue(40)  # Placeholder
        header.addWidget(self.load_label)
        header.addWidget(self.load_bar)
        layout.addLayout(header)

        # Visual timeline placeholder
        self.timeline = QListWidget()
        for i, (task, role) in enumerate([
            ("Breakfast", "primary"),
            ("School Dropoff", "support"),
            ("Work Meeting", "reviewer"),
            ("Therapy Appointment", "primary"),
        ]):
            item = QListWidgetItem(f"{task}  [{role}]")
            color = {"primary": "#4caf50", "support": "#2196f3", "reviewer": "#ff9800"}[role]
            item.setBackground(Qt.transparent)
            item.setForeground(Qt.white)
            item.setData(Qt.UserRole, role)
            item.setToolTip(f"Role: {role}")
            item.setBackground(Qt.transparent)
            item.setForeground(Qt.white)
            item.setTextAlignment(Qt.AlignLeft)
            self.timeline.addItem(item)
        self.timeline.setStyleSheet("background: #333; color: #fff; font-size: 16px;")
        layout.addWidget(QLabel("Today's Timeline (drag-and-drop coming soon)"))
        layout.addWidget(self.timeline)
        self.setLayout(layout)